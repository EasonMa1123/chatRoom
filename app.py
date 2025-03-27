"""
Main Flask application for the chat room system.
This file handles all the routing and core functionality of the chat application.
"""

import time
from flask import Flask, render_template, request, jsonify
from encryption_V2 import Encrytion
from DataBase import DataRecord
import random
import datetime
import json
from email_sender import email_send

# Initialize Flask application
app = Flask(__name__)

# Dictionary to store chat messages for each room in memory
rooms = {}  

def decrypt_messages(messages, room_code):
    """
    Decrypts a list of messages for a specific room.
    
    Args:
        messages (list): List of encrypted messages
        room_code (str): The room code used for decryption
        
    Returns:
        list: List of decrypted messages
    """
    decrypted_messages = []
    for msg in messages:
        try:
            decrypted_message = Encrytion().unencryption(msg['message'], msg['messagekey'], str(room_code))

            if decrypted_message != "Invalid Password,unable to decrypte":
                msg['message'] = decrypted_message
                decrypted_messages.append(msg)
        except:
            continue
    return decrypted_messages

# Route handlers for different pages
@app.route('/room/<room_code>')
def index(room_code):
    """Renders the chat room page for a specific room code."""
    return render_template('index.html', room_code=room_code)

@app.route('/lobby')
def lobby():
    """Renders the lobby page where users can join or create rooms."""
    return render_template('lobby.html')

@app.route('/')
def home():
    """Renders the login page."""
    return render_template('login.html')

@app.route('/admin')
def admin():
    """Renders the admin dashboard page."""
    return render_template('admin.html')

@app.route('/setting')
def setting():
    """Renders the user settings page."""
    return render_template('setting.html')

# API endpoints for room management
@app.route('/create_room', methods=['POST'])
def create_room():
    """
    Creates a new chat room.
    
    Expected form data:
    - admin: The admin username
    - password: Room password
    
    Returns:
        JSON response with room code and status
    """
    admin = request.form.get('admin')
    password = request.form.get('password')
    room_code = str(random.randint(10000, 99999))
    if room_code in rooms:
        return jsonify({"Feedback": "Room already exists"})
    DataRecord().room_registration(int(room_code),admin,password)
    rooms[room_code] = []  # Create a new room with an empty message list
    return jsonify({"Feedback": "Room created", "room_code": room_code})

@app.route('/join_room', methods=['POST'])
def join_room():
    """
    Handles room joining requests.
    
    Expected form data:
    - room_code: The room code to join
    
    Returns:
        JSON response with room data and status
    """
    room_code = request.form.get('room_code')
    data = DataRecord().fetch_room_data(room_code)
    
    if int(room_code) in data['id']:
        data.update({"Feedback": "Success", "room_code": room_code})
        return jsonify(data)
    return jsonify({"Feedback": "Room not found"})

@app.route('/room_list')
def chat_room_list():
    """Returns a list of all available chat rooms."""
    rooms_code = DataRecord().fetch_chat_message()
    return jsonify([key for key in rooms_code])

# Message handling endpoints
@app.route('/send', methods=['POST'])
def send():
    """
    Handles sending messages in a chat room.
    
    Expected form data:
    - username: Sender's username
    - message: Message content
    - room_code: Target room code
    - role: User's role
    
    Returns:
        Empty response with 204 status code
    """
    username = request.form.get('username')
    message = request.form.get('message')
    room_code = request.form.get('room_code')
    User_role = request.form.get('role')
    Message_time = f'{((datetime.datetime.now()).strftime("%X"))} {((datetime.datetime.now()).strftime("%x"))}'
    encrypted_message,key = Encrytion().encryption(message,str(room_code))
    if username and message and room_code in rooms:
        # Store encrypted message in database
        DataRecord().store_chat_message(username,encrypted_message,str(key),str(Message_time),str(room_code))
        
        # Decrypt message for display in rooms dictionary
        decrypted_message = Encrytion().unencryption(encrypted_message, str(key), str(room_code))
        if decrypted_message != "Invalid Password,unable to decrypte":
            rooms[room_code].append({
                'username': username, 
                'message': decrypted_message, 
                "MessageKey": key,
                'timestamp': Message_time, 
                'role': User_role
            })
    return '', 204  # No content response

@app.route('/messages/<room_code>')
def get_messages(room_code):
    """
    Retrieves messages for a specific room.
    
    Args:
        room_code (str): The room code to fetch messages for
        
    Returns:
        JSON response with room messages
    """
    if room_code not in rooms:
        # Fetch messages from database if not in memory
        messages = DataRecord().fetch_chat_message()
        if messages and room_code in messages:
            rooms[room_code] = decrypt_messages(messages[room_code], room_code)

    return jsonify(rooms.get(room_code, []))

# User management endpoints
@app.route('/insertNewUser', methods = ['POST'])
def insert_new_user():
    """
    Handles new user registration.
    
    Expected form data:
    - userName: New username
    - Password: User password
    - Email: User email
    
    Returns:
        JSON response with registration status
    """
    userName = request.form['userName']
    password = request.form['Password']
    Email = request.form['Email']
    if DataRecord().check_user(userName):
        return jsonify({"Feedback":"Invalid Username,This Username had been used "}) 
    else:
        DataRecord().insert_new_user(userName,password,Email)
        return jsonify({"Feedback":"Success"})



@app.route('/access_account_detail', methods = ['POST'])
def access_account_detail():
    """
    Retrieves account details for a user.
    
    Expected form data:
    - Username: Username to look up
    
    Returns:
        JSON response with user account details
    """
    Username = request.form['Username']
    return jsonify({"ID":DataRecord().access_account(Username)[0],
                    "Username":DataRecord().access_account(Username)[1],
                    "Password":DataRecord().access_account(Username)[2],
                    "email":DataRecord().access_account(Username)[3]})

