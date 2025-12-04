from database import get_connection
from werkzeug.security import generate_password_hash, check_password_hash

def create_user(username, email, password):
    db = get_connection()
    cursor = db.cursor()

    hashed = generate_password_hash(password)

    sql = "INSERT INTO users (username, email, password) VALUES (%s, %s, %s)"
    cursor.execute(sql, (username, email, hashed))

    db.commit()
    cursor.close()
    db.close()


def verify_user(email, password):
    db = get_connection()
    cursor = db.cursor(dictionary=True)

    sql = "SELECT * FROM users WHERE email=%s"
    cursor.execute(sql, (email,))
    user = cursor.fetchone()

    cursor.close()
    db.close()

    if user and check_password_hash(user["password"], password):
        return user
    return None
