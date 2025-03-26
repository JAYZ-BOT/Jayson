from flask import Flask, jsonify
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime
import pandas as pd
import joblib
from utils import send_prediction, collect_live_data
from retrain import auto_retrain
import os

app = Flask(__name__)
DATA_PATH = 'data/aviator_payouts.csv'
round_count = 0  # Tracks the number of rounds collected

@app.route('/')
def home():
    return jsonify({"message": "Hello, Render!"})

def real_time_prediction():
    global round_count

    # Step 1: Collect live data for the round
    collect_live_data()  # Ensure every round is collected in aviator_payouts.csv
    round_count += 1

    # Step 2: Check if retraining is needed after 200 rounds
    if round_count >= 200:
        print("🔄 Retraining model...")
        auto_retrain()
        round_count = 0

    # Step 3: Generate predictions for the next round based on model confidence
    try:
        model = joblib.load("model.pkl")
        current_data = pd.DataFrame([{
            "payout": 2.0,
            "hour": datetime.utcnow().hour,
            "minute": datetime.utcnow().minute,
            "day_of_week": datetime.utcnow().weekday()
        }], columns=["payout", "hour", "minute", "day_of_week"])
        
        prediction = model.predict(current_data)[0]

        if prediction >= 2.00:
            send_prediction()  # Send only if prediction confidence is for 2.00x+
            print(f"🚀 Prediction triggered for multiplier 2.00x+: {prediction}")

    except Exception as e:
        print(f"Prediction error: {e}")

scheduler = BackgroundScheduler()
scheduler.add_job(real_time_prediction, 'interval', seconds=60, id='prediction_job')  # Trigger every minute for real-time rounds
scheduler.start()

if __name__ == '__main__':
    try:
        app.run(debug=True)
    except (KeyboardInterrupt, SystemExit):
        scheduler.shutdown()
