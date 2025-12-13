from flask import Blueprint, request, jsonify
from config.db import execute_query 
import jwt
import datetime

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/signup', methods=['POST'])
def signup():
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "No data received"}), 400
        
        required = ['first_name', 'last_name', 'username', 'email', 'password']
        for field in required:
            if not data.get(field):
                return jsonify({"error": f"Missing {field}"}), 400
        
        check_sql = "SELECT user_id FROM Users WHERE username = %s OR email = %s"
        existing = execute_query(check_sql, (data['username'], data['email']), fetch_data=True)
        
        if existing:
            return jsonify({"error": "Username or email already exists"}), 409
        
        # Insert user 
        insert_sql = """
        INSERT INTO Users (first_name, last_name, username, email, password) 
        VALUES (%s, %s, %s, %s, %s)
        """
        
        execute_query(insert_sql, (
            data['first_name'].strip(),
            data['last_name'].strip(),
            data['username'].strip(),
            data['email'].strip(),
            data['password']
        ))
        
        print(f" New user created: {data['username']}")
        return jsonify({
            "message": "Account created successfully!",
            "username": data['username']
        }), 201
        
    except Exception as e:
        print(f" Signup error: {str(e)}")
        return jsonify({"error": f"Server error: {str(e)}"}), 500

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.json
    username = data.get('username_or_email', '').strip()
    password = data.get('password', '')
    
    if not username or not password:
        return jsonify({"error": "Enter credentials"}), 400
    
    try:
        # Find user
        sql = "SELECT user_id, username, password FROM Users WHERE username = %s OR email = %s"
        users = execute_query(sql, (username, username), fetch_data=True)
        
        if not users:
            return jsonify({"error": "User not found"}), 401
        
        user = users[0]
        
        # password check
        if user['password'] == password:
            # Create token
            token = jwt.encode({
                'user_id': user['user_id'],
                'username': user['username'],
                'exp': datetime.datetime.utcnow() + datetime.timedelta(days=1)
            }, 'techpath-secret-123', algorithm='HS256')
            
            # Check if user has taken quiz
            check_quiz_sql = """
            SELECT career_path, description
            FROM Recommendations 
            WHERE user_id = %s
            """
            quiz_result = execute_query(check_quiz_sql, (user['user_id'],), fetch_data=True)
            
            has_quiz = len(quiz_result) > 0
            
            response_data = {
                "message": "Login successful!",
                "token": token,
                "user_id": user['user_id'],
                "username": user['username'],
                "has_quiz": has_quiz
            }
            
            
            if has_quiz:
                response_data["career"] = quiz_result[0]['career_path']
                response_data["roadmap"] = quiz_result[0]['description']
            else:
               
                response_data["message"] = "You haven't taken the quiz yet. Please take the quiz first."
            
            return jsonify(response_data), 200
        else:
            return jsonify({"error": "Wrong password"}), 401
    except Exception as e:
        return jsonify({"error": str(e)}), 500