
import pandas as pd
import joblib
from sklearn.linear_model import LogisticRegression

df = pd.read_csv('data/aviator_payouts.csv')
df['payout'] = pd.to_numeric(df['payout'], errors='coerce')
df = df.dropna()

def label(row):
    if row < 2:
        return 0
    elif row < 5:
        return 1
    else:
        return 2

df['target'] = df['payout'].apply(label)

X = df[['payout']].values
y = df['target'].values

model = LogisticRegression()
model.fit(X, y)

joblib.dump(model, 'model.pkl')
print("Model retrained and saved as model.pkl")
