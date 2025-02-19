from flask import Flask, render_template, request, jsonify
import time
from flask import Flask, render_template, request, jsonify
from encryption_V2 import Encrytion
from DataBase import DataRecord
from password_strength import password_strength_checker



from email_sender import email_send



app = Flask(__name__)

messages = []  # Store chat messages

@app.route('/index')
def index():
    return render_template('index.html')


@app.route('/lobby')
def lobby():
    return render_template('lobby.html')


@app.route('/')
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

    
@app.route('/email_verification',methods = ['POST'])
def email_verification():
    import random
    email = request.form['Email']
    code = random.randint(10000,99999)
    Title = "email Verification"
    Body = f'{code}'
    email_send().send_email(Title,Body,email)
    return jsonify({"Code":code})

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
