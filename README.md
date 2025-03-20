# 🚀 Aviator Predictor Bot — AI Model with Telegram Integration

## ✅ Overview
This project is a production-ready **AI-powered Aviator game predictor** that:
- Trains a machine learning model on real payout data
- Predicts the next round’s category (`Low`, `Mid`, `High`)
- **Sends automatic predictions to your Telegram** every 60 seconds
- Retrains the model **every 12 hours** to stay accurate

## ✅ Project Structure
```
├── app.py                 # Main Flask App (Model + Telegram + Scheduler)
├── aviator_payouts.csv    # Dataset containing Aviator crash points
├── requirements.txt       # Python dependencies
├── render.yaml            # Render deployment config
└── README.md              # Project documentation
```

## ✅ Deployment on Render
1. **Connect this repo** to Render.com
2. **Environment Variables to Add on Render:**
   - `BOT_TOKEN` = Your Telegram Bot Token
   - `CHAT_ID` = Your Telegram Chat ID (user or group)
3. **Start Command (Render auto-detects):**
```
gunicorn app:app
```
4. **Deploy** and your bot starts:
   - Sending predictions every 60 seconds to Telegram
   - Auto-retraining every 12 hours

## ✅ API Endpoints (Optional Use)
### 🔄 Manual Retrain
```
POST /train
```

### 🔮 Manual Prediction
```
POST /predict
Content-Type: application/json
{
  "payout": 2.0,
  "hour": 14,
  "minute": 30,
  "day_of_week": 2
}
```
Response:
```
{ "prediction": "High" }
```

## ✅ Sample Render Logs
```
✅ Model retrained. Accuracy: 74.15%
✅ Sent to Telegram: 🚀 AI Prediction: **High**
```

## ✅ Features
✔ AI Prediction using XGBoost  
✔ Auto Telegram Notifications  
✔ Automatic Model Retraining  
✔ REST API ready  
✔ Render.com Ready  
✔ Scalable and Production-ready  

## ✅ How to Update
- Update `aviator_payouts.csv` or model logic
- Push changes to GitHub
- Render **auto redeploys** and refreshes the model

## ✅ License
MIT - Feel free to modify and use.