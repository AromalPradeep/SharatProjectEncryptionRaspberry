import middleware.userServices.user as user

def run():
    while True:
        print("0. Exit")
        print("1. Signup")
        print("2. Login")

        c = input("Enter choice : ")

        if c == "1":
            email = input("Enter email : ")
            password = input("Enter password : ")
            if user.signup(email,password) == -1:
                print("Account exists")
        elif c == "2":
            return
        else:
            return
