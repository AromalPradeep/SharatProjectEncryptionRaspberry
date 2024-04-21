from md5hash import md5
from PIL import Image
import speech_recognition as speech
import subprocess
import hashlib

import services.fileServices as clean

def generate_key(mail, key):
    """Generates a more complex key based on input mail and key."""
    derived_key = ''.join(str(ord(c) % 100) for c in mail)
    derived_key = str(int(derived_key) - int(key))
    derived_key += str(9872 - len(derived_key))
    return derived_key

def key_wise(key):
    # Ensure key is a string, strip newlines and whitespace.
    if isinstance(key, bytes):
        key = key.decode('utf-8').strip()
    else:
        key = key.strip()

    # Process string input for hash computation.
    try:
        # Encode the string to bytes, then compute MD5 hash, extract digits, and compute numeric key.
        numerical_key = ''.join([i for i in hashlib.md5(key.encode()).hexdigest() if i.isdigit()][:8])
        return int(numerical_key) % 253 + 1

    except Exception as e:
        print(f"Error in key conversion: {e}")
        return 1
    
def encrypt(mail, key, path):
    path = clean.clean_path(path)
    key = key_wise(key)
    try:
        with open(path, 'rb') as file:
            data = bytearray(file.read())

        # Apply XOR encryption
        data = bytearray(value ^ key for value in data)

        # Generate a key string and get its length
        key_str = generate_key(mail, key)
        key_str_length = len(key_str)

        # Append the key and its length
        data.extend(key_str.encode('utf-8'))
        data.extend(key_str_length.to_bytes(4, 'big'))  # Store length as 4 bytes

        with open(path, 'wb') as file:
            file.write(data)
    except Exception as e:
        print(f"Encryption failed: {e}")
        return False
    return True


def decrypt(mail, key, path):
    path = clean.clean_path(path)
    key = key_wise(key)
    try:
        with open(path, 'rb') as file:
            data = bytearray(file.read())

        # Extract the length of the key string
        key_str_length = int.from_bytes(data[-4:], 'big')
        key_str = data[-4 - key_str_length:-4].decode('utf-8')

        # Verify key
        expected_key_str = generate_key(mail, key)
        if key_str != expected_key_str:
            print("Key mismatch or file corruption.")
            return False

        # Remove the key string and its length
        data = data[:-4 - key_str_length]

        # Apply XOR decryption
        decrypted_data = bytearray(value ^ key for value in data)

        with open(path, 'wb') as file:
            file.write(decrypted_data)
        
        return True
    except Exception as e:
        print(f"Decryption failed: {e}")
        return False

    
def voice(self):
    
    self.shint = ''
    
    # voice recognizer object
    voice = speech.Recognizer()
    
    # use microphone
    with speech.Microphone() as source:
        voice_command = voice.listen(source)
        
# check input
    try:
        
        self.ids.key.text = voice.recognize_google(voice_command)

# handle the exceptions
    except speech.UnknownValueError:
        
        self.shint = "System could not understand. Please try again."

    except Exception:
        self.shint = "No Internet Connection."

data_path = "data/values/values.bxt"
def save_key(mail,key,path):
    key = key.strip("\n")
    with open(data_path,"a") as f:
        f.write(mail+" "+key+" "+path+"\n")

def check_key(mail,key,path):
    key = key.strip("\n")
    with open(data_path,"r") as f:
        return mail+" "+key+" "+path+"\n" in f.readlines()

def delete_key(mail,key,path):
    key = key.strip("\n")
    with open(data_path,"r") as f:
        k = f.readlines().remove(mail+" "+key+" "+path+"\n")
        
    k = "" if k == None else k
    with open(data_path,"w") as f:
        f.write(k)