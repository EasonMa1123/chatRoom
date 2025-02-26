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
            """, (theme, font_size, user_id))
        else:
            self.cc.execute("""
                INSERT INTO UserSettingData (id, Theme, FontSize) VALUES (%s, %s, %s)
            """, (user_id, theme, font_size))
        self.DataBase.commit()

    def access_account_setting(self, user_id, check):
        self.cc.execute("SELECT * FROM UserSettingData WHERE id = %s", (user_id,))
        data = self.cc.fetchone()
        if check:
            return data if data else []
        return list(data.values()) if data else None

    def encrypting_data(self, data):
        return ENC().hashing(data)
        
    def unencrypting_data(self, data):
        return ENC().unhashing(data)


    def display_db(self):
        self.cc.execute("SELECT * FROM UserData")
        data = self.cc.fetchall()
        return {key: [self.unencrypting_data(item[key]) for item in data] for key in data[0] if key != 'id'}

    def execute_custom_query(self, query, params=None):
        try:
            self.cc.execute(query, params or ())
            if query.strip().lower().startswith("select"):
                return self.cc.fetchall()  # Return result for SELECT queries
            else:
                self.DataBase.commit()  # Commit changes for INSERT, UPDATE, DELETE
                return True
        except Exception as e:
            return f"Error executing query: {str(e)}"



print(DataRecord().display_db())
  
