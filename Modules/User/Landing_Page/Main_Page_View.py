import tkinter as tk
from tkinter import font, Frame, Button, Label, PhotoImage, Tk
from pathlib import Path
from Modules.User.View_Product.View_Product_View import View_Product
import Modules.User.Landing_Page.Main_Page_Process as up

class MainPage_View:
    def __init__(self, window, user_info):
        self.window = window
        self.user_info = user_info
        self.window.title("Premier League Tickets")

        window_width, window_height = 1440, 950
        screen_width = self.window.winfo_screenwidth()
        x = (screen_width - window_width) // 2
        self.window.geometry(f"{window_width}x{window_height}+{x}+0")
        self.window.resizable(False, False)
        self.window.configure(bg="white")

        base_dir = Path(__file__).parent.parent.parent.parent
        self.assets_path = base_dir / 'Images' / 'Mainpage'

        self.create_navbar()
        self.create_footer()
        self.create_scrollable_text()
        self.content()

    def create_navbar(self):
        nav_frame = Frame(self.window, bg="#0F2F56", height=120)
        nav_frame.pack(fill="x")

        self.logo_img = PhotoImage(file=self.assets_path / "ticketLOGO.png")
        self.name_lg = PhotoImage(file=self.assets_path / "name of website.png")
        self.home_img = PhotoImage(file=self.assets_path / "Choose_Home.png")
        self.my_tickets_img = PhotoImage(file=self.assets_path / "My-tickets.png")
        self.avatar_img = PhotoImage(file=self.assets_path / "avatarpic.png")
        self.logout_img = PhotoImage(file=self.assets_path / "Log out.png")

        logo = Label(nav_frame, image=self.logo_img, bg="#0F2F56")
        logo.place(x=16, y=11)

        name_logo = Label(nav_frame, image=self.name_lg, bg="#0F2F56", borderwidth=0, highlightthickness=0)
        name_logo.place(x=117, y=45)

        home_button = Button(nav_frame, image=self.home_img, bg="#0F2F56", borderwidth=0, highlightthickness=0, cursor="hand2",command=lambda: up.User_Main_Page_process.home_button_handle(self))
        home_button.place(x=1009, y=47)

        my_tickets_button = Button(nav_frame, image=self.my_tickets_img, bg="#0F2F56", borderwidth=0, highlightthickness=0, cursor="hand2",command=lambda: up.User_Main_Page_process.my_tickets_button_handle(self))
        my_tickets_button.place(x=1100, y=55)

        avatar_label = Button(nav_frame, image=self.avatar_img, bg="#0F2F56", borderwidth=0, highlightthickness=0, cursor="hand2",command=lambda: up.User_Main_Page_process.user_info_button_handle(self))
        avatar_label.place(x=1210, y=37)

        logout_button = Button(nav_frame, image=self.logout_img, bg="#0F2F56", borderwidth=0, highlightthickness=0, cursor="hand2",command=lambda: up.User_Main_Page_process.back_login_button_handle(self))
        logout_button.place(x=1300, y=37)

    def create_scrollable_text(self):
        frame = tk.Frame(self.window)
        frame.pack(fill=tk.BOTH, expand=True)

        self.canvas = tk.Canvas(frame, bg="white")
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        v_scrollbar = tk.Scrollbar(frame, orient=tk.VERTICAL, command=self.canvas.yview)
        v_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.canvas.configure(yscrollcommand=v_scrollbar.set)

        self.image_frame = tk.Frame(self.canvas)
        self.canvas_window = self.canvas.create_window((0, 0), window=self.image_frame, anchor="nw")

        self.image_frame.bind("<Configure>", self.update_scroll_region)
        self.canvas.bind_all("<MouseWheel>", self.on_mouse_wheel)

        title_label = tk.Label(self.image_frame, text="PREMIER LEAGUE TICKETS".upper(), font=("Montserrat Black", 45), fg="#0F2F56")
        title_label.pack(pady=2)

        title_small = tk.Label(self.image_frame, text="Get tickets for the best Premier League games.", font=("Montserrat", 15), fg="#0F2F56")
        title_small.pack(pady=3)

    def content(self):
        big_img = PhotoImage(file=self.assets_path / "landing-picture.png")
        image_label = Label(self.image_frame, image=big_img)
        image_label.image = big_img
        image_label.pack(pady=10)

        thumbnail_frame = tk.Frame(self.image_frame)
        thumbnail_frame.pack(pady=10)

        self.Chelsea_img = PhotoImage(file=self.assets_path / "Chelsea.png")
        self.MC_img = PhotoImage(file=self.assets_path / "MC.png")
        self.Tottenham_img = PhotoImage(file=self.assets_path / "Tottenham.png")
        self.Arsenal_img = PhotoImage(file=self.assets_path / "Arsenal.png")
        self.Liverpool_img = PhotoImage(file=self.assets_path / "Liverpool.png")
        self.ManUtd_img = PhotoImage(file=self.assets_path / "ManUtd.png")

        chelsea_button = Button(thumbnail_frame, image=self.Chelsea_img, borderwidth=0, highlightthickness=0, cursor="hand2",command=lambda: self.show_team_details("Chelsea FC"))
        chelsea_button.grid(row=0, column=0, padx=10, pady=10)

        mc_button = Button(thumbnail_frame, image=self.MC_img, borderwidth=0, highlightthickness=0, cursor="hand2",command=lambda: self.show_team_details("Manchester City FC"))
        mc_button.grid(row=0, column=1, padx=10, pady=10)

        tottenham_button = Button(thumbnail_frame, image=self.Tottenham_img, borderwidth=0, highlightthickness=0, cursor="hand2", command=lambda: self.show_team_details("Tottenham Hotspur FC"))
        tottenham_button.grid(row=0, column=2, padx=10, pady=10)

        arsenal_button = Button(thumbnail_frame, image=self.Arsenal_img, borderwidth=0, highlightthickness=0, cursor="hand2",command=lambda: self.show_team_details("Arsenal FC"))
        arsenal_button.grid(row=1, column=0, padx=10, pady=10)

        liverpool_button = Button(thumbnail_frame, image=self.Liverpool_img, borderwidth=0, highlightthickness=0, cursor="hand2",command=lambda: self.show_team_details("Liverpool FC"))
        liverpool_button.grid(row=1, column=1, padx=10, pady=10)

        manUtd_button = Button(thumbnail_frame, image=self.ManUtd_img, borderwidth=0, highlightthickness=0, cursor="hand2",command=lambda: self.show_team_details("Manchester United FC"))
        manUtd_button.grid(row=1, column=2, padx=10, pady=10)

    def update_scroll_region(self, _): #Cập nhật kích thước vùng cuộn
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def on_mouse_wheel(self, event): #Cuộn trang bằng chuột
        self.canvas.yview_scroll(-1 * (event.delta // 120), "units")

    def create_footer(self):
        footer_frame = tk.Frame(self.window, bg="#0F2F56", height=50)
        footer_frame.pack(fill="x", side="bottom")
        footer_label = tk.Label(footer_frame, text="© 2025 Premier League Tickets.", fg="white", bg="#0F2F56",font=("Montserrat", 10))
        footer_label.pack(pady=10)

    def show_team_details(self, team_name):
        if team_name:
            if hasattr(self, 'window') and self.window:
                self.window.destroy()
            self.window = Tk()
            self.app = View_Product(self.window, team_name, self.user_info)
            self.window.mainloop()
        else:
            print("Team name is missing!")