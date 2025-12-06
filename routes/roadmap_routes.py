from flask import Blueprint, jsonify, request
from utils.auth_middleware import token_required
from config.db import execute_query 
import json

roadmap_bp = Blueprint('roadmap', __name__)


@roadmap_bp.route('/suggested-major', methods=['GET'])
@token_required 
def get_suggested_major():
    user_id = request.user_id

    try:
        query = "SELECT career_path, description, roadmap_link FROM Recommendations WHERE user_id = %s"
        result = execute_query(query, (user_id,))
        
        if result:
            recommendation = result[0]
            return jsonify({
                "career_path": recommendation['career_path'],
                "description": recommendation['description'],
                "roadmap_link": recommendation['roadmap_link']
            }), 200
        else:
            return jsonify({"message": "No recommendation found for this user. Please complete the quiz."}), 404

    except Exception as e:
        print(f"Error fetching suggested major: {e}")
        return jsonify({"message": "Internal Server Error"}), 500


@roadmap_bp.route('/<string:major>', methods=['GET'])
@token_required
def get_roadmap_details(major):
    mock_data = {
        "": [
            {"stage": 1, "title": " ()", "topics": ["", ""]},
            {"stage": 2, "title": " ()", "topics": ["", ""]},
        ],
        "": [
            {"stage": 1, "title": " ()", "topics": ["", ""]},
            {"stage": 2, "title": " ()", "topics": ["", ""]},
        ],
        "": [
            {"stage": 1, "title": "()", "topics": ["", ""]},
            {"stage": 2, "title": "()", "topics": ["", ""]},
        ]
    }

    if major in mock_data:
        return jsonify({
            "major": major,
            "roadmap_details": mock_data[major]
        }), 200
    else:
        return jsonify({"message": f"Roadmap for major '{major}' not found."}), 404