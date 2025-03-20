
import logging
import sqlite3
from flask import Flask, request
from telegram import Update, Bot
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

TOKEN = 'YOUR_TELEGRAM_BOT_TOKEN'  # Replace with your token
bot = Bot(token=TOKEN)
app = Flask(__name__)
DB_FILE = 'aviator_data.db'

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

application = ApplicationBuilder().token(TOKEN).build()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("✅ Aviator SQLite Stats Bot ready! Use /stats or /stats <APPNAME>")

def compute_stats_sql(app_filter=None):
    try:
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        query = "SELECT payout FROM aviator_data"
        params = ()
        if app_filter:
            query += " WHERE app = ?"
            params = (app_filter.upper(),)
        query += " ORDER BY id DESC LIMIT 10"
        cursor.execute(query, params)
        payouts = [row[0] for row in cursor.fetchall()]
        conn.close()

        if not payouts:
            return "No data found."

        avg = sum(payouts) / len(payouts)
        high = max(payouts)
        low = min(payouts)
        low_crash_count = sum(1 for p in payouts if p < 1.5)

        return (f"📊 *SQLite Stats (Last {len(payouts)})*
"
                f"Average: {avg:.2f}x
"
                f"High: {high:.2f}x | Low: {low:.2f}x
"
                f"Rounds < 1.5x: {low_crash_count}
")
    except Exception as e:
        logger.error(f"Failed to compute stats: {e}")
        return "❌ Error processing data."

async def stats(update: Update, context: ContextTypes.DEFAULT_TYPE):
    app_filter = context.args[0] if context.args else None
    result = compute_stats_sql(app_filter)
    await update.message.reply_text(result, parse_mode='Markdown')

application.add_handler(CommandHandler('start', start))
application.add_handler(CommandHandler('stats', stats))

@app.route('/webhook', methods=['POST'])
async def webhook():
    update = Update.de_json(request.get_json(force=True), bot)
    await application.process_update(update)
    return "ok", 200

@app.route('/', methods=['GET'])
def index():
    return "✅ Aviator SQLite Stats Bot is running!", 200

if __name__ == '__main__':
    app.run(debug=True)
