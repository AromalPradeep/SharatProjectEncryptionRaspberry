import middleware.userServices.user as user

def run():
    print("0. Exit")
    print("1. Signup")
    print("2. Login")

    c = input("Enter choice : ")

    if c == "0":
        print("Exiting !")
        return
    if c == "1":
        email = input("Enter email : ")
        password = input("Enter password : ")
        if user.signup(email,password) == -1:
            print("Account exists")
            return
        print("Account Created.")
    elif c == "2":
        email = input("Enter email : ")
        password = input("Enter password : ")
        if user.login(email,password) == -1:
            print("Account exists")
            return
        print("Account Created.")
    else:
        return

    while True:
        print("0. Exit")
        print("1. Camera")
        print("2. Encrypt")
        # print("3. Settings")

        c = input("Enter choice : ")

        if c == "0":
            print("Exiting !")
            return
        elif c == "1":
            camera()
        elif c == "2":
            enrypt_file()
        