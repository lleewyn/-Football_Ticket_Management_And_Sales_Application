from tkinter import END, messagebox as mbox
import Modules.Login.Login_View as lg
import re
from dotenv import load_dotenv
from pathlib import Path
import os
from pymongo import MongoClient

class Signup_backend:
    BASE_DIR = Path(__file__).resolve().parent.parent.parent
    dotenv_path = BASE_DIR / "data" / ".env"
    load_dotenv(dotenv_path)
    MONGO_URI = os.getenv("MONGO_URI")
    MONGO_DATABASE = os.getenv("MONGO_DATABASE")
    client = MongoClient(MONGO_URI)
    db = client[MONGO_DATABASE]
    users_collection = db["Users"] # Bảng chứa tài khoản

    @staticmethod
    def back_login(obj):
        obj.window.destroy()
        app = lg.Login_View()
        app.window.mainloop()

    @staticmethod
    def register_button_handle(obj): #Xử lý đăng ký tài khoản
        username = obj.username_entry.get().strip()
        email = obj.email_entry.get().strip()
        password = obj.enter_your_password_entry.get()
        re_password = obj.enter_your_password_again_entry.get()

        #Kiểm tra thông tin không được để trống
        if not email or not username or not password or not re_password:
            mbox.showerror("Warning", "Please fill in all fields")
            return

        #Kiểm tra tên đăng nhập không chứa khoảng trắng
        if " " in username:
            mbox.showerror("Warning", "Username cannot contain spaces")
            return

        #Kiểm tra định dạng email hợp lệ
        email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
        if not re.match(email_regex, email):
            mbox.showerror("Warning", "Invalid email format : ***@gmail.com")
            return

        #Kiểm tra mật khẩu nhập lại có khớp không
        if password != re_password:
            mbox.showerror("Warning", "Passwords do not match")
            return

        #Kiểm tra xem email hoặc tên đăng nhập đã tồn tại chưa
        if Signup_backend.users_collection.find_one({"$or": [{"email": email}, {"username": username}]}):
            mbox.showerror("Warning", "Email or Username already exists")
            return

        # Thêm user mới vào database
        new_user = {
            "email": email,
            "username": username,
            "password": password,
            "match_info": []  # Thêm mảng match_info rỗng
        }
        Signup_backend.users_collection.insert_one(new_user)

        mbox.showinfo("Success", "Account created successfully!")
        obj.email_entry.delete(0, END)
        obj.username_entry.delete(0, END)
        obj.enter_your_password_entry.delete(0, END)
        obj.enter_your_password_again_entry.delete(0, END)
