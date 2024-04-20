import os
import re
import random
import services.mailServices as mail
import services.encryptionServices as encryption

# Func: Verify Email Regex
def verify(email):
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

# Func: Check if a user Exist
def check_if_user_exist(user):
    path = ".//data//private//"
    
    for (root, dirs, file) in os.walk(path):
        for f in file:
            if user+".oec" in f:
                return True

        return False

# Func: Generates OTP
def generate_otp(length = 6):
    digits = "0123456789"
    otp = ""
    for _ in range(length):
        otp += random.choice(digits)
    return otp

# Func: Sent OTP in mail
def send_otp(email):
    otp = generate_otp()

    subject = "OTP for eye2eye"
    message = "Your OTP is "+str(otp)

    mail.send_email(subject, message, email)

    return str(otp)

# Func: Signup
def signup(email,password):
    if check_if_user_exist(email):
        return -1 

    if not verify(email):
        return -2

    create_account(email,password)
    return 1

 # Func: Login 
def login(email,password):
    if check_if_user_exist(email):
        return -1 
    
    with open(email+".oec","w") as f:
        if encryption.md5_hash(password) != f.read()[:-2]:
            print("Password does not match!")
            return -2

    return 1

# Func: Delete Existing Account
def create_account(email,password):
    file_path = ".//data//private//"+email+".oec"    
    with open(file_path,"w") as f:
        f.write(encryption.md5_hash(password))
    
# Func: Delete Existing Account
def delete_account(email):
    file_path = ".//data//private//"+email+".oec"    
    try:
        os.remove(file_path)
    except Exception:
        return
    