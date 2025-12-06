from flask import Blueprint, jsonify, request
from utils.auth_middleware import token_required
from config.db import execute_query 
import json

quiz_bp = Blueprint('quiz', __name__)

@quiz_bp.route('/questions', methods=['GET'])
def get_quiz_questions():
    """ quiz answers being directed  """
    try:
        questions_query = "SELECT question_id, question_text, category FROM QuizQuestions"
        questions = execute_query(questions_query)
        
        if not questions:
            return jsonify({"message": "No questions available."}), 404

        options_query = "SELECT option_id, question_id, option_text, value FROM QuizOptions"
        options = execute_query(options_query)

        options_map = {}
        for opt in options:
            qid = opt['question_id']
            if qid not in options_map:
                options_map[qid] = []
            options_map[qid].append({
                "option_id": opt['option_id'],
                "option_text": opt['option_text'],
                "value": opt['value'] 
            })
        
        full_quiz = []
        for q in questions:
            q_id = q['question_id']
            full_quiz.append({
                "question_id": q_id,
                "question_text": q['question_text'],
                "category": q['category'],
                "options": options_map.get(q_id, [])
            })
            
        return jsonify(full_quiz), 200

    except Exception as e:
        print(f"Error fetching quiz questions: {e}")
        return jsonify({"message": "Internal Server Error"}), 500


def determine_recommendation(user_id, answers):
    """ analyzing answers... """
    try:
        option_ids = [str(a['option_id']) for a in answers if 'option_id' in a]
        if not option_ids:
             raise ValueError("No valid answers provided for scoring.")

        option_ids_str = ', '.join(option_ids)
        
        query = f"SELECT SUM(value) as total_score FROM QuizOptions WHERE option_id IN ({option_ids_str})"
        result = execute_query(query)
        
        total_score = result[0]['total_score'] if result and result[0]['total_score'] is not None else 0

        if total_score >= 80:
            path = ""
            desc = ""
            link = "/roadmap/"
        elif total_score >= 50:
            path = ""
            desc = "."
            link = "/roadmap/"
        else:
            path = ""
            desc = "."
            link = "/roadmap/"
            

        save_rec_query = """
        INSERT INTO Recommendations (user_id, career_path, description, roadmap_link)
        VALUES (%s, %s, %s, %s)
        ON DUPLICATE KEY UPDATE 
        career_path = VALUES(career_path), description = VALUES(description), roadmap_link = VALUES(roadmap_link)
        """
        execute_query(save_rec_query, (user_id, path, desc, link))

        return path

    except Exception as e:
        print(f"Error determining recommendation: {e}")
        raise


@quiz_bp.route('/submit-answers', methods=['POST'])
@token_required 
def submit_answers():
    """takes user answers and save it in the database like : {"answers": [{"question_id": 1, "option_id": 5}, ...]}"""
    user_id = request.user_id 
    data = request.get_json()
    answers = data.get('answers')

    if not answers or not isinstance(answers, list):
        return jsonify({"message": "Invalid or missing answers list."}), 400

    try:
  
        save_answer_query = """
        INSERT INTO UserAnswers (user_id, question_id, option_id)
        VALUES (%s, %s, %s)
        ON DUPLICATE KEY UPDATE option_id = VALUES(option_id)
        """
        
        for answer in answers:
            if 'question_id' in answer and 'option_id' in answer:
                execute_query(save_answer_query, (user_id, answer['question_id'], answer['option_id']))
        
        recommended_major = determine_recommendation(user_id, answers)

        return jsonify({
            "message": "Answers submitted and recommendation determined successfully.",
            "recommended_major": recommended_major
        }), 200

    except Exception as e:
        print(f"Error submitting answers: {e}")
        return jsonify({"message": "Failed to process answers or determine recommendation."}), 500