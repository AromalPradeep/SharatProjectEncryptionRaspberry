import os
import re
import random
import mailServices.mail as mail
import encryptionServices.encryptions as encryption

def check_if_user_exist(user):
    path = ".//data//private//"
    
    for (root, dirs, file) in os.walk(path):
        for f in file:
            if user+".oec" in f:
                return True

        return False
       
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

    subject = "OTP for eye2eye"
    message = "Your OTP is "+str(otp)

    mail.send_email(subject, message, email)

    return str(otp)

def verify_otp(otp):
    return otp == input("Enter OTP")
     
def signup(email,password):
    if not check_if_user_exist(email):
        return -1 

    if not verify(email):
        print("Invalid mail")
        return -2
    print("Valid Mail")

    if not verify_otp(send_otp(email)):
        print("otp does not match")
        return -3        
    
    with open(email+".oec","w") as f:
        f.write(encryption.md5_hash(password))

    return 1
  
def login(email,password):
    if check_if_user_exist(email):
        return -1 
    
    with open(email+".oec","w") as f:
        if encryption.md5_hash(password) != f.read()[:-2]:
            print("Password does not match!")
            return -2
    
    if not verify_otp(send_otp(email)):
        print("otp does not match")
        return -3      

    return 1
    