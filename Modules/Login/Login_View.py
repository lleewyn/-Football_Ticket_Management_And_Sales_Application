from tkinter import *
import tkinter as tk
from pathlib import Path
from PIL import ImageDraw, ImageFont, Image, ImageTk
import Modules.Login.Login_Process as process

class Login_View:
    def __init__(self):
        self.window = tk.Tk()
        self.window.resizable(False, False)

        window_width, window_height = 1440, 950
        screen_width = self.window.winfo_screenwidth()
        x = (screen_width - window_width) // 2
        self.window.geometry(f"{window_width}x{window_height}+{x}+0")
        self.window.configure(bg="#FFFFFF")
        self.window.title("Login")

        BASE_DIR = Path(__file__).parent.parent.parent
        self.assets_path = BASE_DIR / 'Images' / 'Login'

        self.canvas = Canvas(self.window, bg="#FFFFFF", height=1024, width=1440, bd=0, highlightthickness=0,relief="ridge")
        self.canvas.place(x=0, y=0)


        self.background_img = Image.open(self.assets_path / "background.png")
        self.logo_img = Image.open(self.assets_path / "logo.png")

        self.create_overlay()  # Tạo overlay (một lớp màu trắng nhẹ, kích thước cố định 466x371, bo góc)
        self.composite_image = self.background_img.convert("RGBA") # Ban đầu, composite overlay lên ảnh nền gốc (chuyển về RGBA)
        self.composite_image.paste(self.overlay_pil, (self.background_img.width // 2 - 233, self.background_img.height // 2 - 185),  self.overlay_pil)
        self.photo = ImageTk.PhotoImage(self.composite_image)
        self.background = self.canvas.create_image(360, 512, image=self.photo) # Hiển thị ảnh kết hợp trên Canvas

        self.admin_button = Button(self.window, text="Admin".upper(), font=("Montserrat", 18, "bold"), bg="#0f2f56", fg="white", borderwidth=0, width=15, height=2, command=self.show_admin_login)
        self.admin_button.place(x=260, y=500, width=200, height=50)

        self.user_button = Button(self.window, text="User".upper(), font=("Montserrat", 18, "bold"), bg="white", fg="#0f2f56",  borderwidth=0, width=15, height=2, command=self.show_user_login)
        self.user_button.place(x=260, y=570, width=200, height=50)

        # Frame chứa khung đăng nhập
        self.login_frame = Frame(self.window, bg="white", width=396, height=698)
        self.login_frame.place(x=889, y=130)

        self.login = PhotoImage(file=self.assets_path / "Form Log In.png")
        self.login_label = Label(self.login_frame, image=self.login)
        self.login_label.place(x=0, y=0, relwidth=1, relheight=1)  # Ảnh phủ toàn bộ frame

        self.logo = PhotoImage(file=self.assets_path / "logo.png")
        self.logo_lable = Label(self.login_frame, image=self.logo, bg='white')
        self.logo_lable.place(x=55, y=467, width=286, height=161)

        self.show_user_login()  # Mặc định hiển thị login User

    def clear_frame(self):
        for widget in self.login_frame.winfo_children():
            if widget != self.login_label:   # Nếu widget không phải là Label chứa ảnh nền, thì xóa nó
                if widget != self.logo_lable:
                    widget.destroy()

    def show_admin_login(self):
        def clear_placeholder(event, entry, default_text, is_password=False):
            if entry.get() == default_text:
                entry.delete(0, "end")
                entry.config(fg="black", show="*" if is_password else "")

        def restore_placeholder(event, entry, default_text):
            if entry.get() == "":
                entry.insert(0, default_text)
                entry.config(fg="gray")

        self.clear_frame()

        self.signin_label = Label(self.login_frame, text="Admin sign in".upper(), font=("Montserrat Black", 30, "bold"), fg="#0f2f56",bg="white")
        self.signin_label.place(x=36, y=50)

        self.username_label = Label(self.login_frame, text="Username", font=("Inter", 16), fg="black", bg="white")
        self.username_label.place(x=44, y=130)

        self.email_entry = Entry(self.login_frame, font=("Arial", 14), bg="white", fg="gray", bd=1)
        self.email_entry.place(x=48, y=168, width=300, height=40)
        self.email_entry.insert(0, "Enter your username")
        self.email_entry.bind("<FocusIn>",lambda event: clear_placeholder(event, self.email_entry, "Enter your username"))
        self.email_entry.bind("<FocusOut>",lambda event: restore_placeholder(event, self.email_entry, "Enter your username"))

        self.password_label = Label(self.login_frame, text="Password", font=("Inter", 16), fg="black", bg="white")
        self.password_label.place(x=44, y=226)
        self.password_entry = Entry(self.login_frame, font=("Arial", 14), bg="white", fg="gray", bd=1)
        self.password_entry.place(x=48, y=262, width=300, height=40)
        self.password_entry.insert(0, "Enter your password")
        self.password_entry.bind("<FocusIn>",lambda event: clear_placeholder(event, self.password_entry, "Enter your password",True))
        self.password_entry.bind("<FocusOut>", lambda event: restore_placeholder(event, self.password_entry, "Enter your password"))

        self.login_button = Button(self.login_frame, text="Sign in".upper(), font=("Arial", 14, "bold"), bg="black",fg="white", width=20, command=lambda: process.Login_backend.admin_login_handle(self))
        self.login_button.place(x=68, y=330)

    def show_user_login(self):
        def clear_placeholder(event, entry, default_text, is_password=False):
            if entry.get() == default_text:
                entry.delete(0, "end")
                entry.config(fg="black", show="*" if is_password else "")

        def restore_placeholder(event, entry, default_text):
            if entry.get() == "":
                entry.insert(0, default_text)
                entry.config(fg="gray")

        self.clear_frame()

        self.signin_label = Label(self.login_frame, text="User sign in".upper(), font=("Montserrat Black", 30, "bold"), fg="#0f2f56",bg="white")
        self.signin_label.place(x=52, y=50)

        self.username_label = Label(self.login_frame, text="Username", font=("Inter", 16), fg="black", bg="white")
        self.username_label.place(x=44, y=130)

        self.email_entry = Entry(self.login_frame, font=("Arial", 14), bg="white", fg="gray", bd=1)
        self.email_entry.place(x=48, y=168, width=300, height=40)
        self.email_entry.insert(0, "Enter your username")
        self.email_entry.bind("<FocusIn>", lambda event: clear_placeholder(event, self.email_entry, "Enter your username"))
        self.email_entry.bind("<FocusOut>", lambda event: restore_placeholder(event, self.email_entry, "Enter your username"))

        self.password_label = Label(self.login_frame, text="Password", font=("Inter", 16), fg="black", bg="white")
        self.password_label.place(x=44, y=226)
        self.password_entry = Entry(self.login_frame, font=("Arial", 14), bg="white", fg="gray", bd=1)
        self.password_entry.place(x=48, y=262, width=300, height=40)
        self.password_entry.insert(0, "Enter your password")
        self.password_entry.bind("<FocusIn>", lambda event: clear_placeholder(event, self.password_entry, "Enter your password",True))
        self.password_entry.bind("<FocusOut>",lambda event: restore_placeholder(event, self.password_entry, "Enter your password"))

        self.login_button = Button(self.login_frame, text="Sign in".upper(), font=("Arial", 14, "bold"), bg="black",fg="white", width=20,command=lambda: process.Login_backend.confirm_button_handle(self))
        self.login_button.place(x=68, y=330)

        self.sign_up_label = Label(self.login_frame, text="Sign up now", font=("Arial", 14, "underline"), fg="blue",bg='white', cursor="hand2")
        self.sign_up_label.place(x=48, y=400)
        self.sign_up_label.bind('<Button-1>', lambda _: process.Login_backend.sign_up_buton(self))

        self.contact_label = Label(self.login_frame, text="Contact", font=("Arial", 14, "underline"), fg="blue",bg='white', cursor="hand2")
        self.contact_label.place(x=48, y=450)  # Điều chỉnh vị trí nếu cần
        self.contact_label.bind("<Button-1>", process.Login_backend.open_contact_page)
    def create_overlay(self):#Tạo overlay và chồng lên ảnh nền.
        overlay_size = (466, 371)
        overlay_position = (self.background_img.width // 2 - 233, self.background_img.height // 2 - 185)
        # Tạo overlay
        self.overlay_pil = Image.new("RGBA", overlay_size, (255, 255, 255, 0))
        draw = ImageDraw.Draw(self.overlay_pil)
        fill_color = (255, 255, 255, 120)
        draw.rounded_rectangle([(0, 0), overlay_size], radius=30, fill=fill_color)

        # Font chữ
        try:
            font_large = ImageFont.truetype("arialbd.ttf", 60)
            font_small = ImageFont.truetype("arial.ttf", 20)
        except:
            font_large = ImageFont.load_default()
            font_small = ImageFont.load_default()

        text_welcome = "WELCOME!"
        text_sub = "Please select a login role"

        # Lấy kích thước chữ
        bbox_welcome = draw.textbbox((0, 0), text_welcome, font=font_large)
        bbox_sub = draw.textbbox((0, 0), text_sub, font=font_small)

        width_welcome = bbox_welcome[2] - bbox_welcome[0]
        width_sub = bbox_sub[2] - bbox_sub[0]
        text_x_welcome = (overlay_size[0] - width_welcome) / 2
        text_x_sub = (overlay_size[0] - width_sub) / 2

        # Vẽ chữ
        draw.text((text_x_welcome, 35), text_welcome, font=font_large, fill=(255, 255, 255, 255))
        draw.text((text_x_sub, 100), text_sub, font=font_small, fill=(255, 255, 255, 255))


