import time
from flask import Flask, render_template, request, jsonify
from encryption_V2 import Encrytion
from DataBase import DataRecord
from password_strength import password_strength_checker
import random
import datetime
import json
from email_sender import email_send


app = Flask(__name__)


rooms = DataRecord().fetch_chat_message() if DataRecord().fetch_chat_message() else {}# Dictionary to store messages for each room


@app.route('/room/<room_code>')
def index(room_code):
    return render_template('index.html', room_code=room_code)

@app.route('/lobby')
def lobby():
    return render_template('lobby.html')

@app.route('/')
def home():
    return render_template('login.html')

@app.route('/admin')
def admin():
    return render_template('admin.html')

@app.route('/create_room', methods=['POST'])
def create_room():
    room_code = str(random.randint(10000, 99999))
    if room_code in rooms:
        return jsonify({"Feedback": "Room already exists"})
    rooms[room_code] = []  # Create a new room with an empty message list
    return jsonify({"Feedback": "Room created", "room_code": room_code})

@app.route('/join_room', methods=['POST'])
def join_room():
    room_code = request.form.get('room_code')
    if room_code in rooms:
        return jsonify({"Feedback": "Success", "room_code": room_code})
    return jsonify({"Feedback": "Room not found"})

@app.route('/send', methods=['POST'])
def send():
    username = request.form.get('username')
    message = request.form.get('message')
    room_code = request.form.get('room_code')
    User_role = request.form.get('role')
    Message_time = f'{((datetime.datetime.now()).strftime("%X"))} {((datetime.datetime.now()).strftime("%x"))}'

    if username and message and room_code in rooms:
        rooms[room_code].append({'username': username, 'message': message, 'timestamp':Message_time, 'role': User_role})

        DataRecord().store_chat_message(username,message,str(Message_time),str(room_code))
    return '', 204  # No content response

@app.route('/messages/<room_code>')
def get_messages(room_code):
    return jsonify(rooms.get(room_code, []))

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

@app.route('/CheckUserPassword',methods = ['POST'])
def Check_user_password():
    userName = request.form['userName']
    password = request.form['Password']
    if DataRecord().check_password(userName,password):
        return jsonify({"check":True})
    else:
        return jsonify({"check":False})
    


@app.route('/update_account_username',methods = ['POST'])
def update_account_username():
    id = request.form['id']
    new_username = request.form['New_username']
    DataRecord().update_account_Username(new_username,id)
    return jsonify({"Feedback":True})
    

@app.route('/password_Update',methods = ['POST'])
def update_account_password():
    id = request.form['id']
    new_password = request.form['New_password']
    DataRecord().update_account_Password(new_password,id)
    return jsonify({"Feedback":True})
    

@app.route('/update_user_setting',methods = ['POST'])
def update_user_setting():
    id = request.form['id']
    theme = request.form['theme']
    fontsize = request.form['fontSize']
    DataRecord().update_account_setting(id,theme,fontsize)
    return jsonify({"Feedback":True})

@app.route('/update_user_email',methods=['POST'])
def update_user_email():
    id = request.form["id"]
    email = request.form["email"]
    return jsonify({"Feedback":DataRecord().update_account_Email(email,id)})

@app.route('/access_user_setting',methods = ['POST'])
def access_user_setting():
    id = request.form['id']
    data = DataRecord().access_account_setting(id,False)
    if data ==  None:
        return jsonify({"Theme":None,"Fontsize":None})
    else:
        return jsonify({"Theme":data[1],"Fontsize":data[2]})


@app.route('/accessUserRole',methods = ['POST'])   
def access_user_role():
    username = request.form['userName']
    data = DataRecord().user_role(username)
    
    if data == False:
        return 404,''
    else:
        return jsonify({"role":data})

@app.route('/email_verification',methods = ['POST'])
def email_verification():
    import random
    email = request.form['Email']
    code = random.randint(10000,99999)
    Title = "email Verification"
    Body = f'{code}'
    email_send().send_email(Title,Body,email)
    return jsonify({"Code":code})


@app.route('/customSQL',methods=['POST'])
def custom_SQL():
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
