
import os
from flask import Flask, request, jsonify

app = Flask(__name__)

# Replace with your actual bot token
BOT_TOKEN = 'YOUR_BOT_TOKEN'

@app.route('/', methods=['GET'])
def home():
    return 'Bot is running!', 200

@app.route('/', methods=['POST'])
def webhook():
    update = request.get_json()
    print("Received update:", update)

    # Sample handling (echo the received message)
    if 'message' in update and 'text' in update['message']:
        chat_id = update['message']['chat']['id']
        message_text = update['message']['text']
        print(f"Message from {chat_id}: {message_text}")
        # Add response logic here if needed

    return jsonify({"status": "ok"}), 200

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)
