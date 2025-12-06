from flask import Blueprint, request, jsonify, session
from config.db import execute_query 

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/signup', methods=['POST'])
def signup():
    data = request.get_json()
    first_name = data.get('first_name')
    last_name = data.get('last_name')
    username = data.get('username')
    email = data.get('email')
    password = data.get('password') 

    if not all([first_name, last_name, username, email, password]):
        return jsonify({"message": "Missing required fields"}), 400



    check_query = "SELECT user_id FROM Users WHERE username = %s OR email = %s"
    existing_user = execute_query(check_query, (username, email), fetch_data=True)
    
    if existing_user:
        return jsonify({"message": "User with this username or email already exists."}), 409

    insert_query = """
    INSERT INTO Users (first_name, last_name, username, email, password) 
    VALUES (%s, %s, %s, %s, %s)
    """
    params = (first_name, last_name, username, email, password)
    
    try:
        execute_query(insert_query, params, fetch_data=False)
        return jsonify({
            "message": "User created successfully (WARNING: Plaintext password saved).",
        }), 201

    except Exception as e:
        print(f"Error during user creation/database interaction: {e}")
        return jsonify({"message": "Internal Server Error during signup."}), 500


@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username_or_email = data.get('username_or_email')
    password_input = data.get('password') 

    if not username_or_email or not password_input:
        return jsonify({"message": "Missing username/email or password"}), 400

    query = "SELECT user_id, username, password FROM Users WHERE username = %s OR email = %s"
    user = execute_query(query, (username_or_email, username_or_email), fetch_data=True)

    if user and len(user) > 0:
        user_data = user[0]
        stored_password = user_data['password'] 
        
        if password_input == stored_password:
            
            session['user_id'] = user_data['user_id'] 
            
            return jsonify({
                "message": "Login successful (WARNING: Plaintext comparison).", 
                "user_id": user_data['user_id'],
                "username": user_data['username']
            }), 200
        else:
            return jsonify({"message": "Invalid credentials"}), 401
    else:
        return jsonify({"message": "Invalid credentials"}), 401


@auth_bp.route('/logout', methods=['POST'])
def logout():
    session.pop('user_id', None)
    return jsonify({"message": "Logout successful"}), 200