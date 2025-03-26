"""
Encryption module for the chat room system.
This module provides a custom encryption system with the following features:
- Double encryption for messages
- Password-based encryption
- Parallel processing for large messages
- Custom character mapping
- Key management system
"""

import random
import concurrent.futures

class Encrytion:
    """
    Custom encryption class that implements a double encryption system with password protection.
    Uses character mapping and key-based encryption for secure message transmission.
    """
    
    def __init__(self,split_amount = 6):
        """
        Initialize the encryption system.
        
        Args:
            split_amount (int): Number of characters to split messages into for parallel processing
        """
        # Define character mapping slots for encryption
        self.slots = ["abcdefghijklmnMNOPQRSTUVWXYZopqrstuvwxyzABCDEFGHIJKL!@#$%^&*()_+-=[]{|\;}:',./<>?`~1234567890 ",
                      "ABCDEFGHI@#$%^&*()_+-=[]{|\;}:',./<>?`~JKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz!1234567890 ",
                      "ABCDEFGHIJKLMNOPQRSTUVWXYZ!@#$%^&*()_+-=[]{|\;}:',./<>?`~1234567890 abcdefghijklmnopqrstuvwxyz",
                      "ABCDEFGHI@#$%^&*()_+-=[]{|\;}:',./<>?`~JKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz!1234567890 ",
                      "ABCDEFGMNOPQRSTUVWXYZabcdefghijHI@#$%^&*()_+-=[]{|\;}:',./<>?`~JKLklmnopqrstuvwxyz!1234567890 ",
                      "ABCDEFMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz!12345GHI@#$%^&*()_+-=[]{|\;}:',./<>?`~JKL67890 ",
                      "ABCDEFGHI@~JKLMNOPQRSTUVWXYZabcdefghijklmnopqrstu#$%^&*()_+-=[]{|\;}:',./<>?`vwxyz!1234567890 ",
                      "ABCDE<>?`~JKLMNOPQRSTUVWXYZabcdefghijklmnFGHI@#$%^&*()_+-=[]{|\;}:',./opqrstuvwxyz!1234567890 ",
                      "ABCDE<>?`~JKLMNOPQRSTUVWXY^&*()_+-=[]{|\;}:',./opqrstuvwxyz!1234567890 ZabcdefghijklmnFGHI@#$%",
                      "abcdefghijklmnMNOPQRSTUVFGHIJKL!@#$%^&*()_+-=[]{|\;}:',./<>?`~123456789WXYZopqrstuvwxyzABCDE0 ",
                      "abcdefghYZopqrstuvwxyzABCDEFGHIJKL!@#$%^&*()_+-=[]{|\;}:',.ijklmnMNOPQRSTUVWX/<>?`~1234567890 ",
                      "abcdefghijklmn',./<>?`~1234567890 MNOPQRSTUVWXYZopqrstuvwxyzABCDEFGHIJKL!@#$%^&*()_+-=[]{|\;}:",
                      "opqrstuvwxyzABCDEFGHIJKL!@#$%^&*()_+-=[abcdefghijklmnMNOPQRSTUVWXYZ]{|\;}:',./<>?`~1234567890 ",
                      "abcdefghijklmnMNOPQRSTUVWXYZopqrstuvwx*()_+-=[]{|\;}:',./<>yzABCDEFGHIJKL!@#$%^&?`~1234567890 ",
                      "abcdWXYZopqrstuvwxyzABCDEFGHIJKL!@#$%^&*()_+-=[]{|\;}:',./<>?`~efghijklmnMNOPQRSTUV1234567890 ",
                      ]

        self.letter = ""
        self.split_key = "~~123%67"  # Key used for splitting messages
        self.split_amount = split_amount
        self.init_key = 2  # Initial encryption key
        self.space = "   "  # Padding for message splitting

    def encrypter(self, message, password, key,init_key):
        """
        Core encryption function that encrypts a message using character mapping.
        
        Args:
            message (str): Message to encrypt
            password (str): Optional password for additional security
            key (str): Optional key for encryption
            init_key (int): Initial key for encryption
            
        Returns:
            tuple: (encrypted_message, encryption_key)
        """
        if init_key:
            slot_num = init_key
            random_number = init_key
        else:
            slot_num = random.randint(0, len(self.slots) - 1)
            random_number = random.randint(2, len(message))

        slot = self.slots[slot_num]
        
        encrypted_message = []
        counter = random_number

        # Append password and key to message if provided
        if password:
            message += self.split_key + str(password)
        if key:
            message += self.split_key + str(key)

        # Encrypt each character using character mapping
        for word in message:
            word_location = slot.find(word)
            encrypted_location = (word_location + counter) % len(slot)
            encrypted_message.append(slot[encrypted_location])
            counter *= random_number

        return ''.join(encrypted_message[::-1]), f'{random_number} {slot_num}'

    def decrypter(self, message, key ,init_key):
        """
        Core decryption function that decrypts a message using character mapping.
        
        Args:
            message (str): Message to decrypt
            key (str): Encryption key
            init_key (int): Initial key for decryption
            
        Returns:
            str: Decrypted message or None if decryption fails
        """
        decrypted_message = []
        message = message[::-1]
        if init_key  == False:
            split_key = key.split(" ")
            try:
                slot = self.slots[int(split_key[1])]
            except:
                return None
        
            counter = int(split_key[0])
            RANDOM_NUMBER = int(split_key[0])
        else:
            slot = self.slots[init_key]
            counter = init_key
            RANDOM_NUMBER = init_key

        # Decrypt each character using character mapping
        for word in message:
            word_location = slot.find(word)
            decrypted_location = (word_location - (counter % len(slot))) % len(slot)
            decrypted_message.append(slot[decrypted_location])
            counter *= RANDOM_NUMBER

        return ''.join(decrypted_message)

    def single_encryption(self, message, password):
        """
        Performs double encryption on a message.
        
        Args:
            message (str): Message to encrypt
            password (str): Password for encryption
            
        Returns:
            tuple: (encrypted_message, encryption_key)
        """
        single_encrypted_message, key = self.encrypter(message, password=None, key=None,init_key=None)
        double_encrypted_data, double_key = self.encrypter(single_encrypted_message, password, key,init_key=None)
        return double_encrypted_data, double_key

    def single_decryption(self, message, key, password):
        """
        Performs double decryption on a message.
        
        Args:
            message (str): Message to decrypt
            key (str): Encryption key
            password (str): Password for decryption
            
        Returns:
            str: Decrypted message or 405 if decryption fails
        """
        single_decrypted_message = self.decrypter(message, key,False)
        if not single_decrypted_message:
            return 405
        
        correct = self.check_password(single_decrypted_message, password)
        if not correct:
            return 405
        
        second_key = self.get_second_key(single_decrypted_message)
        single_decrypted_message = self.remove_password(single_decrypted_message)
        
        return self.decrypter(single_decrypted_message, second_key,False)

    def check_password(self, message, password):
        """
        Verifies if the password in the message matches the provided password.
        
        Args:
            message (str): Message containing password
            password (str): Password to verify
            
        Returns:
            bool: True if password matches, False otherwise
        """
        parts = message.split(self.split_key)
        try:
            return parts[-2] == password
        except IndexError:
            return False

    def get_second_key(self, message):
        """
        Extracts the second encryption key from a message.
        
        Args:
            message (str): Message containing key
            
        Returns:
            str: Second encryption key
        """
        return message.split(self.split_key)[-1]

    def remove_password(self, message):
        """
        Removes password and key from a message.
        
        Args:
            message (str): Message to clean
            
        Returns:
            str: Message without password and key
        """
        return message.split(self.split_key)[0]

    def split_plain_text(self, message):
        """
        Splits a message into chunks for parallel processing.
        
        Args:
            message (str): Message to split
            
        Returns:
            list: List of message chunks
        """
        new_message = []
        
        if len(message) % self.split_amount != 0:  # Only pad if necessary
            padding_needed = self.split_amount - (len(message) % self.split_amount)
            message += " " * padding_needed  # Add the correct number of spaces

        for i in range((len(message) // self.split_amount)):
            new_message.append(message[self.split_amount * i:(self.split_amount * (i + 1))])

        return new_message

    def merge_cipher(self,message):
        """
        Merges encrypted message chunks.
        
        Args:
            message (list): List of encrypted chunks
            
        Returns:
            str: Merged encrypted message
        """
        cipher_text = ""
        for i in message:
            cipher_text += i[0]+self.split_key
        return cipher_text

    def split_cipher_text(self,text):
        """
        Splits cipher text into chunks.
        
        Args:
            text (str): Cipher text to split
            
        Returns:
            list or bool: List of chunks or False if splitting fails
        """
        if self.split_key in text:
            return text.split(self.split_key)
        else:
            return False

    def encrypt_key(self,message):
        """
        Encrypts the encryption keys.
        
        Args:
            message (list): List of encryption keys
            
        Returns:
            str: Encrypted keys
        """
        key = ""
        counter = 0
        message_length = 0
        for i in message:
            message_length +=1

        for i in message:
            if counter < message_length-1:
                key += i[1]+self.split_key
            else:
                key+=i[1]
            counter += 1
        key_list = self.split_plain_text(key)
        init_key_list = [self.init_key for i in range((len(key)//self.split_amount)+1)]
        default_key_list = [False for i in range((len(key)//self.split_amount)+1)]
        with concurrent.futures.ThreadPoolExecutor() as executor:
            Encrypted_list=list(executor.map(self.encrypter,key_list,default_key_list,default_key_list,init_key_list))
        return self.merge_cipher(Encrypted_list)

    def decrypt_key(self,cipher_key):
        """
        Decrypts the encryption keys.
        
        Args:
            cipher_key (str): Encrypted keys
            
        Returns:
            list: List of decrypted keys
        """
        cipher_key_list = self.split_cipher_text(cipher_key)
        init_key_list = [self.init_key for i in range((len(cipher_key)//self.split_amount)+1)]
        default_key_list = [False for i in range((len(cipher_key)//self.split_amount)+1)]
        with concurrent.futures.ThreadPoolExecutor() as executor:
            Encrypted_list=list(executor.map(self.decrypter,cipher_key_list,default_key_list,init_key_list))
        return (("".join(Encrypted_list)).split(self.split_key))

    def hashing(self,data):
        """
        Creates a hash of data using the encryption system.
        
        Args:
            data (str): Data to hash
            
        Returns:
            str: Hashed data
        """
        return self.encrypter(data,False,False,self.init_key)[0]
    
    def unhashing(self,data):
        """
        Reverses a hash using the encryption system.
        
        Args:
            data (str): Hashed data
            
        Returns:
            str: Unhashed data
        """
        return self.decrypter(data,False,self.init_key)

    def encryption(self,message, password):
        """
        Main encryption function that handles both short and long messages.
        
        Args:
            message (str): Message to encrypt
            password (str): Password for encryption
            
        Returns:
            tuple: (encrypted_message, encryption_key)
        """
        if len(message)<self.split_amount:
            return self.single_encryption(message,password)
        else:
            message_list = self.split_plain_text(message)
            password_list = [password for i in range((len(message)//self.split_amount)+1)]
            with concurrent.futures.ThreadPoolExecutor() as executor:
                Encrypted_list=list(executor.map(self.single_encryption, message_list,password_list))
            return self.merge_cipher(Encrypted_list),self.encrypt_key(Encrypted_list)
    
    def unencryption(self,message, key, password):
        """
        Main decryption function that handles both short and long messages.
        
        Args:
            message (str): Message to decrypt
            key (str): Encryption key
            password (str): Password for decryption
            
        Returns:
            str: Decrypted message or error message if decryption fails
        """
        if self.split_cipher_text(message) == False:
            return self.single_decryption(message, key, password)
        else:
            cipher_text_list = self.split_cipher_text(message)
            key_list = self.decrypt_key(key)
            password_list = [password for i in range((len(message)//self.split_amount)+1)]
            with concurrent.futures.ThreadPoolExecutor() as executor:
               plain_text_list=list(executor.map(self.single_decryption, cipher_text_list,key_list,password_list))
            try:
               plain_text = "".join(plain_text_list)
               plain_text = list(plain_text)[:-(len(self.space)-1)]
               return "".join(plain_text)
            except:
                print(key_list)
                print((cipher_text_list))
                print(len(cipher_text_list),len(key_list))
                return "Invalid Password,unable to decrypte"

'''
plain_text = "1122334455667788990qwe00qwe"
print(len(plain_text))
text,key = Encrytion().encryption(plain_text,"12")
print(f'text: {text},\nkey: {key}')

PT = Encrytion().unencryption(text,key,"12")
print(PT)
print(plain_text)
print(len(PT))
'''