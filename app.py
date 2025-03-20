
from flask import Flask, request
import telebot
import os

BOT_TOKEN = os.getenv("BOT_TOKEN", "7323523378:AAFX3USqaXZXN8xcpsdgzu02cN9HG1wNCZk")
WEBHOOK_URL = os.getenv("WEBHOOK_URL", "https://jayson.onrender.com")

bot = telebot.TeleBot(BOT_TOKEN)
app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
    return "Bot is live!", 200

@app.route(f'/{BOT_TOKEN}', methods=['POST'])
def webhook():
    if request.headers.get('content-type') == 'application/json':
        json_data = request.get_data().decode('utf-8')
        update = telebot.types.Update.de_json(json_data)
        bot.process_new_updates([update])
        return '', 200
    return 'Invalid content-type', 403

@bot.message_handler(commands=['start'])
def welcome(message):
    bot.reply_to(message, "Hello! The bot is live and running on Render!")

if __name__ == '__main__':
    bot.remove_webhook()
    bot.set_webhook(url=f"{WEBHOOK_URL}/{BOT_TOKEN}")
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
