
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

        features = ["payout", "hour", "minute", "day_of_week"]
        X = data[features]
        y = (data["payout"] >= 2.0).astype(int)

        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        model = RandomForestClassifier(n_estimators=100, random_state=42)
        model.fit(X_train, y_train)

        # Save the trained model to the root directory
        joblib.dump(model, 'model.pkl')
        print("✅ Model retrained and saved.")
    except Exception as e:
        print(f"Retrain Error: {e}")
