# import app.app as app

import os
import tkinter as tk
from tkinter import messagebox
import cv2
from PIL import Image, ImageTk

class encryption_app:
    
    def __init__(self, master):
        self.master = master
        self.master.title("Encryption App")
        self.master.geometry("800x400")

        self.create_login_signup_widgets()

    def create_login_signup_widgets(self):
        
        # Create a frame to contain the widgets
        frame = tk.Frame(self.master)
        frame.pack(expand=True, fill=tk.BOTH)
        
        # Create labels and entries for username and password
        username_frame = tk.Frame(frame)
        username_frame.pack(pady=(10, 0))
        tk.Label(username_frame, text="Username:").pack(side=tk.LEFT, padx=(10, 5))
        self.username_entry = tk.Entry(username_frame)
        self.username_entry.pack(side=tk.LEFT)

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


    def login(self):
        # Add your login functionality here
        username = self.username_entry.get()
        password = self.password_entry.get()
        # Dummy login check
        if username == "" and password == "":
            messagebox.showinfo("Login", "Login successful!")
            # self.create_menu()
            self.create_otp_screen()
        else:
            messagebox.showerror("Login Failed", "Invalid username or password.")

    def signup(self):
        # Add your signup functionality here
        messagebox.showinfo("Signup", "Signup functionality not implemented yet.")
        self.create_otp_screen()
        

    def create_otp_screen(self):
        self.clear_screen()
        
         # Create a frame to contain the widgets
        frame = tk.Frame(self.master)
        frame.pack(expand=True, fill=tk.BOTH)
        
        # Create the OTP label and entry widget
        self.otp_label = tk.Label(frame, text="Enter OTP:")
        self.otp_label.pack()

        self.otp_entry = tk.Entry(frame)
        self.otp_entry.pack()

        # Create the check OTP button
        self.check_button = tk.Button(frame, text="Check OTP", command=self.check_otp)
        self.check_button.pack()

    def check_otp(self):
        # Retrieve the OTP entered by the user
        entered_otp = self.otp_entry.get()

        # Check if the entered OTP matches the expected OTP
        expected_otp = ""  # Change this to your expected OTP
        if entered_otp == expected_otp:
            tk.messagebox.showinfo("OTP Verification", "OTP Verified Successfully!")
            self.create_menu()
        else:
            tk.messagebox.showerror("OTP Verification", "Invalid OTP. Please try again.")

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

        option3_button = tk.Button(button_frame, text="Option 3", command=self.option3)
        option3_button.pack(expand=True, fill=tk.BOTH)

        option4_button = tk.Button(button_frame, text="Option 4", command=self.option4)
        option4_button.pack(expand=True, fill=tk.BOTH)

    def camera_option(self):
        self.clear_screen()
        self.cap = cv2.VideoCapture(0)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 320)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 240)

        self.canvas = tk.Canvas(self.master, width=320, height=240)
        self.canvas.grid(row=0, column=0, padx=10, pady=10)

        self.capture_button = tk.Button(self.master, text="Capture", command=self.capture_image)
        self.capture_button.grid(row=1, column=0, pady=5)

        self.update_camera()

    def update_camera(self):
        ret, frame = self.cap.read()
        if ret:
            self.photo = ImageTk.PhotoImage(image=Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)))
            self.canvas.create_image(0, 0, anchor=tk.NW, image=self.photo)
            self.master.after(10, self.update_camera)

    def capture_image(self):
        ret, frame = self.cap.read()
        if ret:
            cv2.imwrite("captured_image.png", frame)
            messagebox.showinfo("Capture", "Image captured successfully!")

    def files_option(self):
        self.clear_screen()
        self.file_listbox = tk.Listbox(self.master)
        self.file_listbox.grid(row=0, column=0, padx=10, pady=10)

        files = os.listdir('.')
        for file in files:
            self.file_listbox.insert(tk.END, file)

        self.choose_button = tk.Button(self.master, text="Choose", command=self.choose_file)
        self.choose_button.grid(row=1, column=0, pady=5)

        self.textbox = tk.Text(self.master, height=4, width=30)
        self.textbox.grid(row=2, column=0, padx=10, pady=10)

        self.button1 = tk.Button(self.master, text="Button 1")
        self.button1.grid(row=3, column=0, padx=5, pady=5)

        self.button2 = tk.Button(self.master, text="Button 2")
        self.button2.grid(row=3, column=1, padx=5, pady=5)

        self.button3 = tk.Button(self.master, text="Button 3")
        self.button3.grid(row=4, column=0, padx=5, pady=5)

        self.button_back = tk.Button(self.master, text="Back", command=self.create_menu)
        self.button_back.grid(row=4, column=1, padx=5, pady=5)

    def choose_file(self):
        selected_file_index = self.file_listbox.curselection()
        if selected_file_index:
            selected_file = self.file_listbox.get(selected_file_index)
            self.textbox.delete(1.0, tk.END)
            self.textbox.insert(tk.END, selected_file)
        else:
            messagebox.showwarning("Warning", "Please select a file.")

    def clear_screen(self):
        for widget in self.master.winfo_children():
            widget.destroy()

    def option3(self):
        messagebox.showinfo("Option 3", "You selected Option 3.")

    def option4(self):
        messagebox.showinfo("Option 4", "You selected Option 4.")

def main():
    root = tk.Tk()
    _ = encryption_app(root)
    root.mainloop()

if __name__ == "__main__":
    main()


# if __name__ == "__main__":
#     app.run()