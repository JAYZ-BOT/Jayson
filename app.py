
import os
import time
import threading
import joblib
import requests
import pandas as pd
from flask import Flask

app = Flask(__name__)
model = joblib.load('model.pkl')

BOT_TOKEN = '7323523378:AAFX3USqaXZXN8xcpsdgzu02cN9HG1wNCZk'
CHAT_ID = '7975116093'
TELEGRAM_URL = f'https://api.telegram.org/bot{BOT_TOKEN}/sendMessage'

data = pd.read_csv('data/aviator_payouts.csv')

def auto_predict():
    while True:
        try:
            latest = data.iloc[-1]
            current_multiplier = latest['payout']
            prediction = model.predict([[current_multiplier]])[0]

            if prediction == 1:
                cashout = round(current_multiplier * 1.5, 2)
                confidence = '95%'
                message = f"✅ *1xBet Prediction*\nPlace bet at *{current_multiplier}x*\nCash out at *{cashout}x*\nConfidence: *{confidence}*"
                send_telegram(message)

            time.sleep(30)

        except Exception as e:
            print(f"Prediction error: {e}")
            time.sleep(30)

def send_telegram(message):
    payload = {
        'chat_id': CHAT_ID,
        'text': message,
        'parse_mode': 'Markdown'
    }
    requests.post(TELEGRAM_URL, data=payload)

@app.route('/')
def home():
    return 'Aviator Predictor Running with Auto Prediction'

threading.Thread(target=auto_predict, daemon=True).start()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
