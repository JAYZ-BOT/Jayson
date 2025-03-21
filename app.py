# app.py

from flask import Flask
app = Flask(__name__)

@app.route('/')
def index():
    return 'Aviator Bot Running'

if __name__ == '__main__':
    app.run()