import pymysql
from encryption_V2 import Encrytion as ENC

class DataRecord:
    def __init__(self):
        timeout = 10
        # Connect to the MySQL database
        self.DataBase =  pymysql.connect(
            charset="utf8mb4",
            connect_timeout=timeout,
            cursorclass=pymysql.cursors.DictCursor,
            db="defaultdb",
            host="mysql-234bcdc-chatroom123.b.aivencloud.com",
            password="AVNS_C_JQYU9Uj9LYnRP69lt",
            read_timeout=timeout,
            port=21035,
            user="avnadmin",
            write_timeout=timeout,
            )
        self.cc = self.DataBase.cursor()
        # Create tables if they don't exist
        self.cc.execute("""
            CREATE TABLE IF NOT EXISTS UserData (
                id INT AUTO_INCREMENT PRIMARY KEY,
                UserName TEXT,
                Password TEXT,
                Email TEXT,
                Role TEXT
            )
        """)
        self.DataBase.commit()

        self.cc.execute("""
            CREATE TABLE IF NOT EXISTS UserSettingData (
                id INT PRIMARY KEY,
                Theme TEXT,
                FontSize TEXT
            )
        """)
        self.DataBase.commit()

        self.cc.execute("""
            CREATE TABLE IF NOT EXISTS ChatRoomMessage (
                id INT AUTO_INCREMENT PRIMARY KEY,
                username TEXT,
                Message TEXT,
                MessageKey TEXT,
                timestamp TEXT,
                roomCode INT
            )
        """)
        self.DataBase.commit()

        self.cc.execute("""
            CREATE TABLE IF NOT EXISTS ChatRoom (
                id INT PRIMARY KEY,
                roomAdmin TEXT,
                roomPassword TEXT
            )
        """)
        self.DataBase.commit()

    def check_user(self, user):
        self.cc.execute("SELECT UserName FROM UserData")
        user_in_DataBase = [row['UserName'] for row in self.cc.fetchall()]
        return self.encrypting_data(user) in user_in_DataBase

    def insert_new_user(self, user, password, email):
        encrypted_user = self.encrypting_data(user)
        encrypted_password = self.encrypting_data(password)
        encrypted_email = self.encrypting_data(email)
        role = self.encrypting_data("normal user")
        self.cc.execute("""
            INSERT INTO UserData (UserName, Password, Email,Role) 
            VALUES (%s, %s, %s,%s)
        """, (encrypted_user, encrypted_password, encrypted_email,role))
        self.DataBase.commit()
    
    def check_password(self, user, password):
        encrypted_user = self.encrypting_data(user)
        self.cc.execute("SELECT Password FROM UserData WHERE UserName = %s", (encrypted_user,))
        password_in_db = [row['Password'] for row in self.cc.fetchall()]
        return self.encrypting_data(password) in password_in_db

    def access_account(self, user):
        encrypted_user = self.encrypting_data(user)
        self.cc.execute("SELECT * FROM UserData WHERE UserName = %s", (encrypted_user,))
        data = self.cc.fetchone()
        return [data['id'], self.unencrypting_data(data['UserName']), self.unencrypting_data(data['Password']), self.unencrypting_data(data['Email'])] if data else None
    
    def update_account_Username(self, new_username, user_id):
        self.cc.execute("UPDATE UserData SET UserName = %s WHERE id = %s", (self.encrypting_data(new_username), user_id))
        self.DataBase.commit()

    def update_account_Password(self, new_password, user_id):
        self.cc.execute("UPDATE UserData SET Password = %s WHERE id = %s", (self.encrypting_data(new_password), user_id))
        self.DataBase.commit()

    def update_account_Email(self, new_email, user_id):
        try:
            self.cc.execute("UPDATE UserData SET Email = %s WHERE id = %s", (self.encrypting_data(new_email), user_id))
            self.DataBase.commit()
            return True
        except:
            return False

    def update_account_setting(self, user_id, theme, font_size):
        if self.access_account_setting(user_id, True):
            self.cc.execute("""
                UPDATE UserSettingData SET Theme = %s, FontSize = %s WHERE id = %s
            """, (self.encrypting_data(theme), self.encrypting_data(font_size), user_id))
        else:
            self.cc.execute("""
                INSERT INTO UserSettingData (id, Theme, FontSize) VALUES (%s, %s, %s)
            """, (user_id, self.encrypting_data(theme), self.encrypting_data(font_size)))
        self.DataBase.commit()

    def access_account_setting(self, user_id, check):
        self.cc.execute("SELECT * FROM UserSettingData WHERE id = %s", (user_id,))
        data = self.cc.fetchall()
        if check:
            return data if data else []
        return [{key: self.unencrypting_data(value) if isinstance(value, str) else value for key, value in row.items()} for row in data] if data else None

    def user_role(self,UserName:str):
        try:
            self.cc.execute("SELECT Role FROM UserData WHERE UserName = %s", (self.encrypting_data(UserName)))
            data = self.cc.fetchall()
            return list({key: [self.unencrypting_data(item[key]) for item in data] for key in data[0] if key != 'id' and key != 'roomCode'  }.values())[0][0]
        except:
            return False

    def room_registration(self,room_code,admin,password):
        self.cc.execute("""
                INSERT INTO ChatRoom (id,roomAdmin,roomPassword) VALUES (%s, %s, %s)
            """, (room_code,self.encrypting_data(admin),self.encrypting_data(password)))
        self.DataBase.commit()

    def fetch_room_data(self,room_code):
        self.cc.execute("""SELECT * FROM ChatRoom WHERE id= %s""",room_code)

        data = self.cc.fetchall()
        if data != ():
            return {
                key: [self.unencrypting_data(item[key]) for item in data] if key != 'id' and key != 'roomCode'  
                else [item[key] for item in data] 
                for key in data[0]}
        else:
            return False

    def store_chat_message(self,username,time,message,messageKey,chatroomID):
        self.cc.execute("""
                INSERT INTO ChatRoomMessage (username,Message,MessageKey,timestamp,roomCode) VALUES (%s, %s, %s, %s,%s)
            """, (self.encrypting_data(username),self.encrypting_data(time),self.encrypting_data(message),self.encrypting_data(messageKey),int(chatroomID)))
        self.DataBase.commit()


    def fetch_chat_message(self):
        self.cc.execute(""" SELECT ChatRoomMessage.username,ChatRoomMessage.MessageKey,UserData.role,ChatRoomMessage.Message,ChatRoomMessage.timestamp,ChatRoomMessage.roomCode FROM ChatRoomMessage JOIN UserData ON ChatRoomMessage.username = UserData.username
        """)
        data = self.cc.fetchall()
        if data != ():
            return self.transform_data({key: [self.unencrypting_data(item[key]) if key !='roomCode' else str(item[key]) for item in data] for key in data[0] if key != 'id'   })
        else:
            return False
    def encrypting_data(self, data):
        return ENC().hashing(data)
        
    def unencrypting_data(self, data):
        return ENC().unhashing(data)


    def display_db(self):
        self.cc.execute("SELECT * FROM UserData")
        data = self.cc.fetchall()
        return {key: [self.unencrypting_data(item[key]) for item in data] for key in data[0] if key != 'id' and key != 'roomCode'  }

    def execute_custom_query(self, query, params=None):
        try:
            # Encrypt only string parameters
            encrypted_params = tuple(self.encrypting_data(p) if isinstance(p, str) else p for p in (params or ()))

            self.cc.execute(query, encrypted_params)
            if query.strip().lower().startswith("select"):
                data = self.cc.fetchall()
                # Decrypt results if needed
                return [{key: self.unencrypting_data(value) if isinstance(value, str) else value for key, value in row.items()} for row in data]
            elif query.strip().lower().startswith("show"):
                data = self.cc.fetchall()
                return data
            else:
                self.DataBase.commit()
                return True
        except Exception as e:
            return f"Error executing query: {str(e)}"


    def transform_data(self,data):
        transformed_data = {}
        keys = list(data.keys())
        num_entries = len(data[keys[0]])
        
        for i in range(num_entries):
            entry = {}
            for key in keys:
                if key == 'roomCode':
                    room_code = data[key][i]
                else:
                    entry[key.lower()] = data[key][i]
            
            if room_code not in transformed_data:
                transformed_data[room_code] = []
            
            transformed_data[room_code].append(entry)
        
        return transformed_data


