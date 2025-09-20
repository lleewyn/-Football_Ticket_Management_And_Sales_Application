import tkinter as tk
from tkinter import Frame, Button, Label, PhotoImage
from pathlib import Path
import Modules.User.My_Tickets.My_Tickets_Process as up
from pymongo import MongoClient
import os
from dotenv import load_dotenv

class MyTickets_View:
    def __init__(self,window,user_info):
        self.window = window
        self.user_info = user_info
        self.window.title("My Tickets")

        window_width, window_height = 1440, 950
        screen_width = self.window.winfo_screenwidth()
        x = (screen_width - window_width) // 2
        self.window.geometry(f"{window_width}x{window_height}+{x}+0")
        self.window.resizable(False,False)
        self.window.configure(bg="white")

        base_dir = Path(__file__).parent.parent.parent.parent
        self.assets_path = base_dir / 'Images' / 'MyTickets'

        self.create_navbar()
        self.create_scrollable_text()
        self.tickets_history()
    def create_navbar(self):
        nav_frame = Frame(self.window, bg="#0F2F56", height=120)
        nav_frame.pack(fill="x")

        self.logo_img = PhotoImage(file=self.assets_path / "ticketLOGO.png")
        self.name_lg = PhotoImage(file=self.assets_path / "name of website.png")
        self.home_img = PhotoImage(file=self.assets_path / "Home.png")
        self.my_tickets_img = PhotoImage(file=self.assets_path / "Choose_mytickets.png")
        self.avatar_img = PhotoImage(file=self.assets_path / "avatarpic.png")
        self.logout_img = PhotoImage(file=self.assets_path / "Log out.png")

        logo = Label(nav_frame, image=self.logo_img, bg='#0F2F56')
        logo.place(x=16, y=11)

        name_logo = Label(nav_frame, image=self.name_lg, bg='#0F2F56', borderwidth=0, highlightthickness=0)
        name_logo.place(x=117, y=45)

        home_button = Button(nav_frame, image=self.home_img, bg='#0F2F56', borderwidth=0, highlightthickness=0, cursor="hand2",command=lambda: up.MyTickets_process.home_button_handle(self))
        home_button.place(x=1010, y=55)

        my_tickets_button = Button(nav_frame, image=self.my_tickets_img, bg='#0F2F56', borderwidth=0, highlightthickness=0, cursor="hand2",command=lambda: up.MyTickets_process.my_tickets_button_handle(self))
        my_tickets_button.place(x=1088, y=47)

        avatar_label = Button(nav_frame, image=self.avatar_img, bg='#0F2F56', borderwidth=0, highlightthickness=0, cursor="hand2",command=lambda: up.MyTickets_process.user_info_button_handle(self))
        avatar_label.place(x=1210, y=37)

        logout_button = Button(nav_frame, image=self.logout_img, bg='#0F2F56', borderwidth=0, highlightthickness=0, cursor="hand2", command=lambda: up.MyTickets_process.back_login_button_handle(self))
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

    def fetch_purchase_history(self):
        BASE_DIR = Path(__file__).resolve().parent.parent
        dotenv_path = BASE_DIR / ".env"
        load_dotenv(dotenv_path)
        MONGO_URI = os.getenv("MONGO_URI")
        DATABASE_NAME = os.getenv("MONGO_DATABASE")
        client = MongoClient(MONGO_URI)
        db = client[DATABASE_NAME]
        collection = db["Users"]

        user_data = collection.find_one({"email": self.user_info["email"]})

        purchase_data = []
        if user_data and "match_info" in user_data:
            for match in user_data["match_info"]:
                match_info = {
                    "match": f"{match['home_team']} vs {match['away_team']}",
                    "date": match["date"],
                    "time": match["time"],
                    "address": match["stadium"],
                    "tickets": [],
                    "total": f"{match['total']}"
                }
                # Lấy thông tin vé
                for ticket in match["tickets"]:
                    ticket_info = {
                        "section": ticket["area"],
                        "quantity": ticket["quantity"],
                        "price": f"{ticket['price']}",
                        "subtotal": f"{ticket['subtotal']}"
                    }
                    match_info["tickets"].append(ticket_info)
                purchase_data.append(match_info)

        return purchase_data

    def tickets_history(self):
        self.purchase_history_img = PhotoImage(file=self.assets_path / "Purchase history.png")
        purchase_history = Label(self.image_frame, image=self.purchase_history_img, bg='white')
        purchase_history.pack(padx=470, pady=10)

        purchase_data = self.fetch_purchase_history()

        if not purchase_data:
            self.no_tickets_img = PhotoImage(file=self.assets_path / "NoTickets.png")
            no_tickets = tk.Label(self.image_frame, image=self.no_tickets_img, bg="white")
            no_tickets.pack(pady=50)
            return

        for idx, match in enumerate(purchase_data):
            match_frame = tk.Frame(self.image_frame, bg="white", padx=10, pady=10, bd=1, relief="solid")
            match_frame.pack(padx=200, pady=10)

            match_label = tk.Label(match_frame, text=match["match"], font=("Montserrat", 20, "bold"), fg="#0F2F56",
                                   bg="white")
            match_label.pack(anchor="w")

            info_frame = tk.Frame(match_frame, bg="white")
            info_frame.pack(fill="x", pady=2)
            tk.Label(info_frame, text=f"Date: {match['date']}", font=("Montserrat", 16), fg="black", bg="white").pack(anchor="w")
            tk.Label(info_frame, text=f"Time: {match['time']}", font=("Montserrat", 16), fg="black", bg="white").pack(anchor="w")
            tk.Label(info_frame, text=f"Address: {match['address']}", font=("Montserrat", 16), fg="black", bg="white").pack(anchor="w")

            tickets_frame = tk.Frame(match_frame, bg="white")
            tickets_frame.pack(fill="x", pady=5)

            header_frame = tk.Frame(tickets_frame, bg="#0F2F56")
            header_frame.pack(fill="x")
            tk.Label(header_frame, text="Section", font=("Montserrat", 16, "bold"), fg="white", bg="#0F2F56",
                     width=20).grid(row=0, column=0, padx=5)
            tk.Label(header_frame, text="Quantity", font=("Montserrat", 16, "bold"), fg="white", bg="#0F2F56",
                     width=10).grid(row=0, column=1, padx=5)
            tk.Label(header_frame, text="Price (USD)", font=("Montserrat", 16, "bold"), fg="white", bg="#0F2F56",
                     width=15).grid(row=0, column=2, padx=5)
            tk.Label(header_frame, text="Subtotal", font=("Montserrat", 16, "bold"), fg="white", bg="#0F2F56",
                     width=15).grid(row=0, column=3, padx=5)

            for i, ticket in enumerate(match["tickets"]):
                data_frame = tk.Frame(tickets_frame, bg="white")
                data_frame.pack(fill="x")
                tk.Label(data_frame, text=ticket["section"], font=("Montserrat", 16), fg="black", bg="white",
                         width=20).grid(row=0, column=0, padx=5)
                tk.Label(data_frame, text=str(ticket["quantity"]), font=("Montserrat", 16), fg="black", bg="white",
                         width=10).grid(row=0, column=1, padx=5)
                tk.Label(data_frame, text=ticket["price"], font=("Montserrat", 16), fg="black", bg="white",
                         width=15).grid(row=0, column=2, padx=5)
                tk.Label(data_frame, text=ticket["subtotal"], font=("Montserrat", 16), fg="black", bg="white",
                         width=15).grid(row=0, column=3, padx=5)

            total_frame = tk.Frame(match_frame, bg="white")
            total_frame.pack(fill="x", pady=5)
            tk.Label(total_frame, text=f"Total: {match['total']}", font=("Montserrat", 20, "bold"), fg="#0F2F56",
                     bg="white").pack(anchor="e", padx=10)
    def update_scroll_region(self, _):
        """Cập nhật kích thước vùng cuộn"""
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def on_mouse_wheel(self, event):
        """Cuộn trang bằng chuột"""
        self.canvas.yview_scroll(-1 * (event.delta // 120), "units")

