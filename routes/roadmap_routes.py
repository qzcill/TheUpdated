from flask import Blueprint, request, jsonify
from config.db import execute_query 
import jwt

roadmap_bp = Blueprint('roadmap', __name__)

def get_user_id():
    """Get user_id from JWT token"""
    auth_header = request.headers.get('Authorization')
    if not auth_header or not auth_header.startswith('Bearer '):
        return None
    
    token = auth_header.split(' ')[1]
    try:
        decoded = jwt.decode(token, 'techpath-secret-123', algorithms=['HS256'])
        return decoded.get('user_id')
    except:
        return None

@roadmap_bp.route('/my-career', methods=['GET'])
def get_my_career():
    """Get user's career recommendation - FIXED"""
    print("\n📋 GETTING USER CAREER")
    
    user_id = get_user_id()
    if not user_id:
        print("❌ No user_id from token")
        return jsonify({"error": "Please login first"}), 401
    
    print(f"✅ User ID: {user_id}")
    
    try:
        # Get recommendation from database
        sql = """
        SELECT career_path, roadmap_link 
        FROM Recommendations 
        WHERE user_id = %s
        """
        result = execute_query(sql, (user_id,), fetch_data=True)
        
        print(f"📊 Database query result: {result}")
        
        if result and len(result) > 0:
            career_data = result[0]
            print(f"✅ Found career: {career_data['career_path']}")
            
            return jsonify({
                "success": True,
                "career": career_data['career_path'],
                "roadmap": career_data['roadmap_link'],
                "message": "Career found"
            }), 200
        else:
            print("❌ No career found in database")
            return jsonify({
                "success": False,
                "error": "No quiz results found. Please take the quiz first.",
                "has_quiz": False
            }), 404
            
    except Exception as e:
        print(f"❌ Error getting career: {e}")
        return jsonify({"error": f"Server error: {str(e)}"}), 500