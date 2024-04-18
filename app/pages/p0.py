import services.userValidate as user

def page0():
    print("0. Exit")
    print("1. SignUp")
    print("2. Login")
    choice = input("Choice : ")

    if choice == "0":
        return
    elif choice == "1":
        user.signup()
    elif choice == "2":
        user.login()
    else:
        print("Invalid Entry")