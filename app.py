
from flask import Flask, request, jsonify
import joblib
import pandas as pd
import numpy as np
import os

app = Flask(__name__)
model = joblib.load('model.pkl')

@app.route('/')
def home():
    return "Aviator Predictor is Live!"

@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json()
    payout = data.get('payout', None)
    if payout is None:
        return jsonify({'error': 'No payout value provided.'}), 400

    try:
        prediction = model.predict(np.array([[float(payout)]]))
        return jsonify({'prediction': prediction.tolist()})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
