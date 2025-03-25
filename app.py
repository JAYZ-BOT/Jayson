from flask import Flask, jsonify
from apscheduler.schedulers.background import BackgroundScheduler
from utils import send_prediction, reset_daily_profit, collect_live_data
from retrain import auto_retrain
import pandas as pd
import joblib

app = Flask(__name__)

# Scheduler
scheduler = BackgroundScheduler()
scheduler.add_job(auto_retrain, 'interval', hours=12, max_instances=1)
scheduler.add_job(reset_daily_profit, 'cron', hour=0, minute=0)
scheduler.add_job(collect_live_data, 'interval', seconds=5, max_instances=3)
scheduler.add_job(send_prediction, 'interval', seconds=10, max_instances=1)
scheduler.start()

# Load model and feature names
model_data = joblib.load("model.pkl")
model = model_data["model"]
features = model_data["features"]

@app.route("/predict", methods=["GET"])
def predict():
    try:
        latest_data = collect_live_data()  # Fetch latest data sample
        X_new = pd.DataFrame([latest_data])
        X_new = X_new.reindex(columns=features, fill_value=0)  # Ensure feature alignment

        prediction = model.predict(X_new)[0]
        return jsonify({"prediction": prediction})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000, debug=True)
