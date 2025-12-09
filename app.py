from flask import Flask, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS

# Import blueprints
from routes.auth_routes import auth_bp
from routes.quiz_routes import quiz_bp
from routes.roadmap_routes import roadmap_bp

app.register_blueprint(auth_bp, url_prefix='/api/auth')
app.register_blueprint(quiz_bp, url_prefix='/api/quiz')
app.register_blueprint(roadmap_bp, url_prefix='/api/roadmap')

@app.route('/')
def home():
    return jsonify({"message": "TechPath Backend Running"})

if __name__ == '__main__':
    print(" Server starting at http://localhost:5000")
    print(" Test: http://localhost:5000/")
    app.run(debug=True, port=5000)

@app.route('/api/test-db', methods=['GET'])
def test_db():
    """Test database connection and inserts"""
    from config.db import execute_query
    try:
        # Test 1: Check connection
        test_query = "SELECT COUNT(*) as user_count FROM Users"
        result = execute_query(test_query, fetch_data=True)
        
        # Test 2: Try to insert into UserAnswers
        test_insert = """
        INSERT INTO UserAnswers (user_id, question_id, selected_option)
        VALUES (%s, %s, %s)
        """
        execute_query(test_insert)
        
        # Test 3: Try to insert into Recommendations
        test_rec = """
        INSERT INTO Recommendations (user_id, career_path, description)
        VALUES (%s, %s, %s)
        """
        execute_query(test_rec)
        
        return jsonify({
            "db_status": "connected",
            "user_count": result[0]['user_count'] if result else 0,
            "message": "Test data inserted successfully"
        })
    except Exception as e:
        return jsonify({"db_status": "error", "error": str(e)})
    