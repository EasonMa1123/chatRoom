from flask import Flask, render_template, request, jsonify
import time

app = Flask(__name__)

messages = []  # Store chat messages

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login')
def home():
    return render_template('login.html')

@app.route('/send', methods=['POST'])
def send():
    username = request.form.get('username')
    message = request.form.get('message')
    if username and message:
        messages.append({'username': username, 'message': message, 'timestamp': time.time()})
    return '', 204  # No content response

@app.route('/messages')
def get_messages():
    return jsonify(messages)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
