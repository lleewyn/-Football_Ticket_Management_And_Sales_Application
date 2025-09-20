from tkinter import *
import tkinter as tk
from tkinter import ttk,font, Frame
from pathlib import Path
import Modules.User.Select_Section_Tickets.Select_Section_Process as up

class SelectSection_View:
    def __init__(self, window, team_name, match, user_info, match_id=None):
        self.window = window
        self.team_name = team_name
        self.match = match
        self.user_info = user_info
        self.match_id = match_id
        self.window.title("Select Section Tickets")

        window_width, window_height = 1440, 950
        screen_width = self.window.winfo_screenwidth()
        x = (screen_width - window_width) // 2
        self.window.geometry(f"{window_width}x{window_height}+{x}+0")
        self.window.resizable(False,False)
        self.window.configure(bg="white")

        base_dir = Path(__file__).parent.parent.parent.parent
        self.assets_path = base_dir / 'Images' / 'SelectSectionTickets'

        self.create_navbar()
        self.create_scrollable_text()

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

        home_button = Button(nav_frame, image=self.home_img, bg='#0F2F56', borderwidth=0, highlightthickness=0,cursor="hand2",command=lambda: up.SelectSection_process.home_button_handle(self))
        home_button.place(x=1020, y=55)

        my_tickets_button = Button(nav_frame, image=self.my_tickets_img, bg='#0F2F56', borderwidth=0, highlightthickness=0, cursor="hand2", command=lambda: up.SelectSection_process.my_tickets_button_handle(self))
        my_tickets_button.place(x=1097, y=55)

        avatar_label = Button(nav_frame, image=self.avatar_img, bg='#0F2F56', borderwidth=0, highlightthickness=0,cursor="hand2",command=lambda: up.SelectSection_process.user_info_button_handle(self))
        avatar_label.place(x=1210, y=37)

        logout_button = Button(nav_frame, image=self.logout_img, bg='#0F2F56', borderwidth=0, highlightthickness=0,cursor="hand2", command=lambda: up.SelectSection_process.back_login_button_handle(self))
        logout_button.place(x=1300, y=37)

    def create_scrollable_text(self):
        frame = tk.Frame(self.window, bg="white")
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

        self.frame_tickets_img = PhotoImage(file=self.assets_path / "frame_ticket.png")
        self.background_img = PhotoImage(file=self.assets_path / "Background.png")

        frame_tickets = Label(self.image_frame, image=self.frame_tickets_img, bg='white')
        frame_tickets.pack(side="left")

        background = Label(self.image_frame, image=self.background_img, bg='white')
        background.pack(side="left", padx=10)

        self.payment_img = PhotoImage(file=self.assets_path / "Paymentbutton.png")
        payment = Button(self.image_frame, image=self.payment_img, bg='white', borderwidth=0, highlightthickness=0,cursor="hand2",command=lambda: up.SelectSection_process.payment_button_handle(self))
        payment.place(x=1250, y=15)

        self.display_match_info()

    def display_match_info(self):
        match = self.match

        self.title_font = font.Font(family="Inter", size=18, weight="bold")
        match_title = Label(self.image_frame, text=f"{match['home_team']} vs {match['away_team']}", bg='white',font=self.title_font, fg='#0F2F56')
        match_title.place(x=10, y=20)

        match_info = Label(self.image_frame, text=f"{match['date']} at {match['time']} - {match['stadium']}", font=("Inter", 12), fg="gray", bg="white")
        match_info.place(x=10, y=60)

        self.available_img = PhotoImage(file=self.assets_path / "AvailableTickets.png")
        available = Label(self.image_frame, image=self.available_img, bg='white')
        available.place(x=0, y=100)

        y_offset = 160  # Initial Y-offset for the ticket details
        self.ticket_entries = []  # Danh sách để lưu các ô Entry

        for ticket in match['tickets']:
            area_seats = Label(self.image_frame, text=f"{ticket['area']}", font=("Inter", 16, "bold"), bg='white',
                               borderwidth=0, highlightthickness=0)
            area_seats.place(x=10, y=y_offset)
            y_offset += 37

            area_price_label = Label(self.image_frame,text=f"Available Seats: {ticket['available_seats']} | Price: {ticket['price']}",font=("Inter", 12), bg='white')
            area_price_label.place(x=10, y=y_offset)
            y_offset += 43

            ticket_entry = Entry(self.image_frame, font=("Inter", 18), bd=1,relief="solid",highlightthickness=1, highlightcolor="#D3D3D3", highlightbackground="#D3D3D3",borderwidth=0, width=10, cursor="hand2")
            ticket_entry.place(x=360, y=y_offset)
            self.ticket_entries.append(ticket_entry)  # Lưu ô Entry vào danh sách
            y_offset += 35

            separator = ttk.Separator(self.image_frame, orient='horizontal')
            separator.place(x=10, y=y_offset, width=485)
            y_offset += 15

    def update_scroll_region(self, _):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def on_mouse_wheel(self, event):
        self.canvas.yview_scroll(-1 * (event.delta // 120), "units")



