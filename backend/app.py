# app.py

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from flask_marshmallow import Marshmallow 

# 1. Initialize Flask App
app = Flask(__name__)

DB_USER = 'root' 
DB_PASSWORD = '12345678'
DB_HOST = 'localhost'
DB_NAME = 'teachpath' 

app.config['SECRET_KEY'] = 'your_super_secret_key_change_me_to_a_long_random_string' 
app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = 'your_jwt_secret_key_change_me_as_well'

# 3. Initialize Extensions
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
jwt = JWTManager(app)
CORS(app) 

ma = Marshmallow(app)

import routes

# Place the models import here, inside the main execution block
if __name__ == '__main__':
    from models import * # <-- CRITICAL: Import models here to register them with SQLAlchemy
    
    with app.app_context():
        # Optional: Uncomment this line to create tables if they don't exist
        # db.create_all() 
        pass
    app.run(debug=True, port=5000)