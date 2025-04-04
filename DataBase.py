"""
Database management module for the chat room system.
This module handles all database operations including user management, chat room management,
and message storage with encryption support.
"""

import pymysql
from ExponEncryption import Encrytion

class DataRecord:
    """
    Database management class that handles all database operations.
    Includes methods for user management, chat room management, and message handling.
    All sensitive data is encrypted before storage and decrypted when retrieved.
    """
    
    def __init__(self):
        """
        Initialize database connection and create necessary tables if they don't exist.
        Sets up tables for:
        - UserData: Stores user information
        - UserSettingData: Stores user preferences
        - ChatRoomMessage: Stores chat messages
        - ChatRoom: Stores chat room information
        - UserRoomBan: Stores Banned user 
        """
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


        self.cc.execute("""
            CREATE TABLE IF NOT EXISTS UserRoomBan (
                id INT PRIMARY KEY,
                room TEXT,
                Username TEXT
            )
        """)
        self.DataBase.commit()

    def check_user(self, user):
        """
        Check if a username already exists in the database.
        
        Args:
            user (str): Username to check
            
        Returns:
            bool: True if username exists, False otherwise
        """
        self.cc.execute("SELECT UserName FROM UserData")
        user_in_DataBase = [row['UserName'] for row in self.cc.fetchall()]
        return self.encrypting_data(user) in user_in_DataBase

    def insert_new_user(self, user, password, email):
        """
        Insert a new user into the database.
        
        Args:
            user (str): Username
            password (str): User password
            email (str): User email
        """
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
        """
        Verify a user's password.
        
        Args:
            user (str): Username
            password (str): Password to verify
            
        Returns:
            bool: True if password matches, False otherwise
        """
        encrypted_user = self.encrypting_data(user)
        self.cc.execute("SELECT Password FROM UserData WHERE UserName = %s", (encrypted_user,))
        password_in_db = [row['Password'] for row in self.cc.fetchall()]
        return self.encrypting_data(password) in password_in_db

    def access_account(self, user):
        """
        Retrieve all account information for a user.
        
        Args:
            user (str): Username to look up
            
        Returns:
            list: [id, username, password, email] or None if user not found
        """
        encrypted_user = self.encrypting_data(user)
        self.cc.execute("SELECT * FROM UserData WHERE UserName = %s", (encrypted_user,))
        data = self.cc.fetchone()
        return [data['id'], self.unencrypting_data(data['UserName']), self.unencrypting_data(data['Password']), self.unencrypting_data(data['Email'])] if data else None
    
    def update_account_Username(self, new_username, user_id):
        """
        Update a user's username.
        
        Args:
            new_username (str): New username
            user_id (int): User's ID
        """
        self.cc.execute("UPDATE UserData SET UserName = %s WHERE id = %s", (self.encrypting_data(new_username), user_id))
        self.DataBase.commit()

    def update_account_Password(self, new_password, user_id):
        """
        Update a user's password.
        
        Args:
            new_password (str): New password
            user_id (int): User's ID
        """
        self.cc.execute("UPDATE UserData SET Password = %s WHERE id = %s", (self.encrypting_data(new_password), user_id))
        self.DataBase.commit()

    def update_account_Email(self, new_email, user_id):
        """
        Update a user's email address.
        
        Args:
            new_email (str): New email address
            user_id (int): User's ID
            
        Returns:
            bool: True if update successful, False otherwise
        """
        try:
            self.cc.execute("UPDATE UserData SET Email = %s WHERE id = %s", (self.encrypting_data(new_email), user_id))
            self.DataBase.commit()
            return True
        except:
            return False

    def update_account_setting(self, user_id, theme, font_size):
        """
        Update a user's interface settings.
        
        Args:
            user_id (int): User's ID
            theme (str): UI theme preference
            font_size (str): Font size preference
        """
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
        """
        Retrieve a user's interface settings.
        
        Args:
            user_id (int): User's ID
            check (bool): If True, return raw data; if False, return decrypted data
            
        Returns:
            list or dict: User settings data
        """
        self.cc.execute("SELECT * FROM UserSettingData WHERE id = %s", (user_id,))
        data = self.cc.fetchall()
        if check:
            return data if data else []
        return [{key: self.unencrypting_data(value) if isinstance(value, str) else value for key, value in row.items()} for row in data] if data else None

    def user_role(self,UserName:str):
        """
        Get a user's role.
        
        Args:
            UserName (str): Username to check
            
        Returns:
            str: User's role or False if user not found
        """
        try:
            self.cc.execute("SELECT Role FROM UserData WHERE UserName = %s", (self.encrypting_data(UserName)))
            data = self.cc.fetchall()
            return list({key: [self.unencrypting_data(item[key]) for item in data] for key in data[0] if key != 'id' and key != 'roomCode'  }.values())[0][0]
        except:
            return False

    def room_registration(self,room_code,admin,password):
        """
        Register a new chat room.
        
        Args:
            room_code (int): Unique room code
            admin (str): Admin username
            password (str): Room password
        """
        self.cc.execute("""
                INSERT INTO ChatRoom (id,roomAdmin,roomPassword) VALUES (%s, %s, %s)
            """, (room_code,self.encrypting_data(admin),self.encrypting_data(password)))
        self.DataBase.commit()

    def fetch_room_data(self,room_code):
        """
        Retrieve data for a specific chat room.
        
        Args:
            room_code (int): Room code to look up
            
        Returns:
            dict: Room data or False if room not found
        """
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
        """
        Store a new chat message.
        
        Args:
            username (str): Sender's username
            time (str): Message timestamp
            message (str): Message content
            messageKey (str): Encryption key for the message
            chatroomID (int): Room code
        """
        self.cc.execute("""
                INSERT INTO ChatRoomMessage (username,Message,MessageKey,timestamp,roomCode) VALUES (%s, %s, %s, %s,%s)
            """, (self.encrypting_data(username),self.encrypting_data(time),self.encrypting_data(message),self.encrypting_data(messageKey),int(chatroomID)))
        self.DataBase.commit()

    def fetch_chat_message(self):
        """
        Retrieve all chat messages with user roles.
        
        Returns:
            dict: Messages organized by room code or False if no messages exist
        """
        self.cc.execute(""" SELECT ChatRoomMessage.username,ChatRoomMessage.MessageKey,UserData.role,ChatRoomMessage.Message,ChatRoomMessage.timestamp,ChatRoomMessage.roomCode FROM ChatRoomMessage JOIN UserData ON ChatRoomMessage.username = UserData.username
        """)
        data = self.cc.fetchall()
        if data != ():
            return self.transform_data({key: [self.unencrypting_data(item[key]) if key !='roomCode' else str(item[key]) for item in data] for key in data[0] if key != 'id'   })
        else:
            return False

    def encrypting_data(self, data):
        """
        Encrypt data before storage.
        
        Args:
            data (str): Data to encrypt
            
        Returns:
            str: Encrypted data
        """
        return Encrytion().hashing(data)
        
    def unencrypting_data(self, data):
        """
        Decrypt stored data.
        
        Args:
            data (str): Data to decrypt
            
        Returns:
            str: Decrypted data
        """
        return Encrytion().unhashing(data)

    def display_db(self):
        """
        Display all user data (for debugging purposes).
        
        Returns:
            dict: All user data
        """
        self.cc.execute("SELECT * FROM UserData")
        data = self.cc.fetchall()
        return {key: [self.unencrypting_data(item[key]) for item in data] for key in data[0] if key != 'id' and key != 'roomCode'  }

    def execute_custom_query(self, query, params=None):
        """
        Execute a custom SQL query with optional parameters.
        
        Args:
            query (str): SQL query to execute
            params (tuple): Optional query parameters
            
        Returns:
            dict or bool: Query results or True for non-SELECT queries
        """
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
        
    def appear_ban_user(self,username,room):

        """
        Add banned user to the table
        """
        self.cc.execute("""
                INSERT INTO UserRoomBan (room,Username) VALUES (%s, %s)
            """, (self.encrypting_data(username),self.encrypting_data(room),self.encrypting_data(username))
            )
        self.DataBase.commit()



    def transform_data(self,data):
        """
        Transform flat data structure into room-based message structure.
        
        Args:
            data (dict): Flat data structure
            
        Returns:
            dict: Messages organized by room code
        """
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


