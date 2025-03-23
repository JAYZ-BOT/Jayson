from flask import Flask, jsonify
from apscheduler.schedulers.background import BackgroundScheduler
from utils import send_prediction, reset_daily_profit, collect_live_data
from retrain import auto_retrain

app = Flask(__name__)

# Scheduler
scheduler = BackgroundScheduler()
scheduler.add_job(auto_retrain, 'interval', hours=12, max_instances=1)
scheduler.add_job(reset_daily_profit, 'cron', hour=0, minute=0)
scheduler.add_job(collect_live_data, 'interval', seconds=5, max_instances=3)
scheduler.add_job(send_prediction, 'interval', seconds=5, max_instances=3)
scheduler.start()

@app.route("/")
def home():
    return "✅ Aviator Predictor Running with Auto-Retrain & Data Collection"

if __name__ == "__main__":
    app.run()
