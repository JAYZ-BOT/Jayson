
from flask import Flask, request
import requests

app = Flask(__name__)

BOT_TOKEN = '7323523378:AAFX3USqaXZXN8xcpsdgzu02cN9HG1wNCZk'
TELEGRAM_API_URL = f'https://api.telegram.org/bot{BOT_TOKEN}/'

@app.route(f'/{BOT_TOKEN}', methods=['POST'])
def telegram_webhook():
    update = request.get_json()
    print(update)  # For Render logs

    if 'message' in update:
        chat_id = update['message']['chat']['id']
        text = update['message'].get('text', '')
        reply_text = f"✅ Received: {text}"
        send_message(chat_id, reply_text)

    return 'OK', 200

def send_message(chat_id, text):
    url = TELEGRAM_API_URL + 'sendMessage'
    payload = {'chat_id': chat_id, 'text': text}
    requests.post(url, json=payload)

@app.route('/')
def home():
    return "✅ Bot is running!", 200

@app.route('/ping')
def ping():
    return 'pong', 200
