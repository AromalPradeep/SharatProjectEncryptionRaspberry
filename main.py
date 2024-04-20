import os
import cv2
from PIL import Image, ImageTk

# Tkinter
import tkinter as tk
from tkinter import messagebox

# Services
import services.userServices as user

class encryption_app:
    
    def __init__(self, master):
        self.master = master
        self.master.title("Encryption App")
        self.master.geometry("800x400")

        self.error = ""
        self.exit_flag = 3

        self.create_login_signup_widgets()

    # Func: signup
    def signup(self):

        # Add your login functionality here
        self.email = self.email_entry.get()
        password = self.password_entry.get()
        
        if self.email == "admin" and password == "admin":
            self.create_menu()        

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

        match user.login(self.email,password):
            case -1:
                self.error = "User Does Not Exist! Consider signup."
            case -2:
                self.error = "Invalid Credentials!"
            case _:
                self.error = "login"
                self.create_otp_screen()
        
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
            cv2.imwrite("captured_image.png", frame)
            messagebox.showinfo("Capture", "Image captured successfully!")

    # func: populate files
    def populate_listbox(self, path):
        # Clear the listbox
        self.file_listbox.delete(0, tk.END)

        # Get a list of files and directories in the given path
        files = os.listdir(path)

        # Add each file or directory to the listbox
        for item in files:
            self.file_listbox.insert(tk.END, item)

    # func: choose files
    def choose_file(self):
        selected_file_index = self.file_listbox.curselection()
        if selected_file_index:
            selected_file = self.file_listbox.get(selected_file_index)
            self.textbox.delete(1.0, tk.END)
            self.textbox.insert(tk.END, selected_file)
        else:
            messagebox.showwarning("Warning", "Please select a file.")

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

        messagebox.showinfo("OTP", "OTP send to mail.")
        otp = user.send_otp(self.email)
        
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

    # screen: files
    def files_option(self):
        self.clear_screen()

        # Create a frame to contain all elements
        frame = tk.Frame(self.master)
        frame.pack(expand=True, fill=tk.BOTH)

        # Create a scrollbar for the file listbox
        scrollbar = tk.Scrollbar(frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Create a listbox to display files
        self.file_listbox = tk.Listbox(frame, yscrollcommand=scrollbar.set)
        self.file_listbox.pack(expand=True, fill=tk.BOTH, padx=10, pady=10)

        # Populate the listbox with files from the current directory
        self.populate_listbox('.')

        # Configure the scrollbar to work with the listbox
        scrollbar.config(command=self.file_listbox.yview)

        # Create a button to choose a file
        self.choose_button = tk.Button(frame, text="Choose", command=self.choose_file)
        self.choose_button.pack()

        # Create a text box for displaying file information
        self.textbox = tk.Text(frame, height=4, width=30)
        self.textbox.pack(padx=10, pady=10)

        # Create buttons for various actions
        encrypt_button = tk.Button(frame, text="Encrypt")
        encrypt_button.pack(side=tk.LEFT, padx=5, pady=5)

        voice_button = tk.Button(frame, text="Voice")
        voice_button.pack(side=tk.LEFT, padx=5, pady=5)

        open_button = tk.Button(frame, text="Open")
        open_button.pack(side=tk.LEFT, padx=5, pady=5)

        delete_button = tk.Button(frame, text="Delete")
        delete_button.pack(side=tk.LEFT, padx=5, pady=5)

        # Create a button to go back to the menu
        back_button = tk.Button(frame, text="Back", command=self.create_menu)
        back_button.pack(side=tk.RIGHT, padx=5, pady=5)

        # Create a button to navigate to the parent directory
        parent_dir_button = tk.Button(frame, text="Parent Directory", command=lambda: self.populate_listbox('..'))
        parent_dir_button.pack(side=tk.RIGHT, padx=5, pady=5)

        open_folder_button = tk.Button(frame, text="Parent Directory", command=lambda: self.populate_listbox(self.file_listbox.curselection()))
        open_folder_button.pack(side=tk.RIGHT, padx=5, pady=5)

    def settings_option(self):
        return

def main():
    root = tk.Tk()
    _ = encryption_app(root)
    root.mainloop()

if __name__ == "__main__":
    main()
