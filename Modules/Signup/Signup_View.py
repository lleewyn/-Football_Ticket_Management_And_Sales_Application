import tkinter as tk
from tkinter import *
from pathlib import Path
from PIL import Image, ImageTk
import Modules.Signup.Signup_Process as process

class RegisterView:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Register")
        window_width, window_height = 1440, 950
        screen_width = self.window.winfo_screenwidth()
        x = (screen_width - window_width) // 2
        self.window.geometry(f"{window_width}x{window_height}+{x}+0")
        self.window.configure(bg="white")
        self.window.resizable(False, False)

        self.left_frame = tk.Frame(self.window, width=400, height=1024, bg="white")
        self.left_frame.place(x=0, y=0)

        BASE_DIR = Path(__file__).parent.parent.parent
        self.assets_path = BASE_DIR / 'Images' / 'Login'

        self.bg_image = Image.open(self.assets_path/"sign up.png")
        self.bg_image = self.bg_image.resize((400, 1024), Image.LANCZOS)
        self.bg_photo = ImageTk.PhotoImage(self.bg_image)

        self.bg_label = tk.Label(self.left_frame, image=self.bg_photo)
        self.bg_label.place(x=0, y=0, width=400, height=1024)

        self.right_frame = tk.Frame(self.window, width=1040, height=1024, bg="white")
        self.right_frame.place(x=400, y=-35)

        self.form_frame = tk.Frame(self.right_frame, width=600, height=900, bg="white", bd=2, relief="ridge", highlightbackground="gray", highlightthickness=2)
        self.form_frame.place(relx=0.5, rely=0.5, anchor="center")

        tk.Label(self.form_frame, text="Create an account", font=("Inter", 24, "bold"), bg="white", fg="#0f2f56").place(relx=0.5, rely=0.1, anchor="center")

        avatar = PhotoImage(file=self.assets_path/"Generic avatar.png")
        logo = PhotoImage(file=self.assets_path/'logo.png')

        avatar_label = Label(self.window, image=avatar, bg="white", cursor="hand2")
        avatar_label.place(x=910, y=50)

        logo_label = Label(self.window, image=logo, bg="white", cursor="hand2")
        logo_label.place(x=780, y=730)

        # Trường nhập
        self.create_entry("Username", "Enter your username", 150)
        self.create_entry("Email", "Enter your email", 250)
        self.create_password_entry("Password", "Enter your password", 350)
        self.create_password_entry("Re-enter Password", "Enter your password again", 450)

        self.register_button = tk.Button(self.form_frame, text="Sign up", font=("Inter", 16), bg="Black", fg="white", command=lambda : process.Signup_backend.register_button_handle(self))
        self.register_button.place(x=200, y=550, width=200, height=50)
        # quay lại log in
        self.login = Label(self.window, text="Log in", font=("Arial", 14, "underline"), fg="blue", bg = 'white', cursor="hand2")
        self.login.place(x=970, y=700)
        self.login.bind("<Button-1>", lambda _: process.Signup_backend.back_login(self))

        self.login_title = Label(self.window, text="Already have an account", font=("Arial", 14, ""), fg="black", bg = 'white', cursor="hand2")
        self.login_title.place(x=755, y=700)
        self.window.mainloop()

    def create_entry(self, label_text, placeholder, y): #Tạo ô nhập thông tin (không phải mật khẩu)
        tk.Label(self.form_frame, text=label_text, font=("Arial", 12), bg="white", anchor="w").place(x=100, y=y-30)
        entry = tk.Entry(self.form_frame, font=("Arial", 14), fg="gray", bg="white", width=30)
        entry.insert(0, placeholder)
        entry.bind("<FocusIn>", lambda event, e=entry, p=placeholder: self.clear_placeholder(event, e, p))
        entry.bind("<FocusOut>", lambda event, e=entry, p=placeholder: self.restore_placeholder(event, e, p))
        entry.place(x=100, y=y, width=400, height=40)
        error_label = tk.Label(self.form_frame, text="", font=("Arial", 10), fg="red", bg="white")
        error_label.place(x=100, y=y+45)
        setattr(self, f"{label_text.lower()}_entry", entry)
        setattr(self, f"{label_text.lower()}_error", error_label)

    def create_password_entry(self, label_text, placeholder, y): #Tạo ô nhập mật khẩu có nút ẩn/hiện
        tk.Label(self.form_frame, text=label_text, font=("Arial", 12), bg="white", anchor="w").place(x=100, y=y-30)
        frame = tk.Frame(self.form_frame, bg="white")
        frame.place(x=100, y=y, width=400, height=40)

        entry = tk.Entry(frame, font=("Arial", 14), fg="gray", bg="white", width=28, show="")
        entry.insert(0, placeholder)
        entry.bind("<FocusIn>", lambda event, e=entry, p=placeholder: self.clear_placeholder(event, e, p, True))
        entry.bind("<FocusOut>", lambda event, e=entry, p=placeholder: self.restore_placeholder(event, e, p, True))
        entry.pack(side="left", fill="both", expand=True)

        eye_button = tk.Button(frame, text="👁", bg="white", bd=0, command=lambda: self.toggle_password(entry))
        eye_button.pack(side="right")
        error_label = tk.Label(self.form_frame, text="", font=("Arial", 10), fg="red", bg="white")
        error_label.place(x=100, y=y+45)

        setattr(self, f"{placeholder.replace(' ', '_').lower()}_entry", entry)
        setattr(self, f"{placeholder.replace(' ', '_').lower()}_error", error_label)


    def toggle_password(self, entry):
        """Chuyển đổi hiển thị mật khẩu"""
        entry.config(show="" if entry.cget("show") == "*" else "*")

    def clear_placeholder(self, event, entry, placeholder, is_password=False):
        if entry.get() == placeholder:
            entry.delete(0, "end")
            entry.config(fg="black", show="*" if is_password else "")

    def restore_placeholder(self, event, entry, placeholder, is_password=False):
        if entry.get() == "":
            entry.insert(0, placeholder)
            entry.config(fg="gray", show="" if is_password else "")

