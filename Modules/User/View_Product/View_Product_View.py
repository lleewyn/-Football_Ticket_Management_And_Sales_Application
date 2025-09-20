import tkinter as tk
from tkinter import font, Frame, Button, Label, PhotoImage,Tk
from pathlib import Path
from Modules.User.Select_Section_Tickets.Select_Section_View import SelectSection_View
import Modules.User.View_Product.View_Product_Process as up
from pymongo import MongoClient
import os
from dotenv import load_dotenv

class View_Product:
    def __init__(self, window, team_name, user_info):
        self.window = window
        self.team_name = team_name
        self.user_info = user_info
        self.window.title("View Product")
        window_width, window_height = 1440, 950
        screen_width = self.window.winfo_screenwidth()
        x = (screen_width - window_width) // 2
        self.window.geometry(f"{window_width}x{window_height}+{x}+0")
        self.window.resizable(False,False)
        self.window.configure(bg="white")

        base_dir = Path(__file__).parent.parent.parent.parent
        self.assets_path = base_dir / 'Images' / 'ViewProduct'

        self.matches = self.get_match_data_from_mongodb()
        self.create_navbar()
        self.create_scrollable_text()

    def get_match_data_from_mongodb(self):
        base_dir = Path(__file__).resolve().parent.parent
        dotenv_path = base_dir / ".env"
        load_dotenv(dotenv_path)
        mongo_uri = os.getenv("MONGO_URI")
        database_name = os.getenv("MONGO_DATABASE")
        client = MongoClient(mongo_uri)
        db = client[database_name]
        collection = db["Teams"]
        print(f"Fetching data for team: {self.team_name}")

        match_data = collection.find({"team": self.team_name}, {'_id': 1, 'team': 1, 'image': 1, 'matches': 1})
        matches = list(match_data)

        client.close()
        return matches

    def create_navbar(self):
        self.nav_frame = Frame(self.window, bg="#0F2F56", height=120)
        self.nav_frame.pack(fill="x")

        self.logo_img = PhotoImage(file=self.assets_path / "ticketLOGO.png")
        self.name_lg = PhotoImage(file=self.assets_path / "name of website.png")
        self.home_img = PhotoImage(file=self.assets_path / "Home.png")
        self.my_tickets_img = PhotoImage(file=self.assets_path / "My-tickets.png")
        self.avatar_img = PhotoImage(file=self.assets_path / "avatarpic.png")
        self.logout_img = PhotoImage(file=self.assets_path / "Log out.png")

        logo = Label(self.nav_frame, image=self.logo_img, bg='#0F2F56')
        logo.place(x=16, y=11)

        name_logo = Label(self.nav_frame, image=self.name_lg, bg='#0F2F56', borderwidth=0, highlightthickness=0)
        name_logo.place(x=117, y=45)

        home_button = Button(self.nav_frame, image=self.home_img, bg='#0F2F56', borderwidth=0, highlightthickness=0,cursor="hand2",command=lambda: up.ViewProduct_process.home_button_handle(self))
        home_button.place(x=1020, y=55)

        my_tickets_button = Button(self.nav_frame, image=self.my_tickets_img, bg='#0F2F56', borderwidth=0, highlightthickness=0, cursor="hand2", command=lambda: up.ViewProduct_process.my_tickets_button_handle(self))
        my_tickets_button.place(x=1097, y=55)

        avatar_label = Button(self.window, image=self.avatar_img, bg='#0F2F56', borderwidth=0, highlightthickness=0,cursor="hand2",command=lambda: up.ViewProduct_process.user_info_button_handle(self))
        avatar_label.place(x=1210, y=37)

        logout_button = Button(self.window, image=self.logout_img, bg='#0F2F56', borderwidth=0, highlightthickness=0, cursor="hand2", command=lambda: up.ViewProduct_process.back_login_button_handle(self))
        logout_button.place(x=1300, y=37)

    def create_scrollable_text(self):
        frame = tk.Frame(self.window)
        frame.pack(fill=tk.BOTH, expand=True)

        self.canvas = tk.Canvas(frame, bg="white")
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        v_scrollbar = tk.Scrollbar(frame, orient=tk.VERTICAL, command=self.canvas.yview)
        v_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.canvas.configure(yscrollcommand=v_scrollbar.set)

        self.image_frame = tk.Frame(self.canvas, bg="white")
        self.canvas_window = self.canvas.create_window((0, 0), window=self.image_frame, anchor="nw")

        self.image_frame.bind("<Configure>", self.update_scroll_region)
        self.canvas.bind_all("<MouseWheel>", self.on_mouse_wheel)

        team = self.get_team_data(self.team_name)

        if team and "matches" in team:
            self.display_team_info(team)
            self.display_matches(team["matches"])
        else:
            tk.Label(self.image_frame, text="No matches found for this team.", font=("Inter", 14), fg="red",
                     bg="white").pack(pady=20)

    def get_team_data(self, team_name):
        for team in self.matches:
            if team.get("team") == team_name:
                return team
        print(f"No team data found for {team_name}")
        return None

    def display_team_info(self, team):
        self.title_font = font.Font(family="Inter", size=30, weight="bold")
        title_label = tk.Label(self.image_frame, text=team["team"] + " Tickets", font=self.title_font, fg="#2C2C2C",bg='white')
        title_label.pack(anchor="w", padx=112, pady=(30, 0))

        img = PhotoImage(file=self.assets_path / team["image"])
        img_label = tk.Label(self.image_frame, image=img, bg="white")
        img_label.image = img  # Giữ tham chiếu để tránh bị garbage collected
        img_label.pack(anchor="w", padx=112, pady=(5, 0))

    def display_matches(self, matches):
        content_frame = tk.Frame(self.image_frame, bg="white")
        content_frame.pack(padx=112, pady=5, fill='x')

        match_list_frame = tk.Frame(content_frame, bg="white", width=700)
        match_list_frame.grid(row=0, column=0, sticky="nw", padx=(0, 10))

        for i in range(len(matches)):
            match = matches[i]
            match_frame = tk.Frame(match_list_frame, bg="white", padx=10, pady=5)
            match_frame.pack(pady=5, fill="x", expand=True)

            date_frame = tk.Frame(match_frame, bg="white", width=100)
            date_frame.grid(row=0, column=0, sticky="w")
            tk.Label(date_frame, text=match.get("date", "N/A"), font=("Inter", 11, "bold"), fg="#0F2F56",bg="white").pack(anchor="w")
            tk.Label(date_frame, text=match.get("time", "N/A"), font=("Inter", 10), fg="gray", bg="white").pack(anchor="w")

            info_frame = tk.Frame(match_frame, bg="white", width=500)
            info_frame.grid(row=0, column=1, padx=20, sticky="w")
            home_team = match.get("home_team", "Unknown")
            away_team = match.get("away_team", "Unknown")
            tk.Label(info_frame, text=f"{home_team} vs. {away_team}", font=("Inter", 11, "bold"), fg="#2C2C2C",bg="white").pack(anchor="w")
            tk.Label(info_frame, text=match.get("stadium", "N/A"), font=("Inter", 9), fg="gray", bg="white").pack(anchor="w")

            button_frame = tk.Frame(match_frame, bg="white")
            button_frame.grid(row=0, column=2, sticky="e", padx=10)
            view_button = tk.Button(button_frame, text="View ticket", bg="#0F2F56", fg="white",font=("Inter", 10, "bold"), padx=10, pady=2, cursor="hand2",command=lambda m=match: self.show_ticket_options(m))
            view_button.pack(anchor="e")

    def show_ticket_options(self, match):
        if hasattr(self, 'window') and self.window:
            self.window.destroy()
        self.window = Tk()
        team_data = self.get_team_data(self.team_name)
        match_id = team_data['_id'] if team_data else None
        self.app = SelectSection_View(self.window, self.team_name, match, self.user_info, match_id=match_id)
        self.app.display_match_info()

    def update_scroll_region(self, _):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def on_mouse_wheel(self, event):
        self.canvas.yview_scroll(-1 * (event.delta // 120), "units")