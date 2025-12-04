from flask import Flask, render_template, request, redirect, session
from database import get_connection

app = Flask(__name__)
app.secret_key = "secret123"

@app.route("/")
def home():
    return render_template("login.html")

@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        username = request.form["username"]
        email = request.form["email"]
        password = request.form["password"]

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("INSERT INTO users (username, email, password) VALUES (%s, %s, %s)",
                       (username, email, password))
        conn.commit()

        return redirect("/login")

    return render_template("signup.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM users WHERE email=%s AND password=%s",
                       (email, password))
        user = cursor.fetchone()

        if user:
            session["user_id"] = user[0]
            return redirect("/roadmap")
        else:
            return "Wrong email or password"

    return render_template("login.html")

@app.route("/roadmap")
def roadmap():
    if "user_id" not in session:
        return redirect("/login")
    return render_template("roadmap.html")

if __name__ == "__main__":
    app.run(debug=True)