@app.route('/CheckUserPassword',methods = ['POST'])
def Check_user_password():
    """
    Verifies a user's password.
    
    Expected form data:
    - userName: Username to check
    - Password: Password to verify
    
    Returns:
        JSON response with verification status
    """
    userName = request.form['userName']
    password = request.form['Password']
    if DataRecord().check_password(userName,password):
        return jsonify({"check":True})
    else:
        return jsonify({"check":False})

# Account update endpoints
@app.route('/update_account_username',methods = ['POST'])
def update_account_username():
    """
    Updates a user's username.
    
    Expected form data:
    - id: User ID
    - New_username: New username
    
    Returns:
        JSON response with update status
    """
    id = request.form['id']
    new_username = request.form['New_username']
    DataRecord().update_account_Username(new_username,id)
    return jsonify({"Feedback":True})

@app.route('/password_Update',methods = ['POST'])
def update_account_password():
    """
    Updates a user's password.
    
    Expected form data:
    - id: User ID
    - New_password: New password
    
    Returns:
        JSON response with update status
    """
    id = request.form['id']
    new_password = request.form['New_password']
    DataRecord().update_account_Password(new_password,id)
    return jsonify({"Feedback":True})

@app.route('/update_user_setting',methods = ['POST'])
def update_user_setting():
    """
    Updates user interface settings.
    
    Expected form data:
    - id: User ID
    - theme: UI theme
    - fontSize: Font size preference
    
    Returns:
        JSON response with update status
    """
    id = request.form['id']
    theme = request.form['theme']
    fontsize = request.form['fontSize']
    DataRecord().update_account_setting(id,theme,fontsize)
    return jsonify({"Feedback":True})

@app.route('/update_user_email',methods=['POST'])
def update_user_email():
    """
    Updates a user's email address.
    
    Expected form data:
    - id: User ID
    - email: New email address
    
    Returns:
        JSON response with update status
    """
    id = request.form["id"]
    email = request.form["email"]
    return jsonify({"Feedback":DataRecord().update_account_Email(email,id)})

@app.route('/access_user_setting',methods = ['POST'])
def access_user_setting():
    """
    Retrieves user interface settings.
    
    Expected form data:
    - id: User ID
    
    Returns:
        JSON response with user settings
    """
    id = request.form['id']
    data = DataRecord().access_account_setting(id,False)
    if data ==  None:
        return jsonify({"Theme":None,"Fontsize":None})
    else:
        return jsonify({"Theme":data[0]["Theme"],"Fontsize":data[0]["FontSize"]})

@app.route('/accessUserRole',methods = ['POST'])   
def access_user_role():
    """
    Retrieves a user's role.
    
    Expected form data:
    - userName: Username to check
    
    Returns:
        JSON response with user role
    """
    username = request.form['userName']
    data = DataRecord().user_role(username)
    
    if data == False:
        return 404,''
    else:
        return jsonify({"role":data})

@app.route('/email_verification',methods = ['POST'])
def email_verification():
    """
    Sends email verification code.
    
    Expected form data:
    - Email: User's email address
    
    Returns:
        JSON response with verification code
    """
    import random
    email = request.form['Email']
    code = random.randint(10000,99999)
    Title = "email Verification"
    Body = f'{code}'
    email_send().send_email(Title,Body,email)
    return jsonify({"Code":code})

# Admin functionality endpoints
@app.route('/customSQL',methods=['POST'])
def custom_SQL():
    """
    Executes custom SQL queries (admin only).
    
    Expected form data:
    - userName: Admin username
    - field: Fields to select
    - table: Target table
    - con_field: Condition field
    - param: Query parameters
    - join_toggle: Whether to use JOIN
    - join_table: Table to join with
    - match_field: Field to match on
    - join_field: Field to join on
    
    Returns:
        JSON response with query results
    """
    username = request.form['userName']
    role = DataRecord().user_role(username)
    if role == "admin":
        field_name = request.form['field']
        table = request.form['table']
        con_field = request.form['con_field']
        try:
            if con_field.lower() != "id":
                param = str(request.form['param'])
                param = tuple(param.split(",")) if param!= "" else None
            else: 
                param = int(request.form['param'])
                param = (param,)if param!= "" else None
        except:
            return jsonify({"log":"Error executing query : Invilad Parameter request"})

        sql = f'SELECT {field_name} FROM {table}'

        join_command = request.form['join_toggle']
        join_table = request.form['join_table']
        match_field = request.form['match_field']
        join_field = request.form['join_field']

        if join_command.lower() == "true":
            sql += f' JOIN {join_table} ON {table}.{match_field} = {join_table}.{join_field}'
        if con_field != "None":
            sql += f' WHERE {table}.{con_field} = %s'
        data = DataRecord().execute_custom_query(sql,param)
        return jsonify({"log":str(data)})
    else:
        return jsonify({"log":"Error executing query : Not admin"})

@app.route('/showdb')
def showtable():
    """
    Shows all database tables (admin only).
    
    Returns:
        JSON response with list of tables
    """
    sql = f'SHOW tables'
    data = DataRecord().execute_custom_query(sql)
    data = [{value if isinstance(value, str) else value for key, value in row.items()} for row in data]
    table = []
    field_data = {}
    for i in data:
        for j in i:
           table.append(j) 
           sql = f'SHOW COLUMNS FROM {j} '
           field = DataRecord().execute_custom_query(sql)
           temp = []
           for l in field:
              temp.append(str(l['Field']))
           field_data[str(j)] = temp

    return jsonify({"table":",".join(table),"field":str(json.dumps(field_data))})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
