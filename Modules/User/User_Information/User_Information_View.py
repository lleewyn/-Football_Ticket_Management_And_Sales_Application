import tkinter as tk
from tkinter import font, Frame, Button, Label, PhotoImage
from pathlib import Path
import Modules.User.User_Information.User_Information_Process as up

class UserInformation_View:
    def __init__(self,window,user_info):
        self.window = window
        self.user_info = user_info
        self.window.title("Information Customer")

        window_width, window_height = 1440, 950
        screen_width = self.window.winfo_screenwidth()
        x = (screen_width - window_width) // 2
        self.window.geometry(f"{window_width}x{window_height}+{x}+0")
        self.window.resizable(False, False)
        self.window.configure(bg="white")
        self.password_visible = False  # Khởi tạo biến password_visible

        base_dir = Path(__file__).parent.parent.parent.parent
        self.assets_path = base_dir / 'Images' / 'UserInformation'

        self.create_navbar()
        self.content()
    def create_navbar(self):
        nav_frame = Frame(self.window, bg="#0F2F56", height=120)
        nav_frame.pack(fill="x")

        self.logo_img = PhotoImage(file=self.assets_path / "ticketLOGO.png")
        self.name_lg = PhotoImage(file=self.assets_path / "name of website.png")
        self.home_img = PhotoImage(file=self.assets_path / "Home.png")
        self.my_tickets_img = PhotoImage(file=self.assets_path / "My-tickets.png")
        self.avatar_img = PhotoImage(file=self.assets_path / "avatarpic.png")
        self.logout_img = PhotoImage(file=self.assets_path / "Log out.png")

        logo = Label(nav_frame, image=self.logo_img, bg='#0F2F56')
        logo.place(x=16, y=11)

        name_logo = Label(nav_frame, image=self.name_lg, bg='#0F2F56', borderwidth=0, highlightthickness=0)
        name_logo.place(x=117, y=45)

        home_button = Button(nav_frame, image=self.home_img, bg='#0F2F56', borderwidth=0, highlightthickness=0,cursor="hand2", command=lambda: up.UserInformation_process.home_button_handle(self))
        home_button.place(x=1020, y=55)

        my_tickets_button = Button(nav_frame, image=self.my_tickets_img, bg='#0F2F56', borderwidth=0, highlightthickness=0, cursor="hand2",command=lambda: up.UserInformation_process.my_tickets_button_handle(self))
        my_tickets_button.place(x=1097, y=55)

        avatar_label = Button(nav_frame, image=self.avatar_img, bg='#0F2F56', borderwidth=0, highlightthickness=0,cursor="hand2",command=lambda: up.UserInformation_process.user_info_button_handle(self))
        avatar_label.place(x=1210, y=37)

        logout_button = Button(nav_frame, image=self.logout_img, bg='#0F2F56', borderwidth=0, highlightthickness=0, cursor="hand2",command=lambda: up.UserInformation_process.back_login_button_handle(self))
        logout_button.place(x=1300, y=37)

    def content(self):
        self.content_frame = Frame(self.window, bg="white")
        self.content_frame.pack(fill="both", expand=True, pady=20)

        self.info_font = font.Font(family="Arial", size=18)
        self.title_font = font.Font(family="Montserrat Black", size=45, weight="bold")

        self.title_label = tk.Label(self.content_frame, text="Information Customer".upper(), font=self.title_font,fg="#0F2F56", bg='white')
        self.title_label.pack(padx=5, pady=3)

        self.frame_info_img = PhotoImage(file=self.assets_path / "Frame_info.png")
        self.frame_messages_img = PhotoImage(file=self.assets_path / "message.png")
        self.contact_img = PhotoImage(file=self.assets_path / "contact_button.png")

        frame_info = Label(self.content_frame, image=self.frame_info_img, bg='white')
        frame_info.pack(padx=5, pady=3)

        self.username = Label(self.content_frame, text=f"Username: {self.user_info['username']}", font=self.info_font,bg="white",fg="#0F2F56")
        self.username.place(x=400, y=170)

        self.email = Label(self.content_frame, text=f"Email: {self.user_info['email']}", font=self.info_font, bg="white",fg="#0F2F56")
        self.email.place(x=400, y=220)

        self.password = Label(self.content_frame, text="Password: " + "*" * len(self.user_info['password']),font=self.info_font, bg="white", fg="#0F2F56")
        self.password.place(x=400, y=270)

        self.show_button = Button(self.content_frame, text="Show", font=self.info_font, bg="#0F2F56", fg="white",borderwidth=0, cursor="hand2", command=self.show_password)
        self.show_button.place(x=650, y=265)

        self.hide_button = Button(self.content_frame, text="Hide", font=self.info_font, bg="#0F2F56", fg="white", borderwidth=0, cursor="hand2", command=self.hide_password)
        self.hide_button.place_forget()

        frame_messages = Label(self.content_frame, image=self.frame_messages_img, bg='white')
        frame_messages.pack(padx=5, pady=40)

        self.contact_button = Button(self.content_frame, image=self.contact_img, bg='#0F2F56', borderwidth=0,highlightthickness=0, cursor="hand2",command=lambda: up.UserInformation_process.open_contact_page(self))
        self.contact_button.place(x=610, y=650)

    def show_password(self):
        self.password.config(text=f"Password: {self.user_info['password']}")
        self.show_button.place_forget()  # Ẩn nút "Show"
        self.hide_button.place(x=650, y=265)  # Hiện nút "Hide"
        self.password_visible = True

    def hide_password(self):
        self.password.config(text="Password: " + "*" * len(self.user_info['password']))
        self.hide_button.place_forget()  # Ẩn nút "Hide"
        self.show_button.place(x=650, y=265)  # Hiện nút "Show"
        self.password_visible = False





