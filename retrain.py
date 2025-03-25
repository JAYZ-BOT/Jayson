import pandas as pd
import joblib
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split

def auto_retrain():
    try:
        data = pd.read_csv('data/aviator_payouts.csv')
        data.dropna(inplace=True)
        data['hour'] = pd.to_datetime(data['created_at']).dt.hour
        data['minute'] = pd.to_datetime(data['created_at']).dt.minute
        data['day_of_week'] = pd.to_datetime(data['created_at']).dt.dayofweek

        # Ensure feature consistency
        features = ["payout_prev", "minute", "hour", "day_of_week"]
        X = data[features]
        y = data["payout"]

        # Train model
        model = RandomForestClassifier()
        model.fit(X, y)

        # Save model with feature names
        model_data = {"model": model, "features": features}
        joblib.dump(model_data, "model.pkl")

        print("Model retrained and saved successfully.")
    except Exception as e:
        print(f"Error during retraining: {e}")
