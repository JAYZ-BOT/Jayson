import websocket
import json
import pandas as pd
from datetime import datetime

DATA_FILE = 'aviator_1xbet_data.csv'

def on_message(ws, message):
    try:
        # Print the raw message (optional for debugging)
        print(f"Raw: {message}")

        # Example JSON parse (adjust this based on actual 1xBet data format)
        data = json.loads(message)

        # Check if the message contains multiplier info
        if 'multiplier' in data:
            multiplier = data['multiplier']
            round_id = data.get('round_id', 'N/A')
            timestamp = datetime.now()

            print(f"[{timestamp}] Round: {round_id}, Multiplier: {multiplier}x")

            # Store data
            df = pd.DataFrame([[timestamp, '1xBet', round_id, multiplier]],
                              columns=['timestamp', 'platform', 'round_id', 'multiplier'])
            df.to_csv(DATA_FILE, mode='a', header=not pd.io.common.file_exists(DATA_FILE), index=False)

    except Exception as e:
        print(f"Error processing message: {e}")

def on_error(ws, error):
    print(f"WebSocket Error: {error}")

def on_close(ws, close_status_code, close_msg):
    print(f"WebSocket Closed: {close_status_code} - {close_msg}")

def on_open(ws):
    print("✅ WebSocket Connection Established")

if __name__ == "__main__":
    websocket.enableTrace(False)
    ws = websocket.WebSocketApp(
        "wss://app-demo2.spribe.io/BlueBox/websocket",
        on_message=on_message,
        on_error=on_error,
        on_close=on_close,
        on_open=on_open
    )
    ws.run_forever()
