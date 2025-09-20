from tkinter import END, messagebox as mbox
import tkinter as tk
from dotenv import load_dotenv
import os
from pathlib import Path
from pymongo import MongoClient
import Modules.Signup.Signup_View as su
import Modules.Admin.Admin_View as ad
import Modules.User.Landing_Page.Main_Page_View as mp

class Login_backend:
    BASE_DIR = Path(__file__).resolve().parent.parent.parent
    dotenv_path = BASE_DIR / "data" / ".env"
    load_dotenv(dotenv_path)
    MONGO_URI = os.getenv("MONGO_URI")
    MONGO_DATABASE = os.getenv("MONGO_DATABASE")
    client = MongoClient(MONGO_URI)
    db = client[MONGO_DATABASE]
    users_collection = db["Users"]  # Bảng chứa tài khoản
    admin_collection = db["Admin"]  # Bảng chứa tài khoản admin

    # Biến toàn cục để lưu thông tin người dùng
    current_user = None

    @staticmethod
    def sign_up_buton(obj):
        obj.window.destroy()
        app = su.RegisterView()
        app.window.mainloop()

    @staticmethod
    def admin_page(obj):
        obj.window.destroy()
        app = ad.Admin_Dashboard()
        app.window.mainloop()

    @staticmethod
    def user_page(obj):
        obj.window.destroy()
        new_window = tk.Tk()
        app = mp.MainPage_View(new_window, Login_backend.current_user)  # Truyền thông tin người dùng
        app.window.mainloop()

    @staticmethod
    def confirm_button_handle(obj):
        username = obj.email_entry.get().strip()  #Đổi từ email thành username
        password = obj.password_entry.get().strip()

        #Kiểm tra username và password không rỗng
        if not username or not password:
            mbox.showerror("Warning", "Please enter username and password")
            return

        # Tìm user trong database theo username
        user = Login_backend.users_collection.find_one({"username": username})

        if not user:
            mbox.showerror("Warning", "User not found")
            obj.email_entry.delete(0, END)
            obj.password_entry.delete(0, END)
            return

        #So sánh mật khẩu trực tiếp
        if password != user["password"]:
            mbox.showerror("Warning", "Wrong password")
            obj.password_entry.delete(0, END)
            return

        # Nếu đăng nhập thành công → Lưu thông tin người dùng
        Login_backend.current_user = user  # Lưu thông tin người dùng
        mbox.showinfo("Success", "Login successful!")
        Login_backend.user_page(obj)

    @staticmethod
    def admin_login_handle(obj):
        username = obj.email_entry.get().strip()
        password = obj.password_entry.get().strip()

        # Kiểm tra username và password không rỗng
        if not username or not password:
            mbox.showerror("Warning", "Please enter admin username and password")
            return

        # Tìm admin trong database theo username
        admin = Login_backend.admin_collection.find_one({"username": username})

        if not admin:
            mbox.showerror("Warning", "Admin not found")
            obj.email_entry.delete(0, END)
            obj.password_entry.delete(0, END)
            return

        # So sánh mật khẩu trực tiếp
        if password != admin["password"]:
            mbox.showerror("Warning", "Wrong admin password")
            obj.password_entry.delete(0, END)
            return

        # Nếu đăng nhập thành công → Hiện thông báo
        mbox.showinfo("Success", "Admin login successful!")
        Login_backend.admin_page(obj)

    @staticmethod
    def open_contact_page(event):
        import webbrowser
        webbrowser.open("https://www.facebook.com/profile.php?id=61573921396960")