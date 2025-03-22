
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
import joblib

df = pd.read_csv('data/aviator_payouts.csv')
df['target'] = (df['payout'] >= 2.0).astype(int)
df['payout_prev'] = df['payout'].shift(1)
df.dropna(inplace=True)
X = df[['payout_prev']]
y = df['target']
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X, y)
joblib.dump(model, 'model.pkl')
print('✅ Model retrained and saved.')
