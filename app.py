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

@app.route('/insertNewUser', methods = ['POST'])
def insert_new_user():
    userName = request.form['userName']
    password = request.form['Password']
    Email = request.form['Email']
    if DataRecord().check_user(userName):
        return jsonify({"Feedback":"Invalid Username,This Username had been used "}) 
    else:
        DataRecord().insert_new_user(userName,password,Email)
        return jsonify({"Feedback":"Success"})

@app.route('/password_strength', methods = ['POST'])
def password_strength_check():
    password = request.form['Password']
    score = password_strength_checker().password_check(password)
    return jsonify({"score":score})

@app.route('/access_account_detail', methods = ['POST'])
def access_account_detail():
    Username = request.form['Username']
    return jsonify({"ID":DataRecord().access_account(Username)[0],
                    "Username":DataRecord().access_account(Username)[1],
                    "Password":DataRecord().access_account(Username)[2],
                    "email":DataRecord().access_account(Username)[3]})

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
