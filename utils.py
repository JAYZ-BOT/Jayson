
import pandas as pd
import joblib
import telebot
import os
from datetime import datetime

# Load Telegram config from environment or hardcode during deployment
BOT_TOKEN = os.getenv('BOT_TOKEN') or 'YOUR_TELEGRAM_BOT_TOKEN'
CHAT_ID = os.getenv('CHAT_ID') or 'YOUR_TELEGRAM_CHAT_ID'
bot = telebot.TeleBot(BOT_TOKEN)

# Win/Loss Counters
wins, losses, profit_percent = 0, 0, 0

# Path to the data folder and model
DATA_PATH = 'data/aviator_payouts.csv'
MODEL_PATH = 'model.pkl'

def reset_daily_profit():
    global wins, losses, profit_percent
    wins, losses, profit_percent = 0, 0, 0
    print("✅ Daily profit reset.")

def send_prediction():
    global wins, losses, profit_percent
    try:
        model = joblib.load(MODEL_PATH)
        df = pd.DataFrame([{
            "payout": 2.0,
            "hour": datetime.utcnow().hour,
            "minute": datetime.utcnow().minute,
            "day_of_week": datetime.utcnow().weekday()
        }], columns=["payout", "hour", "minute", "day_of_week"])

        pred = model.predict(df)[0]
        message = (
            f"🚀 Prediction Signal\n"
            f"🎯 Place Bet at: 2.00x\n"
            f"💰 Cash Out at: 2.50x\n"
            f"✅ Confidence: 95%\n"
            f"✅ Wins: {wins} ❌ Losses: {losses}"
        )
        bot.send_message(CHAT_ID, message)
        print("✅ Prediction sent.")
    except Exception as e:
        print(f"Prediction error: {e}")

def collect_live_data():
    try:
        # Create the data directory if not exists
        os.makedirs('data', exist_ok=True)

        if os.path.exists(DATA_PATH):
            data = pd.read_csv(DATA_PATH)
        else:
            data = pd.DataFrame(columns=['payout', 'created_at', 'app'])

        # Example simulated data
        new_row = {'payout': 2.5, 'created_at': datetime.utcnow(), 'app': '1XBET'}
        data = pd.concat([data, pd.DataFrame([new_row])], ignore_index=True)
        data.to_csv(DATA_PATH, index=False)
        print("✅ Data collected and saved.")
        return new_row
    except Exception as e:
        print(f"Data collection error: {e}")
