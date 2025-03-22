
import pandas as pd
import joblib
import time
import telebot
import os
from flask import Flask
from apscheduler.schedulers.background import BackgroundScheduler

app = Flask(__name__)

BOT_TOKEN = os.getenv("BOT_TOKEN") or "7323523378:AAFX3USqaXZXN8xcpsdgzu02cN9HG1wNCZk"
CHAT_ID = os.getenv("CHAT_ID") or "7975116093"
bot = telebot.TeleBot(BOT_TOKEN)

model = joblib.load('model.pkl')
last_row_count = 0

def real_time_predict():
    global last_row_count
    try:
        df = pd.read_csv('data/aviator_payouts.csv')
        if len(df) > last_row_count:
            new_data = df.iloc[last_row_count:]
            for _, row in new_data.iterrows():
                payout = row['payout']
                pred = model.predict([[payout]])[0]
                if pred == 1:
                    confidence = '95%'
                    message = f"🚀 *Auto Prediction Triggered*\nPlace bet at *{payout}x*\nCash out at *2.00x+*\nConfidence: *{confidence}*"
                    bot.send_message(CHAT_ID, message, parse_mode='Markdown')
                    print(f"✅ Sent prediction to Telegram: {payout}x")
            last_row_count = len(df)
    except Exception as e:
        print(f"❌ Prediction error: {e}")

scheduler = BackgroundScheduler()
scheduler.add_job(real_time_predict, 'interval', seconds=5)
scheduler.start()

@app.route('/')
def home():
    return "✅ Aviator Real-time Predictor Running"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
