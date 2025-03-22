
from flask import Flask
import threading
import retrain
import data_collector
from apscheduler.schedulers.background import BackgroundScheduler

app = Flask(__name__)

# Auto-retraining every 12 hours
scheduler = BackgroundScheduler()
scheduler.add_job(retrain.retrain_model, 'interval', hours=12)
scheduler.start()

# Run data collector in background
threading.Thread(target=data_collector.collect_data, daemon=True).start()

@app.route('/')
def home():
    return "✅ Aviator Predictor Running with Auto-Retrain & Data Collection"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
