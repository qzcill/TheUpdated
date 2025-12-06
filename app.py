from flask import Flask, jsonify
from flask_cors import CORS  
from routes.auth_routes import auth_bp
from routes.quiz_routes import quiz_bp
from routes.roadmap_routes import roadmap_bp
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)


app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', '12345678') 


CORS(app) 

app.register_blueprint(auth_bp, url_prefix='/api/auth')
app.register_blueprint(quiz_bp, url_prefix='/api/quiz')
app.register_blueprint(roadmap_bp, url_prefix='/api/roadmap')

@app.route('/')
def home():
    """ tesssttttt."""
    return jsonify({"message": "Python/Flask Server is running you can start twin "})

if __name__ == '__main__':
    app.run(debug=True)