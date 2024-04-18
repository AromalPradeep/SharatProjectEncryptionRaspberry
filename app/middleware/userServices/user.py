import os
import re
import random
import mailServices.mail as mail

def check_if_user_exist(user):
    path = ".//data//private//"
    
    for (root, dirs, file) in os.walk(path):
        for f in file:
            if user+".oec" in f:
                return True

        return False
        
def signup(email,password):
    if not check_if_user_exist(email):
        return -1 

    if not verify(email):
        print("Invalid mail")
    send_otp(email)
    
    with open(email+".oec","w") as f:
        f.write(password)

    return 1
    
def verify(email):
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def generate_otp(length = 6):
    digits = "0123456789"
    otp = ""
    for _ in range(length):
        otp += random.choice(digits)
    return otp

def send_otp(email):
    otp = generate_otp()
    mail.send_mail(email,"OTP",otp)