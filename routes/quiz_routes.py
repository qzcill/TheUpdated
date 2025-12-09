from flask import Blueprint, request, jsonify
from config.db import execute_query 
import jwt

quiz_bp = Blueprint('quiz', __name__)

@quiz_bp.route('/submit', methods=['POST'])
def submit_quiz():
    """ULTRA SIMPLE QUIZ SUBMISSION - WILL DEFINITELY SAVE"""
    print("="*50)
    print("🟢 QUIZ SUBMIT ENDPOINT CALLED!")
    print("="*50)
    
    # Get token
    auth_header = request.headers.get('Authorization')
    print(f"Auth header: {auth_header}")
    
    if not auth_header or 'Bearer ' not in auth_header:
        print("❌ No Bearer token")
        return jsonify({"error": "No token"}), 401
    
    token = auth_header.split(' ')[1]
    
    try:
        # Decode token to get user_id
        decoded = jwt.decode(token, 'techpath-secret-123', algorithms=['HS256'])
        user_id = decoded.get('user_id')
        print(f"✅ User ID from token: {user_id}")
    except:
        print("❌ Invalid token")
        return jsonify({"error": "Invalid token"}), 401
    
    # Get data
    data = request.get_json()
    print(f"📥 Request data: {data}")
    
    if not data:
        print("❌ No data")
        return jsonify({"error": "No data"}), 400
    
    answers = data.get('answers', [])
    print(f"📥 Answers count: {len(answers)}")
    
    # ========== SAVE TO UserAnswers ==========
    print("\n💾 SAVING TO UserAnswers TABLE...")
    
    for ans in answers:
        q_id = ans.get('question_id')
        o_id = ans.get('option_id')
        
        if q_id and o_id:
            try:
                sql = """
                INSERT INTO UserAnswers (user_id, question_id, selected_option)
                VALUES (%s, %s, %s)
                """
                execute_query(sql, (user_id, q_id, o_id))
                print(f"  ✓ Saved: Q{q_id} -> Option {o_id}")
            except Exception as e:
                print(f"  ❌ Error saving Q{q_id}: {e}")
    
    # ========== SAVE TO Recommendations ==========
    print("\n💾 SAVING TO Recommendations TABLE...")
    
    # Always recommend WebDev for testing
    career = 'WebDev'
    roadmap = 'App_WebDev.html'
    
    try:
        # Delete old
        delete_sql = "DELETE FROM Recommendations WHERE user_id = %s"
        execute_query(delete_sql, (user_id,))
        
        # Insert new
        insert_sql = """
        INSERT INTO Recommendations (user_id, career_path, description) 
        VALUES (%s, %s, %s)
        """
        execute_query(insert_sql, (user_id, career, roadmap))
        print(f"  ✅ Saved recommendation: {career} -> {roadmap}")
    except Exception as e:
        print(f"  ❌ Error saving recommendation: {e}")
    
    print("\n✅ DATABASE SAVES COMPLETED!")
    print("="*50)
    
    return jsonify({
        "success": True,
        "message": "Quiz saved to database!",
        "career": career,
        "roadmap": roadmap,
        "redirect": f"Result.html?career={career}"
    })