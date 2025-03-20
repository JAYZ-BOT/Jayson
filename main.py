from flask import Flask, request
import os

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST', 'HEAD'])
@app.route('/webhook', methods=['GET', 'POST', 'HEAD'])
def index():
    if request.method in ['GET', 'HEAD']:
        return 'Webhook is live!', 200
    elif request.method == 'POST':
        # Process Telegram updates here
        return 'OK', 200
    return 'Method Not Allowed', 405

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)
