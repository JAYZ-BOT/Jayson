
from flask import Flask, request
import sqlite3

app = Flask(__name__)

@app.route('/stats', methods=['GET'])
def stats():
    conn = sqlite3.connect('aviator.db')
    cursor = conn.cursor()
    cursor.execute('SELECT payout FROM game_data ORDER BY id DESC LIMIT 100')
    payouts = [row[0] for row in cursor.fetchall()]
    conn.close()

    if not payouts:
        return "No data available."

    avg = sum(payouts) / len(payouts)
    high = max(payouts)
    low = min(payouts)
    low_crash_count = sum(1 for p in payouts if p < 1.5)

    return (f"📊 *SQLite Stats (Last {len(payouts)})*\n"
            f"Average: {avg:.2f}x\n"
            f"High: {high:.2f}x | Low: {low:.2f}x\n"
            f"Rounds < 1.5x: {low_crash_count}")

if __name__ == '__main__':
    app.run()
