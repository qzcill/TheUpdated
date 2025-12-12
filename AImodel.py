from flask import Flask, request, jsonify
from flask_cors import CORS
import numpy as np
import joblib   

app = Flask(__name__)
CORS(app)

model = joblib.load("AIFinal_XGBoost_Pipeline.pkl")  

@app.route("/predict", methods=["POST"])
def predict():
    data = request.get_json()

    print("Received from frontend:", data)

    values = [
        float(data["q1"]),
        float(data["q2"]),
        float(data["q3"]),
        float(data["q4"]),
        float(data["q5"]),
        float(data["q6"]),
        float(data["q7"]),
        float(data["q8"]),
        float(data["q9"]),
        float(data["q10"])
    ]

    arr = np.array([values])    

    
    prediction = model.predict(arr)[0]

    return jsonify({
        "prediction": str(prediction)
    })


