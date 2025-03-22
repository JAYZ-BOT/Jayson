
import pandas as pd
import joblib
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split

def retrain_model():
    try:
        df = pd.read_csv('data/aviator_payouts.csv')

        # Ensure data consistency
        df['target'] = (df['payout'] >= 2.0).astype(int)
        df['payout_prev'] = df['payout'].shift(1)
        df.dropna(inplace=True)

        # Features and target
        X = df[['payout_prev']]
        y = df['target']

        # Train model
        model = RandomForestClassifier(n_estimators=100, random_state=42)
        model.fit(X, y)

        # Save model
        joblib.dump(model, 'model.pkl')
        print('✅ Model retrained and saved.')
    
    except Exception as e:
        print(f'❌ Retrain Error: {e}')

if __name__ == "__main__":
    retrain_model()
