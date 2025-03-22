
import time
import random
import pandas as pd

def collect_data():
    while True:
        try:
            # Simulated payout data (Replace this with actual WebSocket or API call)
            payout = round(random.uniform(1.0, 20.0), 2)
            timestamp = pd.Timestamp.utcnow()
            platform = "1xBet"  # Hardcoded for now, can be dynamic

            # Append to CSV
            df = pd.DataFrame([[timestamp, platform, payout]], columns=["timestamp", "platform", "payout"])
            df.to_csv('data/aviator_payouts.csv', mode='a', header=False, index=False)

            print(f'✅ Collected data: {timestamp} | {platform} | {payout}x')
            time.sleep(30)  # Collect every 30 seconds
        
        except Exception as e:
            print(f'❌ Data Collection Error: {e}')

if __name__ == "__main__":
    collect_data()
