from flask import Flask, render_template, request
from flask_socketio import SocketIO, send, emit
import json
import tkinter as tk
from tkinter import messagebox

app = Flask(__name__)
socketio = SocketIO(app)

users = {}
user_data_file = 'user_data.json'

bad_word_file = open("bad_word.txt", "r")
bad_word_list = bad_word_file.read()
bad_word_list = bad_word_list.split(",")
bad_word_file.close()



def load_user_data():
    try:
        with open(user_data_file, 'r') as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}

def save_user_data(data):
    with open(user_data_file, 'w') as file:
        json.dump(data, file)

def get_user(username):
    user_data = load_user_data()
    return user_data.get(username)

def create_user(username, password):
    user_data = load_user_data()
    user_data[username] = {'password': password}
    save_user_data(user_data)

def check_credentials(username, password):
    user = get_user(username)
    if user is not None and user['password'] == password:
        return True
    return False

def check_account(username):
    user = get_user(username)
    if user is not None :
        return True
    return False

def check_bad_word(data):
    for word in bad_word_list:
        for message_word in data.split(" "):
            if word in message_word:
                return False
    return True

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('connect')
def handle_connect():
    users[request.sid] = None

@socketio.on('disconnect')
def handle_disconnect():
    if request.sid in users:
        emit('new_user_intro', {'message': f'{users[request.sid]} has left'}, broadcast=True)
        del users[request.sid]

@socketio.on('login')
def handle_login(data):
    username = data['username']
    password = data['password']
    if check_credentials(username, password):
        users[request.sid] = username
        emit('new_user_intro', {'message': f'{username} has joined'}, broadcast=True)
        emit('login_success', broadcast=False)
    else:
        emit('login_failure', broadcast=False)

@socketio.on('signup')
def handle_signup(data):
    username = data['username']
    password = data['password']
    if not check_account(username):
        create_user(username, password)
        users[request.sid] = username
    else:
        emit('repeated_sign_up_non_boardcast',broadcast=False)

@socketio.on('message')
def handle_message(data):
    if request.sid in users:
        username = users[request.sid]
        message = data['message']
        if check_bad_word(message):
            emit('new_message', {'username': username, 'message': message}, broadcast=True)
            with open("log.txt", "a", encoding='utf-8') as log_text:
                log_text.write(f'{username} : {message}\n')
        else:
            print("here")
            emit('bad_word_non_boardcast',broadcast=False)

@socketio.on('name')
def handle_name(data):
    if request.sid in users:
        users[request.sid] = data['name']
        emit('new_user_intro', {'message': f'{users[request.sid]} has joined'}, broadcast=True)

@socketio.on('change_name')
def handle_change_name(data):
    if request.sid in users:
        old_name = users[request.sid]
        new_name = data['name']
        users[request.sid] = new_name
        emit('new_user_intro', {'message': f'{old_name} changed their name to {new_name}'}, broadcast=True)

@socketio.on('change_font_size')
def handle_change_font_size(data):
    if request.sid in users:
        font_size = data['font_size']
        emit('font_size_changed', {'font_size': font_size}, broadcast=True)

if __name__ == '__main__':
    socketio.run(app, host='10.0.0.57', port=4630)
    