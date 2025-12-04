from flask import Blueprint, request, jsonify
from models import create_user, verify_user

auth = Blueprint("auth", __name__)

@auth.route("/signup", methods=["POST"])
def signup():
    data = request.json
    create_user(data["username"], data["email"], data["password"])
    return jsonify({"message": "User created!"})


@auth.route("/login", methods=["POST"])
def login():
    data = request.json
    user = verify_user(data["email"], data["password"])

    if user:
        return jsonify({"message": "Login successful", "user": user})
    return jsonify({"message": "Invalid email or password"}), 401
