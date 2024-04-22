import os
import cv2
from PIL import Image, ImageTk
import datetime

# Tkinter
import tkinter as tk
from tkinter import messagebox

# Services
import services.userServices as user
import services.fileServices as file
import services.voiceServices as voice
import services.algoServices as algo

class encryption_app:
    
    def __init__(self, master):
        self.master = master
        self.master.title("Encryption App")
        self.master.geometry("800x400")

        # self.current_path = "D:\Programming2\Projects\SharatProject\data\pictures"
        self.current_path = os.getcwd()+"/data/pictures"
        
        self.error = ""
        self.exit_flag = 3

        self.email = "admin"
        # self.files_option()
        self.create_login_signup_widgets()


    # Func: signup
    def signup(self):

        # Add your login functionality here
        self.email = self.email_entry.get()
        password = self.password_entry.get()
        
        if self.email == "admin" and password == "admin":
            self.create_menu()    
            return    

        match user.signup(self.email,password):
            case -1:
                self.error = "User Already Exists! Consider Login."
            case -2:
                self.error = "Invalid Mail ID!"
            case _:
                self.error = "signup"
                self.create_otp_screen()
                return
        
        messagebox.showerror("Account Creation Failed", self.error)

    # Func: Login
    def login(self):
        # Add your login functionality here
        self.email = self.email_entry.get()
        password = self.password_entry.get()
        
        if self.email == "admin" and password == "admin":
            self.create_menu()      
            return  

        match user.login(self.email,password):
            case -1:
                self.error = "User Does Not Exist! Consider signup."
            case -2:
                self.error = "Invalid Credentials!"
            case _:
                self.create_otp_screen()
                return
        
        messagebox.showerror("Login Failed", self.error)

    # Func: check otp
    def check_otp(self,expected_otp):
        
        # Retrieve the OTP entered by the user
        entered_otp = self.otp_entry.get()

        # Check if the entered OTP matches the expected OTP
        # Change this to your expected OTP
        if entered_otp == expected_otp:
            tk.messagebox.showinfo("OTP Verification", "OTP Verified Successfully!")
            self.enable_fingerprint_screen()
        else:
            self.exit_flag -= 1
            tk.messagebox.showerror("OTP Verification", "Invalid OTP. "+str(self.exit_flag)+" tries remaining.")
            if self.exit_flag == 0:                    
                if self.error == "signup":
                    user.delete_account(self.email)
                self.exit_application()  

    def register_fingerprint(self):
        self.create_menu()

    def check_fingerptint_screen(self):
        return

    def check_fingerptint(self):
        return
 
    # func: update camera
    def update_camera(self):
        ret, frame = self.cap.read()
        if ret:
            self.photo = ImageTk.PhotoImage(image=Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)))
            self.canvas.create_image(0, 0, anchor=tk.NW, image=self.photo)
            self.master.after(10, self.update_camera)

    # func: capture image
    def capture_image(self):
        ret, frame = self.cap.read()
        if ret:
            timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
            path = self.current_path
            cv2.imwrite(path+"//image_"+timestamp+".png", frame)
            messagebox.showinfo("Capture", "Image captured successfully!")

    def populate_listbox(self, path):
        self.file_listbox.delete(0, tk.END)
        self.label.config(text=f"Current Directory: {path}")
        self.current_path = path

        # Add ".." to go back to the parent directory
        # self.file_listbox.insert(tk.END, "..")

        for item in sorted(os.listdir(path)):
            full_path = os.path.join(path, item)
            display_name = f"{item} /" if os.path.isdir(full_path) else item
            self.file_listbox.insert(tk.END, display_name)

    def open_folder(self):
        selected_index = self.file_listbox.curselection()
        if selected_index:
            selected_item = self.file_listbox.get(selected_index)
            # Handle going back to parent directory
            if selected_item == "..":
                self.go_back()
            else:
                new_path = os.path.join(self.current_path, selected_item.rstrip(' /'))
                if os.path.isdir(new_path):
                    self.populate_listbox(new_path)

    def go_back(self):
        parent_directory = os.path.dirname(self.current_path)
        if parent_directory != self.current_path:  # Prevent going back from the root directory
            self.populate_listbox(parent_directory)

    # func: choose files
    def choose_file(self):
        selected_file_index = self.file_listbox.curselection()
        if not selected_file_index:
            messagebox.showwarning("Warning", "Please select a file.")
            return -1
        selected_file = self.file_listbox.get(selected_file_index)
        file_path = self.current_path + "\\" + selected_file
        # self.textbox.delete(1.0, tk.END)
        # self.textbox.insert(tk.END, file_path)
        return file_path

    def encrypt_file(self):
        path = self.choose_file()
        if path == -1:
            return
        mail = self.email
        key = self.key.get("1.0",tk.END)
        if algo.encrypt(mail,key,path):
            messagebox.showinfo("Encrypt File", path+" successfully Encrypted!") 
            algo.save_key(mail,key,path) 
            return
        messagebox.showerror("Encrypt File", path+" could not be Encrypted!") 
       
    def decrypt_file(self):
        path = self.choose_file()
        if path == -1:
            return
        mail = self.email
        key = self.key.get("1.0",tk.END)

        if not algo.check_key(mail,key,path):
            messagebox.showerror("Decrypt File", path+" could not be Decrypted! Credentials does not match!")             
            return
        
        if algo.decrypt(mail,key,path):
            messagebox.showinfo("Decrypt File", path+" successfully Decrypted!")   
            algo.delete_key(mail,key,path)
            return
        messagebox.showerror("Decrypt File", path+" could not be Decrypted! Decryption Error.") 
   
    def voice_key(self):
        self.key.delete(1.0, tk.END)
        text = voice.listen()
        self.key.insert(tk.END, text)       
   
    def open_file(self):
        filename = self.choose_file()        
        if file.open_file(filename):
            # messagebox.showinfo("Open File", filename+" successfully opened!")            
            return
        messagebox.showerror("Open File", filename+" could not be opened!")  
        
    def delete_file(self):
        filename = self.choose_file()
        if filename == -1:
            return
        if file.delete_file(filename):
            messagebox.showinfo("Delete File", filename+" successfully deleted!")   
            self.files_option()         
            return
        messagebox.showerror("Delete File", filename+" could not be deleted!")   

    # func: remove elements
    def clear_screen(self):
        for widget in self.master.winfo_children():
            widget.destroy()
   
    # Func: exit
    def exit_application(self):
        self.master.destroy()
        
    # Screen: Login Signup Screen Elements
    def create_login_signup_widgets(self):
        self.clear_screen()
        
        # Create a frame to contain the widgets
        frame = tk.Frame(self.master)
        frame.pack(expand=True, fill=tk.BOTH)
        
        # Create labels and entries for email and password
        email_frame = tk.Frame(frame)
        email_frame.pack(pady=(10, 0))
        tk.Label(email_frame, text="email:").pack(side=tk.LEFT, padx=(10, 5))
        self.email_entry = tk.Entry(email_frame)
        self.email_entry.pack(side=tk.LEFT)

        password_frame = tk.Frame(frame)
        password_frame.pack()
        tk.Label(password_frame, text="Password:").pack(side=tk.LEFT, padx=(10, 5))
        self.password_entry = tk.Entry(password_frame, show="*")
        self.password_entry.pack(side=tk.LEFT)

        # Create login and signup buttons
        login_signup_frame = tk.Frame(frame)
        login_signup_frame.pack(pady=10)
        self.login_button = tk.Button(login_signup_frame, text="Login", command=self.login)
        self.login_button.pack(side=tk.LEFT, padx=5)
        self.signup_button = tk.Button(login_signup_frame, text="Signup", command=self.signup)
        self.signup_button.pack(side=tk.LEFT)

        # tk.Label(text = self.error)            

    # screen: otp screen elements
    def create_otp_screen(self):
        self.clear_screen()

        otp = user.send_otp(self.email)
        messagebox.showinfo("OTP", "OTP send to mail.")
        
         # Create a frame to contain the widgets
        frame = tk.Frame(self.master)
        frame.pack(expand=True, fill=tk.BOTH)
        
        # Create the OTP label and entry widget
        self.otp_label = tk.Label(frame, text="Enter OTP:")
        self.otp_label.pack()

        self.otp_entry = tk.Entry(frame)
        self.otp_entry.pack()

        # Create the check OTP button
        self.check_button = tk.Button(frame, text="Check OTP", command=lambda:self.check_otp(otp))
        self.check_button.pack()

        # Resend Button
        self.resend_button = tk.Button(frame, text="Resend OTP", command=lambda:self.create_otp_screen)
        self.resend_button.pack()

    # Screen
    def enable_fingerprint_screen(self):
        self.clear_screen()
                
        # Create a frame to contain the elements
        frame = tk.Frame(self.master)
        frame.pack(expand=True, fill=tk.BOTH)

        # Create the label
        label = tk.Label(frame, text="Do you want to add fingerprint feature?", padx=10, pady=10)
        label.pack()

        # Create "Yes" and "No" buttons
        yes_button = tk.Button(frame, text="Yes", command=self.register_fingerprint)
        yes_button.pack(side=tk.LEFT, padx=5, pady=5)

        no_button = tk.Button(frame, text="No", command=self.create_menu)
        no_button.pack(side=tk.RIGHT, padx=5, pady=5)

    # Screen: Menu elements
    def create_menu(self):
        self.clear_screen()

        # Create a frame to contain the buttons
        button_frame = tk.Frame(self.master)
        button_frame.pack(expand=True, fill=tk.BOTH)

        # Create buttons for different options
        camera_button = tk.Button(button_frame, text="Camera", command=self.camera_option)
        camera_button.pack(expand=True, fill=tk.BOTH)

        files_button = tk.Button(button_frame, text="Files", command=self.files_option)
        files_button.pack(expand=True, fill=tk.BOTH)

        option3_button = tk.Button(button_frame, text="Settings", command=self.settings_option)
        option3_button.pack(expand=True, fill=tk.BOTH)

        logout_button = tk.Button(button_frame, text="Logout", command=self.create_login_signup_widgets)
        logout_button.pack(expand=True, fill=tk.BOTH)

    # Screen : Camera
    def camera_option(self):
        self.clear_screen()
        self.cap = cv2.VideoCapture(0)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 320)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 240)

        self.canvas = tk.Canvas(self.master, width=320, height=240)
        self.canvas.grid(row=0, column=0, padx=10, pady=10)

        self.capture_button = tk.Button(self.master, text="Capture", command=self.capture_image)
        self.capture_button.grid(row=1, column=0, pady=5)

        self.button_back = tk.Button(self.master, text="Back", command=self.create_menu)
        self.button_back.grid(row=4, column=1, padx=5, pady=5)

        self.update_camera()

    def files_option(self):
        self.clear_screen()
        
        self.frame = tk.Frame(self.master)
        self.frame.pack(fill="both", expand=True)

        self.label = tk.Label(self.frame, text="Current Directory:")
        self.label.pack()

        self.scrollbar = tk.Scrollbar(self.frame)
        self.scrollbar.pack(side="right", fill="y")

        self.file_listbox = tk.Listbox(self.frame, yscrollcommand=self.scrollbar.set)
        self.file_listbox.pack(fill="both", expand=True)
        self.scrollbar.config(command=self.file_listbox.yview)

        self.back_button = tk.Button(self.frame, text="Back", command=self.go_back)
        self.back_button.pack(side="left")

        self.open_button = tk.Button(self.frame, text="OpenFolder", command=self.open_folder)
        self.open_button.pack(side="right")

        # Create a button to choose a file
        # self.choose_button = tk.Button(self.frame, text="SelectFile", command=self.choose_file)
        # self.choose_button.pack()

        # Create a text box for displaying file information
        # self.textbox = tk.Text(self.frame, height=4, width=30)
        # self.textbox.pack(padx=10, pady=10)
        
        self.key = tk.Text(self.frame, height=4, width=30)
        self.key.pack(padx=10, pady=10)

        # Create buttons for various actions
        encrypt_button = tk.Button(self.frame, text="Encrypt File",command=self.encrypt_file)
        encrypt_button.pack(side=tk.LEFT, padx=5, pady=5)
        
        decrypt_button = tk.Button(self.frame, text="Decrypt File",command=self.decrypt_file)
        decrypt_button.pack(side=tk.LEFT, padx=5, pady=5)

        voice_button = tk.Button(self.frame, text="Voice Key",command=self.voice_key)
        voice_button.pack(side=tk.LEFT, padx=5, pady=5)

        open_button = tk.Button(self.frame, text="Open File",command=self.open_file)
        open_button.pack(side=tk.LEFT, padx=5, pady=5)

        delete_button = tk.Button(self.frame, text="Delete File",command=self.delete_file)
        delete_button.pack(side=tk.LEFT, padx=5, pady=5)

        # Create a button to go back to the menu
        back_button = tk.Button(self.frame, text="Back", command=self.create_menu)
        back_button.pack(side=tk.RIGHT, padx=5, pady=5)

        self.populate_listbox(self.current_path)

    def settings_option(self):
        return

def main():
    root = tk.Tk()
    _ = encryption_app(root)
    root.mainloop()

if __name__ == "__main__":
    main()
