
from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

# Replace this with your actual Bot Token
BOT_TOKEN = '7323523378:AAFX3USqaXZXN8xcpsdgzu02cN9HG1wNCZk'
TELEGRAM_API_URL = f'https://api.telegram.org/bot{BOT_TOKEN}/sendMessage'

@app.route('/')
def index():
    return 'Aviator Bot Running'

# Webhook route to receive updates from Telegram
@app.route(f'/{BOT_TOKEN}', methods=['POST'])
def webhook():
    update = request.get_json()
    print("Received update:", update)

    if 'message' in update:
        chat_id = update['message']['chat']['id']
        text = update['message'].get('text', '')
        reply_text = f"✅ Received: {text}"

        # Send a reply back to the user
        requests.post(TELEGRAM_API_URL, json={
            'chat_id': chat_id,
            'text': reply_text
        })

    return jsonify({'status': 'ok'}), 200

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
