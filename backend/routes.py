# routes.py
from flask import request, jsonify
from app import app, db, bcrypt 
from models import User, QuizQuestion, QuizOption, UserAnswer, Recommendation, quiz_schema 
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from sqlalchemy.orm import joinedload 


@app.route('/api/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')

    if not all([username, email, password]):
        return jsonify({"msg": "Missing required fields"}), 400

    if User.query.filter_by(username=username).first() or User.query.filter_by(email=email).first():
        return jsonify({"msg": "Username or email already exists"}), 400

    hashed_password = bcrypt.generate_password_hash(password.encode('utf-8')).decode('utf-8')

    new_user = User(
        first_name=data.get('first_name'),
        last_name=data.get('last_name'),
        username=username,
        email=email,
        password=hashed_password
    )

    db.session.add(new_user)
    db.session.commit()

    return jsonify({"msg": "User registered successfully"}), 201

@app.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    user = User.query.filter_by(username=username).first()

    if user and bcrypt.check_password_hash(user.password, password.encode('utf-8')):
        access_token = create_access_token(identity=user.user_id)
        
        return jsonify(access_token=access_token, user_id=user.user_id), 200
    
    return jsonify({"msg": "Bad username or password"}), 401


# Fetch all quiz questions and options
@app.route('/api/quiz', methods=['GET'])
@jwt_required()
def get_quiz():
    questions = QuizQuestion.query.options(joinedload(QuizQuestion.options)).all()
    
    result = quiz_schema.dump(questions)
    
    return jsonify(result), 200

@app.route('/api/quiz/submit', methods=['POST'])
@jwt_required()
def submit_quiz():
    current_user_id = get_jwt_identity()
    answers = request.get_json() 

    if not answers:
        return jsonify({"msg": "No answers provided"}), 400
    
    UserAnswer.query.filter_by(user_id=current_user_id).delete()
    
    total_value = 0
    
    # 2. Process and save new answers
    for answer in answers:
        q_id = answer.get('question_id')
        o_id = answer.get('selected_option_id')
        
        
        option = QuizOption.query.filter_by(option_id=o_id, question_id=q_id).first()
        
        if not option:
            db.session.rollback() 
            return jsonify({"msg": f"Invalid option {o_id} for question {q_id}"}), 400

        new_answer = UserAnswer(
            user_id=current_user_id,
            question_id=q_id,
            selected_option=o_id
        )
        db.session.add(new_answer)
        total_value += option.value 
        
    db.session.commit()

    if total_value < 10:
        path = "Data Analyst"
        desc = "Focus on data interpretation and logical structure."
    elif total_value < 20:
        path = "Full Stack Developer"
        desc = "Balanced skills across technical and creative domains."
    else:
        path = "UX/UI Designer"
        desc = "Strong affinity for design and user-centric problem solving."
        
    recommendation = Recommendation.query.filter_by(user_id=current_user_id).first()

    if recommendation:
        recommendation.career_path = path
        recommendation.description = desc
    else:
        new_rec = Recommendation(user_id=current_user_id, career_path=path, description=desc)
        db.session.add(new_rec)
        
    db.session.commit()
    
    return jsonify({"msg": "Answers submitted and recommendation generated.", "career_path": path}), 200

@app.route('/api/recommendation', methods=['GET'])
@jwt_required()
def get_recommendation():
    current_user_id = get_jwt_identity()
    
    recommendation = Recommendation.query.filter_by(user_id=current_user_id).first()
    
    if not recommendation:
        return jsonify({"msg": "No recommendation found. Please take the quiz."}), 404

    return jsonify({
        "career_path": recommendation.career_path,
        "description": recommendation.description,
        "date_generated": recommendation.date_generated.strftime('%Y-%m-%d %H:%M:%S')
    }), 200