
from flask import Flask, request
import telegram
import pandas as pd
import joblib
from apscheduler.schedulers.background import BackgroundScheduler
import numpy as np
import os
import random
import time

app = Flask(__name__)

TOKEN = '7323523378:AAFX3USqaXZXN8xcpsdgzu02cN9HG1wNCZk'
CHAT_ID = '7975116093'
bot = telegram.Bot(token=TOKEN)

# Load your model
model = joblib.load('model.pkl')

def auto_predict():
    try:
        # Simulate input features (replace with real data fetching)
        sample_data = pd.DataFrame([np.random.rand(5)], columns=['feature1', 'feature2', 'feature3', 'feature4', 'feature5'])
        predicted_multiplier = round(float(model.predict(sample_data)[0]), 2)

        # Dynamically calculate confidence (example logic)
        confidence = random.randint(80, 99)

        # Build the betting message
        message = f"""
🎯 Place Bet at: 1.00x
💰 Cash Out at: {predicted_multiplier}x
✅ Confidence Level: {confidence}%

⏳ Waiting for result...
"""
        bot.send_message(chat_id=CHAT_ID, text=message)

        # Simulate countdown/waiting (can be async/removed if desired)
        time.sleep(5)

        # Random win/lose simulation based on confidence
        outcome = '✅ WIN! 🎉' if random.randint(0, 100) < confidence else '❌ LOSS!'
        bot.send_message(chat_id=CHAT_ID, text=f"🎲 Result: Predicted Multiplier {predicted_multiplier}x\n{outcome}")

    except Exception as e:
        bot.send_message(chat_id=CHAT_ID, text=f'❌ Prediction error: {str(e)}')

# Schedule automatic prediction every 30 seconds
scheduler = BackgroundScheduler()
scheduler.add_job(auto_predict, 'interval', seconds=30)
scheduler.start()

@app.route(f'/{TOKEN}', methods=['POST'])
def webhook():
    update = telegram.Update.de_json(request.get_json(force=True), bot)
    chat_id = update.message.chat.id
    message_text = update.message.text

    if message_text == '/start':
        bot.send_message(chat_id=chat_id, text='✅ Aviator Bot started. Predictions run every 30 seconds.')
    else:
        bot.send_message(chat_id=chat_id, text='Unknown command.')

    return 'ok'

@app.route('/')
def index():
    return 'Aviator Bot running with auto predictions.'

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
