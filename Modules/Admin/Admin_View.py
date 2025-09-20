import tkinter as tk
from PIL import Image, ImageTk
from pathlib import Path
from tkinter import ttk
from tkinter import Toplevel,Label
from Modules.Admin.Admin_Process import AdminProcess_Main
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np

class Admin_Dashboard:
    def __init__(self):
        self.window = tk.Tk()
        self.window.resizable(False, False)
        self.window.title("Admin Football Ticket App")

        window_width, window_height = 1440, 950
        screen_width = self.window.winfo_screenwidth()
        x = (screen_width - window_width) // 2
        self.window.geometry(f"{window_width}x{window_height}+{x}+0")
        self.window.configure(bg="#FFFFFF")

        BASE_DIR = Path(__file__).parent.parent.parent
        self.assets_path = BASE_DIR / 'Images' / 'Admin'

        self.frame_menu = tk.Frame(self.window, width=365, height=950, bg="White")
        self.frame_menu.pack_propagate(False)
        self.frame_menu.pack(side=tk.LEFT, fill=tk.Y)

        self.menu_photo = self.load_image("logo.png", (338, 94))
        self.menu_label = tk.Label(self.frame_menu, image=self.menu_photo, bg="white")
        self.menu_label.pack(pady=20)

        self.frame_top = tk.Frame(self.window, height=100, bg="darkgray")
        self.frame_top.pack_propagate(False)
        self.frame_top.pack(side=tk.TOP, fill=tk.X)

        self.top_photo = self.load_image("top.png", (1440 - 365, 100))
        self.top_label = tk.Label(self.frame_top, image=self.top_photo, bg="darkgray")
        self.top_label.pack(fill=tk.BOTH, expand=True)

        self.container_frame = tk.Frame(self.window, bg="white")
        self.container_frame.pack(fill=tk.BOTH, expand=True)

        self.content_frame = tk.Frame(self.container_frame, bg="white")
        self.content_frame.pack(fill=tk.BOTH, expand=True)

        self.frames = {}
        for F in (DashboardPage, InvoicesPage, ProductsPage, CustomersPage, Add_products):
            page = F(self.content_frame, self)
            self.frames[F] = page
            page.grid(row=0, column=0, sticky="nsew")

        self.content_frame.grid_rowconfigure(0, weight=1)
        self.content_frame.grid_columnconfigure(0, weight=1)

        self.show_page(DashboardPage)
        self.create_menu_buttons()

    def load_image(self, image_name, size):
        path = self.assets_path / image_name
        img = Image.open(path).resize(size, Image.LANCZOS)
        return ImageTk.PhotoImage(img)

    def create_menu_buttons(self):
        buttons_data = [
            ("Dashboard", "button1.png", DashboardPage),
            ("Invoices", "button2.png", InvoicesPage),
            ("Products", "button3.png", ProductsPage),
            ("Customers", "button4.png", CustomersPage),]
        self.button_images = []
        y_position = 197

        for text, image_name, page in buttons_data:
            img = self.load_image(image_name, (330, 50))
            self.button_images.append(img)
            button = tk.Button(self.frame_menu, image=img,bd=0,relief="flat", bg='white', cursor='hand2',command=lambda p=page: self.show_page(p))
            button.place(x=18, y=y_position)
            y_position += 87

        self.logout_photo = self.load_image("Logout.png", (139, 32))
        self.logout_button = tk.Button(self.frame_menu, image=self.logout_photo,bd=0,bg='white',relief="flat",cursor='hand2',command=lambda: AdminProcess_Main.back_login(self))
        self.logout_button.place(x=34, y=880)

    def show_page(self, page_class):
        if page_class in self.frames:
            frame = self.frames[page_class]
            frame.tkraise()
            if hasattr(frame, 'show') and callable(getattr(frame, 'show')):# Gọi phương thức show nếu trang có phương thức này
                frame.show()
        else:
            print(f"Page {page_class} not found in self.frames")

# ---------------------------------------------CÁC PAGE ------------------------------------------------------------------

# =========================== DASHBOARD PAGE========================================================
class DashboardPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg="#F9FBFF")
        self.controller = controller

        self.title_label = tk.Label(self,text="Match Purchase Statistics".upper(),font=("Montserrat Black", 30),bg="#F9FBFF",fg="#0f2f56")
        self.title_label.pack(pady=15)

        self.chart_frame = tk.Frame(self,bg="white",relief="solid", highlightthickness=1,highlightcolor="#D3D3D3",highlightbackground="#D3D3D3",borderwidth=0,width=800,height=400)
        self.chart_frame.pack(pady=10, padx=20, fill=tk.BOTH, expand=True)
        self.chart_frame.pack_propagate(False)

        self.revenue_frame = tk.Frame(self,bg="#0f2f56",relief="solid",highlightthickness=1,highlightcolor="#D3D3D3",highlightbackground="#D3D3D3",borderwidth=0,width=800,height=150)
        self.revenue_frame.pack(pady=10, padx=20, fill=tk.X)
        self.revenue_frame.pack_propagate(False)

        self.revenue_title_label = tk.Label(self.revenue_frame,text="TOTAL REVENUE FROM TICKET SALES",font=("Montserrat", 16, "bold"),bg="#0f2f56",fg="white")
        self.revenue_title_label.pack(pady=(20, 0))

        self.revenue_amount_label = tk.Label(self.revenue_frame,text="$0", font=("Montserrat Black", 45),bg="#0f2f56",fg="white")
        self.revenue_amount_label.pack(pady=(0, 10))

        self.canvas = None #Biến để lưu canvas của biểu đồ (dùng để cập nhật)
        self.update_data() #Gọi update_data lần đầu tiên khi khởi tạo

    def update_data(self): # Cập nhật dữ liệu doanh thu và biểu đồ
        team_revenue = AdminProcess_Main.get_team_revenue()
        total_revenue = AdminProcess_Main.get_total_revenue()
        self.revenue_amount_label.config(text=f"${total_revenue}")

        if self.canvas:
            self.canvas.get_tk_widget().destroy()
        self.create_bar_chart(team_revenue, self.chart_frame)

    def create_bar_chart(self, team_revenue, chart_frame): #Tạo biểu đồ cột hiển thị tổng doanh thu từ vé đã bán cho từng đội
        fig, ax = plt.subplots(figsize=(8, 4))
        teams = list(team_revenue.keys())
        revenues = list(team_revenue.values())

        bars = ax.bar(teams, revenues, color='#0f2f56', edgecolor='black')
        ax.set_title("Revenue from Ticket Sales by Team", font="Montserrat", fontsize=18, pad=20)
        ax.set_xlabel("Teams", fontsize=20, font="Montserrat")
        ax.set_ylabel("Revenue ($)", fontsize=15, font="Montserrat")

        plt.xticks(rotation=45, ha='right', fontsize=8)
        plt.yticks(fontsize=8)

        max_revenue = max(revenues) if revenues else 0    # Điều chỉnh giới hạn trục y để hiển thị đầy đủ giá trị cao nhất
        ax.set_ylim(0, max_revenue + max_revenue * 0.1)

        if max_revenue > 1000: # Điều chỉnh khoảng cách nhãn trên trục y (nếu doanh thu lớn)
            step = max_revenue // 10
            ax.set_yticks(np.arange(0, max_revenue + step, step))

        for bar in bars:
            yval = bar.get_height()
            ax.text(bar.get_x() + bar.get_width() / 2, yval + max_revenue * 0.02, f"${int(yval)}", ha='center', va='bottom', fontsize=8)
        plt.tight_layout(rect=[0, 0, 1, 0.95])

        self.canvas = FigureCanvasTkAgg(fig, master=chart_frame)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(pady=10, fill=tk.BOTH, expand=True)
        plt.close(fig)

    def show(self): #Phương thức được gọi khi trang được hiển thị.
        self.update_data()
        self.tkraise()

