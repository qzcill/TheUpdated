from flask import Flask, request, jsonify
import mysql.connector

app = Flask(__name__)

# ------------------------
# DATABASE CONNECTION
# ------------------------
def get_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",          
        password="12345678",          
        database="techpath"   
    )

# ------------------------
# SIGNUP ROUTE
# ------------------------
@app.route("/signup", methods=["POST"])
def signup():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    try:
        conn = get_db()
        cursor = conn.cursor()

        cursor.execute(
            "INSERT INTO users (username, password) VALUES (%s, %s)",
            (username, password)
        )
        conn.commit()
        cursor.close()
        conn.close()

        return jsonify({"message": "Signup successful!"}), 201

    except mysql.connector.IntegrityError:
        return jsonify({"error": "Username already exists!"}), 400

# ------------------------
# LOGIN ROUTE
# ------------------------
@app.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    conn = get_db()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM users WHERE username=%s AND password=%s",
        (username, password)
    )
    user = cursor.fetchone()

    cursor.close()
    conn.close()

    if user:
        return jsonify({"message": "Login successful!"}), 200
    else:
        return jsonify({"error": "Invalid username or password!"}), 401

# ------------------------
# RUN SERVER
# ------------------------
if __name__ == "__main__":
    app.run(debug=True)
