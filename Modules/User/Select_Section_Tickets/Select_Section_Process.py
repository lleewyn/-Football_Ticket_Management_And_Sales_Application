import Modules.User.Landing_Page.Main_Page_View as usmv
import Modules.User.My_Tickets.My_Tickets_View as mtv
import Modules.User.User_Information.User_Information_View as uiv
import Modules.Login.Login_View as lg
import Modules.User.Select_Section_Tickets.Select_Section_View as selv
from pymongo import MongoClient
import os
from tkinter import messagebox, PhotoImage
import tkinter as tk
from pathlib import Path

MONGO_URI = os.getenv("MONGO_URI")
DATABASE_NAME = os.getenv("MONGO_DATABASE")
client = MongoClient(MONGO_URI)
db = client[DATABASE_NAME]
matches_collection = db["Teams"]  # Chọn collection
users_collection = db["Users"]

class SelectSection_process:

    @staticmethod
    def home_button_handle(obj):
        obj.window.destroy()
        new_window = tk.Tk()
        app = usmv.MainPage_View(new_window, obj.user_info)
        app.window.mainloop()

    @staticmethod
    def my_tickets_button_handle(obj):
        obj.window.destroy()
        new_window = tk.Tk()
        app = mtv.MyTickets_View(new_window, obj.user_info)
        app.window.mainloop()

    @staticmethod
    def user_info_button_handle(obj):
        obj.window.destroy()
        new_window = tk.Tk()
        app = uiv.UserInformation_View(new_window, obj.user_info)
        app.window.mainloop()

    @staticmethod
    def back_login_button_handle(obj):
        confirm = messagebox.askyesno(
            title="Confirm Logout",
            message="Are you sure you want to log out?",
            parent=obj.window)
        if confirm:
            obj.window.destroy()
            app = lg.Login_View()
            app.window.mainloop()
        else:
            return

    @staticmethod
    def payment_button_handle(view):
        print("Payment button clicked!")  # Debug: Kiểm tra xem phương thức có được gọi không
        BASE_DIR = Path(__file__).parent.parent.parent.parent
        view.assets_path = BASE_DIR / 'Images' / 'SelectSectionTickets'

        ticket_info = []
        has_error = False  # Biến kiểm tra xem có lỗi nào không

        for i, entry in enumerate(view.ticket_entries):
            value = entry.get()
            if not value or value == "0":
                value = "0"
                entry.delete(0, tk.END)  # Xóa giá trị trong ô nhập liệu
                entry.insert(0, "0")  # Đặt giá trị mặc định là "0"
                entry.config(bg="white")  # Đặt lại màu nền
                ticket_info.append(value)
                continue

            # Kiểm tra xem giá trị nhập vào có hợp lệ không
            if not value.isdigit():
                messagebox.showerror("Error", f"Please enter a valid number for {view.match['tickets'][i]['area']}.")
                entry.config(bg="#FFCCCC")  # Đánh dấu ô nhập liệu sai bằng màu nền đỏ nhạt
                entry.focus_set()  # Chuyển focus đến ô nhập liệu sai
                has_error = True
            elif int(value) > view.match['tickets'][i]['available_seats']:  # Nếu số lượng vé vượt quá số lượng còn lại
                messagebox.showerror("Error",
                                     f"Not enough available seats for {view.match['tickets'][i]['area']}. Only {view.match['tickets'][i]['available_seats']} seats left.")
                entry.config(bg="#FFCCCC")
                entry.focus_set()  # Chuyển focus đến ô nhập liệu sai
                has_error = True
            else:
                entry.config(bg="white")  # Đặt lại màu nền nếu nhập liệu đúng
                ticket_info.append(value)

        if has_error: #Nếu có lỗi, dừng lại và không tiếp tục
            return

        if all(value == "0" for value in ticket_info): #Kiểm tra xem tất cả các ô nhập liệu có giá trị là 0 không
            messagebox.showwarning("Warning", "You have not selected any tickets.")
            return  # Dừng lại và không tiếp tục

        # Tạo cửa sổ popup
        view.popup = tk.Toplevel(view.window)
        view.popup.title("Confirm Payment")
        popup_width = 600
        popup_height = 715
        main_window_width = view.window.winfo_width()
        main_window_height = view.window.winfo_height()
        main_window_x = view.window.winfo_x()
        main_window_y = view.window.winfo_y()
        popup_x = main_window_x + (main_window_width - popup_width) // 2
        popup_y = main_window_y + (main_window_height - popup_height) // 2
        view.popup.geometry(f"{popup_width}x{popup_height}+{popup_x}+{popup_y}")

        view.popup.resizable(False, False)
        view.popup.configure(bg="white")
        view.popup.attributes('-topmost', True)  # Đảm bảo popup luôn hiển thị trên cùng

        Title_popup = tk.Label(view.popup, text="Review Your Order".upper(), font=("Montserrat Black", 30),
                               fg="#0F2F56", bg="white")
        Title_popup.pack(padx=5, pady=15)

        # Hiển thị thông tin trận đấu
        match_title = tk.Label(view.popup, text=f"{view.match['home_team']} vs {view.match['away_team']}",bg='white',font=("Inter", 19, "bold"),fg='black',)
        match_title.pack(pady=5)

        match_info = tk.Label(view.popup,text=f"{view.match['date']} at {view.match['time']} - {view.match['stadium']}",font=("Inter", 13),fg="gray",bg="white")
        match_info.pack(pady=5)

        view.selected_img = PhotoImage(file=view.assets_path / 'Selected tickets.png')
        view.selected = tk.Label(view.popup, image=view.selected_img, background="white")
        view.selected.pack(padx=5, pady=20)

        # Hiển thị thông tin vé và tính tổng giá tiền
        total_price = 0
        ticket_details = []  # Lưu thông tin vé để hiển thị

        for i, ticket in enumerate(view.match['tickets']):
            quantity = int(ticket_info[i])  # Lấy số lượng vé từ ô Entry
            if quantity > 0:  # Chỉ hiển thị và tính toán nếu số lượng vé > 0
                price = int(ticket['price'].replace("$", ""))  # Chuyển đổi giá vé từ chuỗi sang số
                subtotal = quantity * price  # Tính tổng giá tiền cho loại vé này
                total_price += subtotal  # Cộng vào tổng giá tiền
                # Thêm thông tin vé vào danh sách để hiển thị
                ticket_details.append(f"{ticket['area']:<20} {quantity:>10} tickets x ${price:<5} {subtotal:>30}")

        for detail in ticket_details:
            ticket_label = tk.Label(view.popup,text=detail,font=("Inter", 13),bg="white")
            ticket_label.pack(pady=10)

        # Hiển thị tổng giá tiền
        total_label = tk.Label(view.popup,text=f"Total: ${total_price}",font=("Inter", 22, "bold"), bg="white",fg='#0F2F56')
        total_label.pack(pady=15)

        # Thêm nút Confirm và Cancel
        view.confirm_button_img = PhotoImage(file=view.assets_path / 'ConfirmPayment.png')
        view.confirm_button = tk.Button(view.popup, image=view.confirm_button_img,bg="white", borderwidth=0,highlightthickness=0, cursor="hand2",
                                                    command=lambda: SelectSection_process.confirm_payment(view, ticket_info, total_price,view.match_id))
        view.confirm_button.pack(side=tk.LEFT, padx=30, pady=10)

        view.cancel_button_img = PhotoImage(file=view.assets_path / 'Cancel.png')
        view.cancel_button = tk.Button(view.popup, image=view.cancel_button_img,bg="white", borderwidth=0, highlightthickness=0, cursor="hand2",
                                                    command=view.popup.destroy)
        view.cancel_button.pack(side=tk.RIGHT, padx=30, pady=10)

    @staticmethod
    def confirm_payment(view, ticket_info, total_price, match_id):
        print(f"Confirm payment for match_id: {match_id}")  # Debug
        print(f"Original match data: {view.match}")  # Debug
        # Lưu thông tin vé vào MongoDB
        match_info = {
            "home_team": view.match['home_team'],
            "away_team": view.match['away_team'],
            "date": view.match['date'],
            "time": view.match['time'],
            "stadium": view.match['stadium'],
            "total": f"${total_price}",
            "tickets": []
        }

        for i, ticket in enumerate(view.match['tickets']):
            if ticket_info[i] and int(ticket_info[i]) > 0:
                ticket_detail = {
                    "area": ticket['area'],
                    "quantity": int(ticket_info[i]),
                    "price": f"${int(ticket['price'].replace('$', ''))}",
                    "subtotal": f"${int(ticket_info[i]) * int(ticket['price'].replace('$', ''))}"
                }
                match_info["tickets"].append(ticket_detail)

                # Cập nhật số lượng ghế còn lại trong mảng matches
                result = matches_collection.update_one(
                    {"_id": match_id},  # Tìm tài liệu bằng _id
                    {
                        "$inc": {
                            "matches.$[match].tickets.$[ticket].available_seats": -int(ticket_info[i])
                        }
                    },
                    array_filters=[
                        {
                            "match.date": view.match['date'],
                            "match.time": view.match['time'],
                            "match.home_team": view.match['home_team'],
                            "match.away_team": view.match['away_team']
                        },
                        {"ticket.area": ticket['area']}
                    ]
                )

                # Debug: In ra kết quả cập nhật
                print(f"Updated {result.modified_count} document(s) for ticket area: {ticket['area']}")

        print(f"Match info to be saved: {match_info}")

        result = users_collection.update_one(
            {"username": view.user_info['username']},
            {"$push": {"match_info": match_info}}
        )

        print(f"Update result for users_collection: {result.modified_count} document(s) updated.")

        updated_match = SelectSection_process.fetch_updated_match(match_id, view.match)
        # Đóng cửa sổ popup xác nhận thanh toán
        view.popup.destroy()

        # Hiển thị popup thông báo thanh toán thành công
        success_popup = tk.Toplevel(view.window)
        success_popup.title("Payment Successful")
        popup_width = 300
        popup_height = 150

        # Lấy kích thước và vị trí của cửa sổ chính
        main_window_width = view.window.winfo_width()
        main_window_height = view.window.winfo_height()
        main_window_x = view.window.winfo_x()
        main_window_y = view.window.winfo_y()

        # Tính toán vị trí để đặt popup ở giữa màn hình chính
        popup_x = main_window_x + (main_window_width - popup_width) // 2
        popup_y = main_window_y + (main_window_height - popup_height) // 2

        # Đặt vị trí và kích thước của popup
        success_popup.geometry(f"{popup_width}x{popup_height}+{popup_x}+{popup_y}")
        success_popup.resizable(0, 0)
        success_popup.configure(bg="white")
        success_popup.attributes('-topmost', True)

        success_label = tk.Label(
            success_popup,
            text="Payment Successful!",
            font=("Montserrat", 18, "bold"),
            bg="white",
            fg='green'
        )
        success_label.pack(pady=20)

        ok_button = tk.Button(
            success_popup,
            text="OK",
            bg="#0F2F56",
            fg="white",
            font=("Montserrat", 12),
            command=lambda: [
                success_popup.destroy(),
                SelectSection_process.clear_entries(view),
                SelectSection_process.reload_select_section_tickets_view(view, updated_match)
            ]        )
        ok_button.pack(pady=10)

    @staticmethod
    def clear_entries(view):
        """Xóa các giá trị trong các ô nhập liệu"""
        for entry in view.ticket_entries:
            entry.delete(0, tk.END)

    @staticmethod
    def fetch_updated_match(match_id, current_match):
        """Lấy dữ liệu trận đấu mới nhất từ MongoDB"""
        match_data = matches_collection.find_one(
            {"_id": match_id},
            {'_id': 0, 'matches': 1}
        )
        if match_data and "matches" in match_data:
            for match in match_data["matches"]:
                if (match["date"] == current_match["date"] and
                        match["time"] == current_match["time"] and
                        match["home_team"] == current_match["home_team"] and
                        match["away_team"] == current_match["away_team"]):
                    print(f"Updated match data: {match}")
                    return match
        print("Could not find updated match data, returning original match.")
        return current_match

    @staticmethod
    def reload_select_section_tickets_view(view, updated_match): #Mở lại trang SelectSection_View với dữ liệu đã cập nhật
        print(f"Reloading SelectSection_View with team: {view.team_name}, match: {updated_match}")  # Debug
        view.window.destroy()
        new_window = tk.Tk()
        app = selv.SelectSection_View( new_window,view.team_name,updated_match, view.user_info,match_id=view.match_id)
        app.display_match_info()
        new_window.mainloop()

