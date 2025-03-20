from flask import Flask, request
import requests
import os

BOT_TOKEN = os.environ.get("BOT_TOKEN")
WEBHOOK_URL = os.environ.get("WEBHOOK_URL")

app = Flask(__name__)

# Set Telegram webhook immediately after app creation
requests.get(f"https://api.telegram.org/bot{BOT_TOKEN}/setWebhook?url={WEBHOOK_URL}")

@app.route('/', methods=['GET'])
def home():
    return 'Bot is running'

@app.route(f'/{BOT_TOKEN}', methods=['POST'])
def receive_update():
    update = request.get_json()
    # Handle the Telegram update here
    print(update)
    return "OK", 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)