#========================== INVOICE ==================================================

class InvoicesPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg="white")
        self.controller = controller
        self.all_matches = []

        self.create_background()
        self.create_scrollable_area()
        self.load_content()

    def show(self): #Phương thức được gọi khi trang được hiển thị.
        self.load_content()
        self.tkraise() # Hiển thị frame

    def create_background(self):
        self.bg_photo = self.controller.load_image("invoices_bg.png", (1075, 850))
        if self.bg_photo:
            self.bg_label = tk.Label(self, image=self.bg_photo, bg="white")
            self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)

        self.search_entry = tk.Entry(self, width=30, font=("Montserrat", 18), relief="solid", highlightthickness=1,highlightcolor="#D3D3D3", highlightbackground="#D3D3D3", borderwidth=0)
        self.search_entry.place(x=180, y=27)
        self.search_entry.insert(0, "Search matches...")
        self.search_entry.config(fg="grey")
        self.search_entry.bind("<FocusIn>", lambda e: self.clear_search_placeholder())
        self.search_entry.bind("<FocusOut>", lambda e: self.add_search_placeholder())
        self.search_entry.bind("<KeyRelease>", lambda e: self.update_search_results())

        self.sort_var = tk.StringVar()
        sort_options = ["Sort by Date and Time", "Sort by Revenue (High to Low)", "Sort by Home Team"]
        self.sort_combobox = ttk.Combobox(self, textvariable=self.sort_var, values=sort_options,state="readonly", width=25, font=("Montserrat", 12))
        self.sort_combobox.set("Sort by Revenue (High to Low)")
        self.sort_combobox.place(x=755, y=805)
        self.sort_combobox.bind("<<ComboboxSelected>>", self.sort_matches)

    def clear_search_placeholder(self): #Xóa placeholder khi người dùng click vào ô nhập liệu
        if self.search_entry.get() == "Search matches...":
            self.search_entry.delete(0, tk.END)
            self.search_entry.config(fg="black")

    def add_search_placeholder(self): #Thêm placeholder nếu ô nhập liệu trống khi người dùng rời khỏi
        if not self.search_entry.get():
            self.search_entry.insert(0, "Search matches...")
            self.search_entry.config(fg="grey")

    def add_search_placeholder(self):
        if not self.search_entry.get():
            self.search_entry.insert(0, "Search matches...")
            self.search_entry.config(fg="grey")

    def update_search_results(self):
        if not hasattr(self, 'all_matches') or not self.all_matches:
            self.load_content()

        search_text = self.search_entry.get()
        if search_text == "Search matches..." or search_text.strip() == "":
            self.unique_matches = self.all_matches.copy()
        else:
            self.unique_matches = AdminProcess_Main.search_matches(self.all_matches, search_text)

        self.display_matches(self.unique_matches)

    def sort_matches(self, event):
        # Làm mới dữ liệu từ all_matches trước khi sắp xếp
        if not hasattr(self, 'all_matches') or not self.all_matches:
            self.load_content()
        self.unique_matches = self.all_matches.copy()
        self.display_matches(self.unique_matches)

    def display_matches(self, matches): # Hiển thị danh sách trận đấu
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()

        sort_option = self.sort_var.get()
        sorted_matches = AdminProcess_Main.sort_matches(matches.copy(), sort_option)

        for match in sorted_matches:
            frame = self.create_match_frame(match)
            frame.bind("<Button-1>", lambda e, m=match: self.show_match_details(m))

    def create_scrollable_area(self):
        self.canvas = tk.Canvas(self, width=1000, height=696, bg="white", highlightthickness=0)
        self.canvas.place(x=38, y=90)
        self.scrollbar = tk.Scrollbar(self, orient=tk.VERTICAL, command=self.canvas.yview)
        self.scrollbar.place(x=1038, y=90, height=696)
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        self.scrollable_frame = tk.Frame(self.canvas, bg="white")
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.scrollable_frame.bind("<Configure>", self.update_scroll_region)
        self.canvas.bind("<MouseWheel>", self.on_mouse_wheel) # Bind MouseWheel trực tiếp lên canvas thay vì bind_all

    def load_content(self):
        AdminProcess_Main.load_matches(self)
        self.all_matches = self.unique_matches.copy()  # Lưu danh sách gốc
        self.unique_matches = self.all_matches.copy()  # Khởi tạo danh sách hiển thị
        self.display_matches(self.unique_matches)  # Hiển thị lần đầu tiên

    def update_scroll_region(self, event): #Cập nhật kích thước vùng cuộn
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def on_mouse_wheel(self, event): #Cuộn trang bằng chuột
        self.canvas.yview_scroll(-1 * (event.delta // 120), "units")

    def create_match_frame(self, match):
        frame = tk.Frame(self.scrollable_frame, bg="white", padx=10, pady=5) #Tạo frame cho từng trận đấu
        frame.pack(fill="x", pady=5)

        date_label = tk.Label(frame, text=match["date"], font=("Arial", 12), bg="white", fg="#0f2f56", width=15)
        date_label.grid(row=0, column=0, padx=5, pady=5)

        time_label = tk.Label(frame, text=match["time"], font=("Arial", 12), bg="white", fg="#0f2f56", width=10)
        time_label.grid(row=0, column=1, padx=5, pady=5)

        home_team_label = tk.Label(frame, text=match["home_team"], font=("Arial", 12), bg="white", fg="#0f2f56",width=20)
        home_team_label.grid(row=0, column=2, padx=5, pady=5)

        vs_label = tk.Label(frame, text="vs", font=("Arial", 12), bg="white", fg="#0f2f56", width=5)
        vs_label.grid(row=0, column=3, padx=5, pady=5)

        away_team_label = tk.Label(frame, text=match["away_team"], font=("Arial", 12), bg="white", fg="#0f2f56",width=20)
        away_team_label.grid(row=0, column=4, padx=5, pady=5)

        total_label = tk.Label(frame, text=match["total"], font=("Arial", 12), bg="white", fg="#0f2f56", width=30)
        total_label.grid(row=0, column=5, padx=5, pady=5)

        for widget in [frame, date_label, time_label, home_team_label, vs_label, away_team_label, total_label]: # Bind MouseWheel cho từng widget con để truyền sự kiện đến canvas
            widget.bind("<MouseWheel>", self.on_mouse_wheel)  # Truyền sự kiện cuộn chuột
            widget.bind("<Button-1>", lambda e, m=match: self.show_match_details(m))
            widget.config(cursor="hand2")
        return frame

    def show_match_details(self, match):
        self.match = match
        home_team = match["home_team"]
        away_team = match["away_team"]
        date = match["date"]
        time = match["time"]
        total = match["total"]

        ticket_info = AdminProcess_Main.get_tickets_for_match(home_team, away_team, date, time)

        popup = tk.Toplevel(self)
        popup.title("Sold Tickets Information")
        popup_width = 900
        popup_height = 600
        popup.configure(bg="white")
        popup.resizable(False, False)

        main_window_width = self.winfo_width()
        main_window_height = self.winfo_height()
        main_window_x = self.winfo_rootx()
        main_window_y = self.winfo_rooty()
        popup_x = main_window_x + (main_window_width - popup_width) // 2
        popup_y = main_window_y + (main_window_height - popup_height) // 2
        popup.geometry(f"{popup_width}x{popup_height}+{popup_x}+{popup_y}")


        self.create_popup_scrollable_area(popup)
        self.load_popup_content(ticket_info, home_team, away_team, date, time, total)
        popup.mainloop()

    def create_popup_scrollable_area(self, popup):
        self.popup_canvas = tk.Canvas(popup, bg="white", highlightthickness=0)
        self.popup_scrollbar = tk.Scrollbar(popup, orient="vertical", command=self.popup_canvas.yview)
        self.popup_scrollable_frame = tk.Frame(self.popup_canvas, bg="white")
        self.popup_scrollable_frame.bind("<Configure>", self.update_popup_scroll_region)
        self.popup_canvas.bind("<MouseWheel>", self.on_popup_mouse_wheel)
        popup_width = popup.winfo_width()
        self.popup_canvas.configure(width=popup_width - 40)  # Trừ đi padding và scrollbar
        self.popup_canvas.create_window((popup_width // 2 - 20), 0, window=self.popup_scrollable_frame, anchor="n")
        self.popup_canvas.configure(yscrollcommand=self.popup_scrollbar.set)
        self.popup_canvas.pack(side="left", fill="both", expand=True, padx=20, pady=(30, 0))
        self.popup_scrollbar.pack(side="right", fill="y")

    def update_popup_scroll_region(self, event):
        self.popup_canvas.configure(scrollregion=self.popup_canvas.bbox("all"))

    def on_popup_mouse_wheel(self, event):
        self.popup_canvas.yview_scroll(-1 * (event.delta // 120), "units")

    def load_popup_content(self, ticket_info, home_team, away_team, date, time, total):
        tk.Label(self.popup_scrollable_frame, text=f"{home_team} vs {away_team}", font=("Montserrat", 22, "bold"),fg="#0f2f56", bg="white").pack(pady=(5, 0), anchor="center", fill="x", expand=True)

        stadium = self.match["stadium"] if "stadium" in self.match else "N/A"
        info_text = f"{date}, {time}, {stadium}"
        tk.Label(self.popup_scrollable_frame, text=info_text, font=("Arial", 14, "italic"), fg="#0f2f56",bg="white").pack(pady=(0, 5), anchor="center", fill="x", expand=True)

        tk.Label(self.popup_scrollable_frame, text=f"Total Revenue: {total}", font=("Arial", 18, "bold"), fg="black",bg="white").pack(pady=(0, 10), anchor="center", fill="x", expand=True)

        if not ticket_info:
            customer_frame = tk.Frame(self.popup_scrollable_frame, bg="white", bd=1, relief="solid")
            customer_frame.pack(pady=10, anchor="center", padx=12, fill="x")

            tk.Label(customer_frame, text="No customers have purchased tickets yet.", font=("Arial", 16, "bold"),fg="red",bg="white").pack(pady=(5, 4), anchor="center", fill="x", expand=True)

            tickets_frame = tk.Frame(customer_frame, bg="white")
            tickets_frame.pack(anchor="center", pady=5, fill="x")

            header_frame = tk.Frame(tickets_frame, bg="#0F2F56")
            header_frame.pack(fill="x")
            tk.Label(header_frame, text="Section", font=("Arial", 14, "bold"), fg="white", bg="#0F2F56",
                     width=22, anchor="center").grid(row=0, column=0, padx=5, sticky="nsew")
            tk.Label(header_frame, text="Quantity", font=("Arial", 14, "bold"), fg="white", bg="#0F2F56",
                     width=10, anchor="center").grid(row=0, column=1, padx=5, sticky="nsew")
            tk.Label(header_frame, text="Price", font=("Arial", 14, "bold"), fg="white", bg="#0F2F56",
                     width=15, anchor="center").grid(row=0, column=2, padx=5, sticky="nsew")
            tk.Label(header_frame, text="Subtotal", font=("Arial", 14, "bold"), fg="white", bg="#0F2F56",
                     width=15, anchor="center").grid(row=0, column=3, padx=5, sticky="nsew")

            header_frame.grid_columnconfigure(0, weight=1)
            header_frame.grid_columnconfigure(1, weight=1)
            header_frame.grid_columnconfigure(2, weight=1)
            header_frame.grid_columnconfigure(3, weight=1)

            customer_frame.bind("<MouseWheel>", self.on_popup_mouse_wheel)
            tickets_frame.bind("<MouseWheel>", self.on_popup_mouse_wheel)
            header_frame.bind("<MouseWheel>", self.on_popup_mouse_wheel)
            return

        for ticket in ticket_info:
            customer_frame = tk.Frame(self.popup_scrollable_frame, bg="white", bd=1, relief="solid")
            customer_frame.pack(pady=10, anchor="center", padx=12, fill="x")

            customer_text = f"Customer: {ticket['username']} | Total: ${ticket['total']}"
            tk.Label(customer_frame, text=customer_text, font=("Arial", 16, "bold"), fg="#0f2f56",bg="white").pack(pady=(5, 4), anchor="center", fill="x", expand=True)

            tickets_frame = tk.Frame(customer_frame, bg="white")
            tickets_frame.pack(anchor="center", pady=5, fill="x")

            header_frame = tk.Frame(tickets_frame, bg="#0F2F56")
            header_frame.pack(fill="x")
            tk.Label(header_frame, text="Section", font=("Arial", 14, "bold"), fg="white", bg="#0F2F56",
                     width=22, anchor="center").grid(row=0, column=0, padx=5, sticky="nsew")
            tk.Label(header_frame, text="Quantity", font=("Arial", 14, "bold"), fg="white", bg="#0F2F56",
                     width=10, anchor="center").grid(row=0, column=1, padx=5, sticky="nsew")
            tk.Label(header_frame, text="Price", font=("Arial", 14, "bold"), fg="white", bg="#0F2F56",
                     width=15, anchor="center").grid(row=0, column=2, padx=5, sticky="nsew")
            tk.Label(header_frame, text="Subtotal", font=("Arial", 14, "bold"), fg="white", bg="#0F2F56",
                     width=15, anchor="center").grid(row=0, column=3, padx=5, sticky="nsew")

            #Đảm bảo các cột có trọng số đồng đều để căn giữa
            header_frame.grid_columnconfigure(0, weight=1)
            header_frame.grid_columnconfigure(1, weight=1)
            header_frame.grid_columnconfigure(2, weight=1)
            header_frame.grid_columnconfigure(3, weight=1)

            for t in ticket.get("tickets", []):
                data_frame = tk.Frame(tickets_frame, bg="white")
                data_frame.pack(fill="x")
                tk.Label(data_frame, text=t.get("area", "N/A"), font=("Arial", 14), fg="black", bg="white",
                         width=22, anchor="center").grid(row=0, column=0, padx=5, sticky="nsew")
                tk.Label(data_frame, text=str(t.get("quantity", 0)), font=("Arial", 14), fg="black", bg="white",
                         width=10, anchor="center").grid(row=0, column=1, padx=5, sticky="nsew")
                tk.Label(data_frame, text=t.get("price", "$0"), font=("Arial", 14), fg="black", bg="white",
                         width=15, anchor="center").grid(row=0, column=2, padx=5, sticky="nsew")
                tk.Label(data_frame, text=t.get("subtotal", "$0"), font=("Arial", 14), fg="black", bg="white",
                         width=15, anchor="center").grid(row=0, column=3, padx=5, sticky="nsew")

                data_frame.grid_columnconfigure(0, weight=1)
                data_frame.grid_columnconfigure(1, weight=1)
                data_frame.grid_columnconfigure(2, weight=1)
                data_frame.grid_columnconfigure(3, weight=1)

            # Bind sự kiện cuộn chuột cho khung khách hàng và các thành phần con
            customer_frame.bind("<MouseWheel>", self.on_popup_mouse_wheel)
            tickets_frame.bind("<MouseWheel>", self.on_popup_mouse_wheel)
            header_frame.bind("<MouseWheel>", self.on_popup_mouse_wheel)
            for child in tickets_frame.winfo_children():
                child.bind("<MouseWheel>", self.on_popup_mouse_wheel)

# ==================================  PRODUCT PAGE  =================================================================================
class ProductsPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg="white")
        self.controller = controller
        self.all_matches = []

        self.create_background()
        self.create_scrollable_area()
        self.load_content()

    def show(self):
        self.load_content()
        self.tkraise()

    def create_background(self):
        self.bg_photo = self.controller.load_image("product_bg.png", (1075, 850))
        self.bg_label = tk.Label(self,image=self.bg_photo,bg="white" )
        self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)

        self.add_photo = self.controller.load_image("add_button.png", (200, 44))
        self.add_button = tk.Button(self,image=self.add_photo,bd=0,relief="flat",cursor="hand2",bg="#F9FBFF",command=lambda: self.controller.show_page(Add_products))
        self.add_button.place(x=828, y=29)

        self.search_entry = tk.Entry(self, width=30, font=("Montserrat", 18), relief="solid",highlightthickness=1, highlightcolor="#D3D3D3", highlightbackground="#D3D3D3", borderwidth=0)
        self.search_entry.place(x=200, y=30)
        self.search_entry.insert(0, "Search matches...")
        self.search_entry.config(fg="grey")

        self.search_entry.bind("<FocusIn>", lambda e: self.clear_search_placeholder())
        self.search_entry.bind("<FocusOut>", lambda e: self.add_search_placeholder())
        self.search_entry.bind("<KeyRelease>", lambda e: self.update_search_results())

        self.sort_var = tk.StringVar()
        sort_options = ["Sort by Date and Time", "Sort by Home Team"]
        self.sort_combobox = ttk.Combobox(self, textvariable=self.sort_var, values=sort_options, state="readonly",width=25, font=("Montserrat", 12))
        self.sort_combobox.set("Sort by Date and Time")
        self.sort_combobox.place(x=755, y=800)
        self.sort_combobox.bind("<<ComboboxSelected>>", self.sort_matches)

    def clear_search_placeholder(self):
        if self.search_entry.get() == "Search matches...":
            self.search_entry.delete(0, tk.END)
            self.search_entry.config(fg="black")

    def add_search_placeholder(self):
        if not self.search_entry.get():
            self.search_entry.insert(0, "Search matches...")
            self.search_entry.config(fg="grey")

    def update_search_results(self):
        if not hasattr(self, 'all_matches') or not self.all_matches:
            self.load_content()

        search_text = self.search_entry.get()
        if search_text == "Search matches..." or search_text.strip() == "":
            self.unique_matches = self.all_matches.copy()
        else:
            self.unique_matches = AdminProcess_Main.search_matches(self.all_matches, search_text)

        self.display_matches(self.unique_matches)

    def sort_matches(self, event):
        self.display_matches(self.unique_matches)

    def display_matches(self, matches):
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()

        sort_option = self.sort_var.get()
        sorted_matches = AdminProcess_Main.sort_products(matches.copy(), sort_option)

        def create_handler(match):
            return lambda e: self.open_edit_window(match)

        for match in sorted_matches:
            frame = self.create_match_frame(match)
            frame.bind("<Button-1>", create_handler(match))

    def create_scrollable_area(self):
        self.canvas = tk.Canvas(self, width=1000, height=696, bg="white", highlightthickness=0)
        self.canvas.place(x=38, y=90)
        self.scrollbar = tk.Scrollbar(self, orient=tk.VERTICAL, command=self.canvas.yview)
        self.scrollbar.place(x=1038, y=90, height=696)
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        self.scrollable_frame = tk.Frame(self.canvas, bg="white")
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.scrollable_frame.bind("<Configure>", self.update_scroll_region)
        self.canvas.bind("<MouseWheel>", self.on_mouse_wheel)

    def update_scroll_region(self, event):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def on_mouse_wheel(self, event):
        self.canvas.yview_scroll(-1 * (event.delta // 120), "units")

    def load_content(self):
        AdminProcess_Main.load_matches(self)
        self.all_matches = self.unique_matches.copy()
        self.unique_matches = self.all_matches.copy()
        self.display_matches(self.unique_matches)

    def create_match_frame(self, match):
        frame = tk.Frame(self.scrollable_frame, bg="white", padx=10, pady=5)
        frame.pack(fill="x", pady=5)

        date_label = tk.Label(frame, text=match["date"], font=("Arial", 12), bg="white", fg="#0f2f56", width=15)
        date_label.grid(row=0, column=0, padx=5, pady=5)

        time_label = tk.Label(frame, text=match["time"], font=("Arial", 12), bg="white", fg="#0f2f56", width=10)
        time_label.grid(row=0, column=1, padx=5, pady=5)

        home_team_label = tk.Label(frame, text=match["home_team"], font=("Arial", 12), bg="white", fg="#0f2f56", width=20)
        home_team_label.grid(row=0, column=2, padx=5, pady=5)

        vs_label = tk.Label(frame, text="vs", font=("Arial", 12), bg="white", fg="#0f2f56", width=5)
        vs_label.grid(row=0, column=3, padx=5, pady=5)

        away_team_label = tk.Label(frame, text=match["away_team"], font=("Arial", 12), bg="white", fg="#0f2f56", width=20)
        away_team_label.grid(row=0, column=4, padx=5, pady=5)

        stadium_label = tk.Label(frame, text=match["stadium"], font=("Arial", 12), bg="white", fg="#0f2f56", width=30)
        stadium_label.grid(row=0, column=5, padx=5, pady=5)

        for widget in [frame, date_label, time_label, home_team_label, vs_label, away_team_label, stadium_label]:
            widget.bind("<MouseWheel>", self.on_mouse_wheel)
            widget.bind("<Button-1>", lambda e, m=match: self.open_edit_window(m))
            widget.config(cursor="hand2")
        return frame

    def open_edit_window(self, match):
        edit_window = Toplevel(self)
        edit_window.title("Edit Match")
        window_width = 950
        window_height = 670
        edit_window.resizable(False, False)
        edit_window.configure(bg="white")

        edit_window.transient(self)
        edit_window.grab_set()

        main_window_width = self.winfo_width()
        main_window_height = self.winfo_height()
        main_window_x = self.winfo_rootx()
        main_window_y = self.winfo_rooty()
        x = main_window_x + (main_window_width - window_width) // 2
        y = main_window_y + (main_window_height - window_height) // 2
        edit_window.geometry(f"{window_width}x{window_height}+{x}+{y}")

        main_frame = tk.Frame(edit_window, bg="white")
        main_frame.pack(padx=20, pady=20, fill=tk.BOTH, expand=True)

        title_label = tk.Label(main_frame, text="Product Update".upper(), font=("Montserrat Black", 30), fg="#0F2F56",bg="white")
        title_label.pack(anchor="center", pady=(0, 5))

        match_name = f"{match['home_team']} vs {match['away_team']}"
        match_label = tk.Label(main_frame, text=match_name, font=("Montserrat", 16, "bold"), fg="black", bg="white")
        match_label.pack(anchor="center", pady=(0, 7))

        info_frame = tk.Frame(main_frame, bg="white", bd=1, relief="solid",highlightthickness=1,highlightcolor="white", highlightbackground="white", borderwidth=0)
        info_frame.pack(fill="x", pady=10)

        date_frame = tk.Frame(info_frame, bg="white")
        date_frame.pack(fill="x", pady=2)
        tk.Label(date_frame, text="Date:", font=("Montserrat", 16), fg="black", bg="white", width=10).pack(side="left")
        date_entry = tk.Entry(date_frame, font=("Montserrat", 16), width=30, relief="solid", highlightthickness=1,highlightcolor="#D3D3D3", highlightbackground="#D3D3D3", borderwidth=0)
        date_entry.insert(0, match["date"])
        date_entry.pack(side="left", padx=5)

        time_frame = tk.Frame(info_frame, bg="white")
        time_frame.pack(fill="x", pady=2)
        tk.Label(time_frame, text="Time:", font=("Montserrat", 16), fg="black", bg="white", width=10).pack(side="left")
        time_entry = tk.Entry(time_frame, font=("Montserrat", 16), width=30, relief="solid", highlightthickness=1,highlightcolor="#D3D3D3", highlightbackground="#D3D3D3", borderwidth=0)
        time_entry.insert(0, match["time"])
        time_entry.pack(side="left", padx=5)

        stadium_frame = tk.Frame(info_frame, bg="white")
        stadium_frame.pack(fill="x", pady=2)
        tk.Label(stadium_frame, text="Stadium:", font=("Montserrat", 16), fg="black", bg="white", width=10).pack(side="left")
        stadium_entry = tk.Entry(stadium_frame, font=("Montserrat", 16), width=30, relief="solid", highlightthickness=1,highlightcolor="#D3D3D3", highlightbackground="#D3D3D3", borderwidth=0)
        stadium_entry.insert(0, match["stadium"])
        stadium_entry.pack(side="left", padx=5)

        tickets_frame = tk.Frame(main_frame, bg="white", bd=1, relief="solid")
        tickets_frame.pack(fill="x", pady=10)

        header_frame = tk.Frame(tickets_frame, bg="#0F2F56")
        header_frame.pack(fill="x")
        tk.Label(header_frame, text="Section", font=("Montserrat", 13, "bold"), fg="white", bg="#0F2F56",
                 width=12, anchor="center").grid(row=0, column=0, padx=5, pady=5, sticky="ew")
        tk.Label(header_frame, text="Available Tickets", font=("Montserrat", 13, "bold"), fg="white", bg="#0F2F56",
                 width=16, anchor="center").grid(row=0, column=1, padx=5, pady=5, sticky="ew")
        tk.Label(header_frame, text="Price (USD)", font=("Montserrat", 13, "bold"), fg="white", bg="#0F2F56",
                 width=16, anchor="center").grid(row=0, column=2, padx=5, pady=5, sticky="ew")
        tk.Label(header_frame, text="New Price (USD)", font=("Montserrat", 13, "bold"), fg="white", bg="#0F2F56",
                 width=16, anchor="center").grid(row=0, column=3, padx=5, pady=5, sticky="ew")
        tk.Label(header_frame, text="New Seats", font=("Montserrat", 13, "bold"), fg="white", bg="#0F2F56",
                 width=16, anchor="center").grid(row=0, column=4, padx=5, pady=5, sticky="ew")

        for col in range(5):
            header_frame.grid_columnconfigure(col, weight=1)

        # Load ticket data
        ticket_dict = {ticket["area"]: ticket for ticket in match.get("tickets", [])}
        standard_areas = [
            ("SUT", "Shortside Upper Tier"),
            ("LUT", "Longside Upper Tier"),
            ("LLT", "Longside Lower Tier"),
            ("SLT", "Shortside Lower Tier"),
            ("AW", "Away Section")]

        ticket_categories = []
        for code, area in standard_areas:
            if area in ticket_dict:
                ticket = ticket_dict[area]
                price = ticket.get("price", "error")
                if price is None or price == 0 or not isinstance(price, str):
                    price = "error"
                ticket_categories.append({
                    "section": code,
                    "available": int(ticket.get("available_seats", "error")),
                    "price": price})
            else:
                ticket_categories.append({
                    "section": code,
                    "available": int(match["available_seats_by_category"].get(area, "error")),
                    "price": "error"})

        price_entries = {}
        seat_entries = {}
        for i, category in enumerate(ticket_categories):
            data_frame = tk.Frame(tickets_frame, bg="white")
            data_frame.pack(fill="x", pady=2)

            for col in range(5):
                data_frame.grid_columnconfigure(col, weight=1)

            tk.Label(data_frame, text=category["section"], font=("Montserrat", 14), fg="black", bg="white",
                     width=12, anchor="center").grid(row=0, column=0, padx=5, pady=5, sticky="ew")

            tk.Label(data_frame, text=str(category["available"]), font=("Montserrat", 14), fg="black", bg="white",
                     width=16, anchor="center").grid(row=0, column=1, padx=5, pady=5, sticky="ew")

            tk.Label(data_frame, text=category["price"], font=("Montserrat", 14), fg="black", bg="white",
                     width=16, anchor="center").grid(row=0, column=2, padx=5, pady=5, sticky="ew")

            price_entry = tk.Entry(data_frame, font=("Montserrat", 14), width=12, relief="solid", highlightthickness=1,highlightcolor="#D3D3D3", highlightbackground="#D3D3D3", borderwidth=0,justify="center")
            price_entry.insert(0, "")
            price_entry.grid(row=0, column=3, padx=48, pady=5, sticky="ew")
            price_entries[i] = price_entry

            seat_entry = tk.Entry(data_frame, font=("Montserrat", 14), width=12, relief="solid", highlightthickness=1,highlightcolor="#D3D3D3", highlightbackground="#D3D3D3", borderwidth=0,justify="center")
            seat_entry.insert(0, "")
            seat_entry.grid(row=0, column=4, padx=15, pady=5, sticky="ew")
            seat_entries[i] = seat_entry

        buttons_frame = tk.Frame(main_frame, bg="white")
        buttons_frame.pack(fill="x", pady=20)

        button_container = tk.Frame(buttons_frame, bg="white")
        button_container.pack(expand=True)  # Center the container in buttons_frame

        save_button_image = self.controller.load_image("btn_Save_Changes.png", (140, 50))
        save_button = tk.Button(button_container, image=save_button_image, bd=0, relief="flat", cursor='hand2')
        save_button.image = save_button_image
        save_button.pack(side="left", padx=10)

        delete_button_image = self.controller.load_image("btn_Delete_Match.png", (140, 50))
        delete_button = tk.Button(button_container, image=delete_button_image, bd=0, relief="flat", cursor='hand2')
        delete_button.image = delete_button_image
        delete_button.pack(side="left", padx=10)

        cancel_button_image = self.controller.load_image("btn_cancel_changes.png", (140, 50))
        cancel_button = tk.Button(button_container, image=cancel_button_image, bd=0, relief="flat", cursor='hand2')
        cancel_button.image = cancel_button_image
        cancel_button.pack(side="left", padx=10)

        def save_changes():
            new_data = {
                "date": date_entry.get().strip(),
                "time": time_entry.get().strip(),
                "stadium": stadium_entry.get().strip(),
                "tickets": []}
            for i in range(len(ticket_categories)):
                new_price = price_entries[i].get().strip()
                new_seats = seat_entries[i].get().strip()
                old_price = ticket_categories[i]["price"]
                old_seats = str(ticket_categories[i]["available"])
                new_data["tickets"].append({
                    "area": standard_areas[i][1],  # Use the full area name (e.g., "Shortside Upper Tier")
                    "new_price": new_price,
                    "new_seats": new_seats,
                    "old_price": old_price,
                    "old_seats": old_seats})
            AdminProcess_Main.update_match(self, match, new_data, edit_window)

        def delete_match():
            AdminProcess_Main.delete_match(self, match, edit_window)
            edit_window.destroy()

        def cancel_changes():
            edit_window.destroy()

        save_button.config(command=save_changes)
        delete_button.config(command=delete_match)
        cancel_button.config(command=cancel_changes)

# ================================== ADD PRODUCT PAGE ==============================================================================
class Add_products(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg="white")
        self.controller = controller
        self.VALID_TEAMS = [
            "Chelsea FC", "Arsenal FC", "Manchester City FC",
            "Liverpool FC", "Manchester United FC", "Tottenham Hotspur FC"]
        self.STADIUMS = [
            "Stamford Bridge", "Emirates Stadium", "Etihad Stadium",
            "Anfield", "Old Trafford", "Tottenham Hotspur Stadium"]
        self.TICKET_CATEGORIES = [
            {"area": "Shortside Upper Tier", "price": "$244"},
            {"area": "Longside Upper Tier", "price": "$258"},
            {"area": "Longside Lower Tier", "price": "$286"},
            {"area": "Shortside Lower Tier", "price": "$348"},
            {"area": "Away Section", "price": "$394"}]

        self.seat_entries = []
        self.price_entries = []
        self.create_background()
        self.create_input_fields()
        self.create_save_button()

    def create_background(self):  # Tạo background cho trang
        self.bg_photo = self.controller.load_image("Frame_Add_Products.png", (1075, 850))
        self.bg_label = tk.Label(self,image=self.bg_photo, bg="white")
        self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)

    def create_input_fields(self):
        self.home_team = Label(self, text="Home Team", bg="white", font=("Montserrat Bold", 12))
        self.home_team.place(x=90, y=200)
        self.home_team_combobox = ttk.Combobox(self, width=33, values=self.VALID_TEAMS, font=("Montserrat", 15),state="normal")
        self.home_team_combobox.option_add('*TCombobox*Listbox.font', ("Montserrat", 15))
        self.home_team_combobox.place(x=92, y=235, height=40)

        self.visiting_team = Label(self, text="Visiting team", bg="white", font=("Montserrat Bold", 12))
        self.visiting_team.place(x=90, y=320)
        self.visiting_team_combobox = ttk.Combobox(self, width=33, values=self.VALID_TEAMS, font=("Montserrat", 15),state="normal")
        self.visiting_team_combobox.option_add('*TCombobox*Listbox.font', ("Montserrat", 15))
        self.visiting_team_combobox.place(x=92, y=355, height=40)

        self.stadium = Label(self, text="Stadium", bg="white", font=("Montserrat Bold", 12))
        self.stadium.place(x=90, y=440)
        self.stadium_combobox = ttk.Combobox(self, width=33, values=self.STADIUMS, font=("Montserrat", 15),state="normal")
        self.stadium_combobox.option_add('*TCombobox*Listbox.font', ("Montserrat", 15))
        self.stadium_combobox.place(x=92, y=475, height=40)

        self.date = Label(self, text="Date", bg="white", font=("Montserrat Bold", 12))
        self.date.place(x=90, y=560)
        self.date_entry = tk.Entry(self, width=15, font=("Montserrat", 15), relief="solid", highlightthickness=1, highlightcolor="#D3D3D3", highlightbackground="#D3D3D3", borderwidth=0)
        self.date_entry.place(x=92, y=595, height=40)
        self.date_entry.insert(0, "YYYY-MM-DD")
        self.date_entry.config(fg="grey")
        self.date_entry.bind("<FocusIn>", lambda e: self.clear_placeholder(e, self.date_entry, "YYYY-MM-DD"))
        self.date_entry.bind("<FocusOut>", lambda e: self.add_placeholder(e, self.date_entry, "YYYY-MM-DD"))

        self.time = Label(self, text="Time", bg="white", font=("Montserrat Bold", 12))
        self.time.place(x=360, y=560)
        self.time_entry = tk.Entry(self, width=15, font=("Montserrat", 15), relief="solid", highlightthickness=1,highlightcolor="#D3D3D3", highlightbackground="#D3D3D3", borderwidth=0)
        self.time_entry.place(x=362, y=595, height=40)
        self.time_entry.insert(0, "HH:MM AM/PM")
        self.time_entry.config(fg="grey")
        self.time_entry.bind("<FocusIn>", lambda e: self.clear_placeholder(e, self.time_entry, "HH:MM AM/PM"))
        self.time_entry.bind("<FocusOut>", lambda e: self.add_placeholder(e, self.time_entry, "HH:MM AM/PM"))

        start_x, start_y, seat_x, price_x = 600, 190, 810, 910  # Điều chỉnh tọa độ
        tk.Label(self, text="Seats", font=("Montserrat Bold", 13), fg="black", bg="white").place(x=seat_x,y=start_y - 30)
        tk.Label(self, text="Price", font=("Montserrat Bold", 13), fg="black", bg="white").place(x=price_x,y=start_y - 30)

        for i, category in enumerate(self.TICKET_CATEGORIES):
            tk.Label(self, text=f"{category['area']}:", font=("Montserrat Bold", 13),fg="black", bg="white", anchor="w").place(x=start_x, y=start_y + i * 90)

            seat_entry = tk.Entry(self, width=6, font=("Montserrat", 15), relief="solid", highlightthickness=1, highlightcolor="#D3D3D3", highlightbackground="#D3D3D3", borderwidth=0)
            seat_entry.place(x=seat_x, y=start_y + i * 90, height=35)
            self.seat_entries.append(seat_entry)

            price_entry = tk.Entry(self, width=6, font=("Montserrat", 15), relief="solid", highlightthickness=1, highlightcolor="#D3D3D3", highlightbackground="#D3D3D3", borderwidth=0)
            price_entry.place(x=price_x, y=start_y + i * 90, height=35)
            price_entry.insert(0, "")
            price_entry.config(fg="black")
            self.price_entries.append(price_entry)

    def clear_placeholder(self, event, entry, placeholder):  # Xóa placeholder khi người dùng click vào ô nhập liệu
        if entry.get() == placeholder:
            entry.delete(0, tk.END)
            entry.config(fg="#0f2f56")

    def add_placeholder(self, event, entry, placeholder):  # Thêm placeholder nếu ô nhập liệu trống khi người dùng rời khỏi
        if not entry.get():
            entry.insert(0, placeholder)
            entry.config(fg="grey")  # Đổi màu chữ thành màu mờ

    def create_save_button(self):  # Tạo nút Save
        self.add_products_photo = self.controller.load_image("btn_Save.png", (105, 48))
        if self.add_products_photo:
            self.add_product_button = tk.Button(self, image=self.add_products_photo, bd=0, bg="white", relief="flat", cursor="hand2",
                                                command=lambda: AdminProcess_Main.save_match(self) if self.validate_input() else None)
            self.add_product_button.place(x=889, y=650)

    def validate_input(self):
        data = AdminProcess_Main.validate_input(self)
        if not data:
            return False

        for i, category in enumerate(self.TICKET_CATEGORIES):
            price = self.price_entries[i].get().strip()
            seats = self.seat_entries[i].get().strip()

            # Kiểm tra nếu giá bị để trống
            if not price:
                tk.messagebox.showerror("Error", f"Price for {category['area']} must be provided!")
                return False

            # Kiểm tra nếu số ghế bị để trống
            if not seats:
                tk.messagebox.showerror("Error", f"Seats for {category['area']} must be provided!")
                return False

            # Kiểm tra định dạng giá
            if price.startswith("$"):
                price_value = price[1:]
                if not price_value.isdigit() or int(price_value) <= 0:
                    tk.messagebox.showerror("Error",
                                            f"Price for {category['area']} must be a positive integer (e.g., $123 or 123)!")
                    return False
            else:
                if not price.isdigit() or int(price) <= 0:
                    tk.messagebox.showerror("Error",
                                            f"Price for {category['area']} must be a positive integer (e.g., $123 or 123)!")
                    return False

            # Kiểm tra định dạng ghế
            if not seats.isdigit() or int(seats) <= 0:
                tk.messagebox.showerror("Error",
                                        f"Seats for {category['area']} must be a positive integer greater than 0!")
                return False

        return True

    def clear_all_entries(self):#Xóa nội dung của tất cả các ô nhập
        self.date_entry.delete(0, tk.END)
        self.date_entry.insert(0, "YYYY-MM-DD")
        self.date_entry.config(fg="grey")

        self.time_entry.delete(0, tk.END)
        self.time_entry.insert(0, "HH:MM AM/PM")
        self.time_entry.config(fg="grey")

        self.home_team_combobox.set('')
        self.visiting_team_combobox.set('')
        self.stadium_combobox.set('')

        for seat_entry in self.seat_entries:
            seat_entry.delete(0, tk.END)

        for price_entry in self.price_entries:
            price_entry.delete(0, tk.END)

# ====================================  CUSTOMER PAGE  =============================================
class CustomersPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg="white")
        self.controller = controller
        self.create_background()
        self.create_scrollable_area()
        self.load_customers()

    def show(self): #Phương thức được gọi khi trang được hiển thị.
        self.load_customers()
        self.tkraise() # Hiển thị frame

    def create_background(self):
        self.bg_photo = self.controller.load_image("cus_bg.png", (1075, 850))
        self.bg_label = tk.Label(self, image=self.bg_photo, bg="white")
        self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)

        self.search_entry = tk.Entry(self, width=30, font=("Montserrat", 18), relief="solid", highlightthickness=1,highlightcolor="#D3D3D3", highlightbackground="#D3D3D3", borderwidth=0)
        self.search_entry.place(x=235, y=27)
        self.search_entry.insert(0, "Search customers...")
        self.search_entry.config(fg="grey")

        self.search_entry.bind("<FocusIn>", lambda e: self.clear_search_placeholder())
        self.search_entry.bind("<FocusOut>", lambda e: self.add_search_placeholder())
        self.search_entry.bind("<KeyRelease>", lambda e: self.update_search_results())

    def create_scrollable_area(self): #Tạo vùng cuộn chính
        self.canvas = tk.Canvas(self, width=1000, height=696, bg="white", highlightthickness=0)
        self.canvas.place(x=38, y=90)
        self.scrollbar = tk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.scrollbar.place(x=1038, y=90, height=696)
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        self.scrollable_frame = tk.Frame(self.canvas, bg="white")
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.scrollable_frame.bind("<Configure>", self.update_scroll_region)
        self.canvas.bind("<MouseWheel>", self.on_mouse_wheel)
    def update_scroll_region(self, event): #Cập nhật kích thước vùng cuộn
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def on_mouse_wheel(self, event): # Cuộn trang bằng chuột
        self.canvas.yview_scroll(-1 * (event.delta // 120), "units")

    def load_customers(self): #Lấy dữ liệu từ backend và hiển thị lên giao diện
        customers = AdminProcess_Main.get_customers(self)  # Gọi backend để lấy danh sách khách hàng
        self.display_customers(customers)

    def display_customers(self, customers): #Hiển thị danh sách khách hàng lên giao diện
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy() # Xóa nội dung cũ

        columns = 4  # Số cột trong lưới
        card_width = 200
        card_height = 250

        for i, customer in enumerate(customers):  # Tạo các frame cho mỗi user
            frame = tk.Frame(self.scrollable_frame, bd=2, relief="ridge", padx=10, pady=10, bg="white",width=card_width, height=card_height, cursor="hand2")
            frame.grid(row=i // columns, column=i % columns, padx=15, pady=15, sticky="nsew")
            frame.pack_propagate(False)

            avatar_image = self.controller.load_image("avatar.png", (100, 100))  # Load avatar image
            avatar_label = tk.Label(frame, image=avatar_image, bg="white", cursor="hand2")
            avatar_label.image = avatar_image
            avatar_label.pack(pady=10)

            username_label = tk.Label(frame, text=customer.get("username", "N/A"), font=("Arial", 12, "bold"),bg="white", cursor="hand2")
            username_label.pack()
            email_label = tk.Label(frame, text=customer.get("email", "N/A"), font=("Arial", 10), bg="white",cursor="hand2")
            email_label.pack()

            # Gán sự kiện click vào frame và labels
            frame.bind("<Button-1>", lambda e, c=customer: self.show_tickets(c))
            avatar_label.bind("<Button-1>", lambda e, c=customer: self.show_tickets(c))
            username_label.bind("<Button-1>", lambda e, c=customer: self.show_tickets(c))
            email_label.bind("<Button-1>", lambda e, c=customer: self.show_tickets(c))

            for widget in [frame, avatar_label, username_label, email_label]: # Bind sự kiện cuộn chuột cho từng widget con
                widget.bind("<MouseWheel>", self.on_mouse_wheel)

    def clear_search_placeholder(self): #Xóa placeholder khi người dùng click vào ô nhập liệu
        if self.search_entry.get() == "Search customers...":
            self.search_entry.delete(0, tk.END)
            self.search_entry.config(fg="black")

    def add_search_placeholder(self): #Thêm placeholder nếu ô nhập liệu trống khi người dùng rời khỏi
        if not self.search_entry.get():
            self.search_entry.insert(0, "Search customers...")
            self.search_entry.config(fg="grey")

    def update_search_results(self): #Cập nhật danh sách khách hàng dựa trên từ khóa tìm kiếm
        customers = AdminProcess_Main.get_customers(self) # Lấy danh sách tất cả khách hàng từ backend

        for widget in self.scrollable_frame.winfo_children():
            widget.destroy() # Xóa nội dung cũ trong scrollable_frame

        search_text = self.search_entry.get() # Lấy từ khóa tìm kiếm và lọc danh sách khách hàng
        filtered_customers = AdminProcess_Main.search_customers(customers, search_text)

        self.display_customers(filtered_customers)  # Hiển thị danh sách đã lọc

    def show_tickets(self, customer):
        username = customer.get("username")
        tickets = AdminProcess_Main.get_tickets_by_customer(username)  # Lấy toàn bộ dữ liệu từ backend

        popup = tk.Toplevel(self)
        popup.title(f"{username}'s Tickets")
        popup.geometry("800x600")
        popup.configure(bg="white")
        popup.resizable(False, False)

        # Đặt vị trí giữa cửa sổ chính
        self.update_idletasks()
        x_position = self.winfo_rootx() + (self.winfo_width() // 2) - (800 // 2)
        y_position = self.winfo_rooty() + (self.winfo_height() // 2) - (600 // 2)
        popup.geometry(f"+{x_position}+{y_position}")

        title_label = tk.Label(popup, text=f"{username.upper()}’S TICKETS", font=("Montserrat Black", 20), bg="white", fg="#0f2f56")
        title_label.pack(pady=10)

        if tickets:
            canvas = tk.Canvas(popup, bg="white", highlightthickness=0) # Tạo khung cuộn nếu có nhiều lần mua vé
            scrollbar = ttk.Scrollbar(popup, orient="vertical", command=canvas.yview)
            scrollable_frame = tk.Frame(canvas, bg="white")
            scrollable_frame.bind("<Configure>",lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
            canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
            canvas.configure(yscrollcommand=scrollbar.set)
            canvas.pack(side="left", fill="both", expand=True)
            scrollbar.pack(side="right", fill="y")
            canvas.bind("<MouseWheel>", lambda e: canvas.yview_scroll(-1 * (e.delta // 120), "units"))

            for idx, ticket in enumerate(tickets, start=1):
                match_name = ticket.get("match_name")
                date = ticket.get("date")
                time = ticket.get("time")
                total = ticket.get("total")
                stadium = ticket.get("stadium")  # Lấy thông tin sân vận động

                # Khung chứa từng lần mua vé
                ticket_frame = tk.Frame(scrollable_frame, bg="white", bd=2, relief="solid")
                ticket_frame.pack(pady=10, padx=10, fill="x")

                match_label = tk.Label(ticket_frame, text=match_name, font=("Montserrat", 14, "bold"), bg="white")
                match_label.pack()

                info_frame = tk.Frame(ticket_frame, bg="white")
                info_frame.pack(pady=5)

                date_part, time_part = time.split(", ") # Tách ngày và thời gian bằng dấu ","

                info_text = f"{date_part}, {time_part}, {stadium}"
                info_label = tk.Label(info_frame, text=info_text, font=("Montserrat", 12), bg="white")
                info_label.pack(anchor="w")  # Căn trái

                total_label = tk.Label(ticket_frame, text=f"Total: {total}", font=("Montserrat", 16, "bold"), bg="white")
                total_label.pack(pady=5)

                table_frame = tk.Frame(ticket_frame, bg="white") # Bảng hiển thị chi tiết vé
                table_frame.pack(pady=10)

                headers = ["Section", "Quantity", "Price (USD)", "Subtotal"]
                for col, header in enumerate(headers):
                    header_label = tk.Label(table_frame, text=header, font=("Montserrat", 11, "bold"), fg="white",bg="#0F2F56", width=15)
                    header_label.grid(row=0, column=col, padx=5, pady=5)

                for row, seat_info in enumerate(ticket.get("tickets", []), start=1):
                    section_label = tk.Label(table_frame, text=seat_info.get("area", ""), font=("Montserrat", 11),fg="black", bg="white", width=17)
                    section_label.grid(row=row, column=0, padx=5, pady=5)

                    quantity_label = tk.Label(table_frame, text=seat_info.get("quantity", ""), font=("Montserrat", 11),fg="black", bg="white", width=17)
                    quantity_label.grid(row=row, column=1, padx=5, pady=5)
                    price_label = tk.Label(table_frame, text=seat_info.get("price", ""), font=("Montserrat", 11),fg="black", bg="white", width=17)
                    price_label.grid(row=row, column=2, padx=5, pady=5)
                    subtotal_label = tk.Label(table_frame, text=seat_info.get("subtotal", ""), font=("Montserrat", 11),fg="black", bg="white", width=17)
                    subtotal_label.grid(row=row, column=3, padx=5, pady=5)

                    for widget in [section_label, quantity_label, price_label, subtotal_label]:# Bind sự kiện cuộn chuột cho các label trong bảng
                        widget.bind("<MouseWheel>", lambda e: canvas.yview_scroll(-1 * (e.delta // 120), "units"))

                for widget in [ticket_frame, match_label, info_frame, info_label, total_label, table_frame]: # Bind sự kiện cuộn chuột cho các widget con
                    widget.bind("<MouseWheel>", lambda e: canvas.yview_scroll(-1 * (e.delta // 120), "units"))
        else:
            tk.Label(popup, text="No tickets found.", font=("Montserrat", 12), fg="black", bg="white").pack()
