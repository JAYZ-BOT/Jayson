from flask import Flask
from apscheduler.schedulers.background import BackgroundScheduler
import os
from joblib import load

app = Flask(__name__)
MODEL_PATH = 'model.pkl'

# Scheduled background job with exception handling
def job():
    try:
        if os.path.exists(MODEL_PATH):
            model = load(MODEL_PATH)
            print("Model loaded successfully.")
        else:
            print(f"Error: {MODEL_PATH} not found!")
    except Exception as e:
        print(f"Error in scheduled job: {e}")

def create_app():
    if not app.debug or os.environ.get("WERKZEUG_RUN_MAIN") == "true":
        scheduler = BackgroundScheduler()
        scheduler.add_job(job, 'interval', minutes=5)
        scheduler.start()
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
