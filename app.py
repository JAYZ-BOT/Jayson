
import logging
from flask import Flask, request
from telegram import Update, Bot
from telegram.ext import Dispatcher, CommandHandler, CallbackContext

TOKEN = 'YOUR_TELEGRAM_BOT_TOKEN'  # Replace with your token
bot = Bot(token=TOKEN)

app = Flask(__name__)

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

dispatcher = Dispatcher(bot=bot, update_queue=None, workers=0, use_context=True)

def start(update: Update, context: CallbackContext):
    update.message.reply_text("✅ Hello! Your bot is running on webhook + WSGI.")

def help_command(update: Update, context: CallbackContext):
    update.message.reply_text("ℹ️ Use /start to test the bot.")

dispatcher.add_handler(CommandHandler('start', start))
dispatcher.add_handler(CommandHandler('help', help_command))

@app.route('/webhook', methods=['POST'])
def webhook():
    try:
        update = Update.de_json(request.get_json(force=True), bot)
        dispatcher.process_update(update)
    except Exception as e:
        logger.error(f"Error processing update: {e}")
    return "ok", 200

@app.route('/', methods=['GET'])
def index():
    return "✅ Bot is live", 200

if __name__ == '__main__':
    app.run(debug=True)
