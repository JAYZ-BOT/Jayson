from flask import Flask, request, jsonify
import pandas as pd
import pickle
import xgboost as xgb
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.preprocessing import LabelEncoder
from apscheduler.schedulers.background import BackgroundScheduler
import telebot
import os
from datetime import datetime

app = Flask(__name__)

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")
bot = telebot.TeleBot(BOT_TOKEN)

def train_model():
    try:
        data = pd.read_csv('aviator_payouts.csv')
        data["created_at"] = pd.to_datetime(data["created_at"], errors="coerce")
        data = data[data["app"].str.upper().isin(["1XBET", "ODIBETS", "BETIKA"])]
        data["hour"] = data["created_at"].dt.hour
        data["minute"] = data["created_at"].dt.minute
        data["day_of_week"] = data["created_at"].dt.dayofweek
        data["next_payout"] = data["payout"].shift(-1)

        def categorize_multiplier(m):
            if m < 1.5: return "Low"
            elif m < 2.0: return "Mid"
            else: return "High"

        data["next_category"] = data["next_payout"].apply(categorize_multiplier)
        data = data.dropna()
        features = ["payout", "hour", "minute", "day_of_week"]
        X = data[features]
        y = data["next_category"]

        le = LabelEncoder()
        y_encoded = le.fit_transform(y)

        X_train, X_test, y_train, y_test = train_test_split(X, y_encoded, test_size=0.2, random_state=42)

        model = xgb.XGBClassifier(n_estimators=100, max_depth=7, random_state=42, use_label_encoder=False, eval_metric='mlogloss')
        model.fit(X_train, y_train)

        y_pred = model.predict(X_test)
        accuracy = accuracy_score(y_test, y_pred)

        with open('aviator_xgb_model.pkl', 'wb') as f:
            pickle.dump(model, f)
        with open('label_encoder.pkl', 'wb') as f:
            pickle.dump(le, f)

        print(f"✅ Model retrained. Accuracy: {accuracy:.2%}")
    except Exception as e:
        print(f"❌ Training error: {str(e)}")

def send_prediction_to_telegram():
    try:
        with open('aviator_xgb_model.pkl', 'rb') as f:
            model = pickle.load(f)
        with open('label_encoder.pkl', 'rb') as f:
            le = pickle.load(f)

        sample_input = pd.DataFrame([{
            "payout": 2.0,
            "hour": datetime.utcnow().hour,
            "minute": datetime.utcnow().minute,
            "day_of_week": datetime.utcnow().weekday()
        }])
        pred = model.predict(sample_input)[0]
        label = le.inverse_transform([pred])[0]
        message = f"🚀 AI Prediction: **{label}**"
        bot.send_message(CHAT_ID, message)
        print(f"✅ Sent to Telegram: {message}")
    except Exception as e:
        print(f"❌ Failed to send prediction: {e}")

@app.route('/train', methods=['POST'])
def manual_train():
    train_model()
    return jsonify({"result": "Model retrained."})

@app.route('/predict', methods=['POST'])
def predict():
    try:
        input_data = request.json
        with open('aviator_xgb_model.pkl', 'rb') as f:
            model = pickle.load(f)
        with open('label_encoder.pkl', 'rb') as f:
            le = pickle.load(f)

        df = pd.DataFrame([input_data])
        prediction = model.predict(df)[0]
        label = le.inverse_transform([prediction])[0]

        return jsonify({"prediction": label})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Scheduler: Auto retraining + Auto sending predictions
scheduler = BackgroundScheduler()
scheduler.add_job(train_model, 'interval', hours=12)  # Retrain every 12 hours
scheduler.add_job(send_prediction_to_telegram, 'interval', seconds=60)  # Predict and send every 60s
scheduler.start()

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)