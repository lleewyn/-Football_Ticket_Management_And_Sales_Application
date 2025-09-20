from tkinter import messagebox
from pymongo import MongoClient
import os
from dotenv import load_dotenv
from pathlib import Path
from datetime import datetime
import Modules.Login.Login_View as lg

# Kết nối MongoDB
BASE_DIR = Path(__file__).resolve().parent.parent # Đường dẫn đến thư mục gốc của dự án
dotenv_path = BASE_DIR / ".env" # Đường dẫn đến file .env
load_dotenv(dotenv_path) # Load biến môi trường từ file .env
MONGO_URI = os.getenv("MONGO_URI") # Kiểm tra biến môi trường
DATABASE_NAME = os.getenv("MONGO_DATABASE")
client = MongoClient(MONGO_URI) # Kết nối MongoDB
db = client[DATABASE_NAME]
collection = db["Teams"]
user_collection = db['Users']


class AdminProcess_Main:
    @staticmethod
    def back_login(obj):
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

    # ==================================  XỬ LÝ DASHBOARD  ===================================================
    @staticmethod
    def get_team_revenue():  # Tính tổng doanh thu từ vé đã bán cho từng đội bóng.
        teams = [
            "Chelsea FC", "Arsenal FC", "Manchester City FC",
            "Liverpool FC", "Manchester United FC", "Tottenham Hotspur FC"]

        team_revenue = {team: 0 for team in teams}  # đếm tổng doanh thu cho từng đội
        users = user_collection.find({"match_info": {"$exists": True}})  # Lấy tất cả người dùng từ collection Users

        for user in users:
            for match in user.get("match_info", []):
                home_team = match.get("home_team")
                away_team = match.get("away_team")
                total_str = str(match.get("total", "0")).replace("$", "").strip()
                try:
                    total = int(total_str)
                except ValueError:
                    print(f"Lỗi chuyển đổi total: {total_str}")
                    total = 0

                if home_team in team_revenue:  # Cộng doanh thu cho home_team nếu nó nằm trong danh sách teams
                    team_revenue[home_team] += total
                if away_team in team_revenue:  # Cộng doanh thu cho away_team nếu nó nằm trong danh sách teams
                    team_revenue[away_team] += total
        return team_revenue

    @staticmethod
    def get_total_revenue(): #Tính tổng doanh thu từ tất cả các trận đấu đã được mua vé
        total_revenue = 0
        users = user_collection.find({"match_info": {"$exists": True}})  # Lấy tất cả người dùng từ collection Users

        for user in users:  # Duyệt qua từng người dùng và các trận đấu họ đã mua
            for match in user.get("match_info", []):
                total_str = str(match.get("total", "0")).replace("$", "").strip()
                try:
                    total_revenue += int(total_str)
                except ValueError:
                    print(f"Lỗi chuyển đổi total: {total_str}")
        return total_revenue

    # ==================================== XỬ LÝ PRODUCT + INVOICE ================================================
    @staticmethod
    def load_matches(obj):  # Lấy danh sách trận đấu từ MongoDB và hiển thị trên giao diện
        # Sử dụng obj để xóa nội dung cũ trong scrollable_frame
        for widget in obj.scrollable_frame.winfo_children():
            widget.destroy()

        data = list(collection.find())
        matches_dict = {}

        for team_data in data:
            for match in team_data.get("matches", []):
                match_key = (match.get("date"), match.get("time"), match.get("home_team"), match.get("away_team"))
                if match_key not in matches_dict:
                    total_revenue = AdminProcess_Main.calculate_total_revenue(match.get("date"), match.get("time"),
                                                                              match.get("home_team"),
                                                                              match.get("away_team"))
                    available_seats_by_category = {}

                    # Lấy danh sách tickets từ dữ liệu gốc
                    tickets = match.get("tickets", [])

                    for ticket in tickets:
                        area = ticket.get("area", "Unknown")  # Lấy tên khu vực, nếu không có thì đặt là 'Unknown'

                        # Lấy số lượng ghế trống và đảm bảo dữ liệu là số nguyên
                        available_seats = ticket.get("available_seats", 0)
                        if isinstance(available_seats, dict) and "$numberInt" in available_seats:
                            try:
                                available_seats = int(available_seats["$numberInt"])
                            except ValueError:
                                available_seats = 0  # Nếu lỗi, đặt là 0
                        elif isinstance(available_seats, str):  # Nếu là chuỗi, kiểm tra và chuyển đổi
                            try:
                                available_seats = int(available_seats.strip())
                            except ValueError:
                                available_seats = 0  # Nếu lỗi, đặt là 0

                        available_seats_by_category[area] = available_seats  # Gán số ghế trống vào danh mục

                    # Lưu thông tin trận đấu, bao gồm cả tickets
                    matches_dict[match_key] = {
                        "_id": team_data["_id"],
                        "date": match.get("date", "N/A"),
                        "time": match.get("time", "N/A"),
                        "home_team": match.get("home_team", "N/A"),
                        "away_team": match.get("away_team", "N/A"),
                        "stadium": match.get("stadium", "N/A"),
                        "total": f"${total_revenue}",
                        "available_seats_by_category": available_seats_by_category,
                        "tickets": tickets  # Thêm trường tickets vào đây
                    }

        # Sử dụng obj để gán danh sách trận đấu vào unique_matches
        obj.unique_matches = list(matches_dict.values())

    @staticmethod
    def validate_and_format_price(new_price, old_price):
        new_price = new_price.strip()
        if not new_price:  # If the input is empty, return the old price
            return old_price

        if new_price.startswith("$") and new_price[1:].isdigit():
            price = new_price
        elif new_price.isdigit():
            price = f"${new_price}"
        else:
            raise ValueError("Price must be a positive integer with optional $ prefix (e.g., $250 or 250)!")

        try:
            price_int = int(price[1:] if price.startswith("$") else price)
            if price_int <= 0:
                raise ValueError("Price must be a positive integer greater than 0!")
        except ValueError as e:
            if "positive integer greater than 0" in str(e):
                raise
            raise ValueError("Price must be a positive integer with optional $ prefix (e.g., $250 or 250)!")
        return price

    @staticmethod
    def validate_and_format_seats(new_seats, old_seats):
        new_seats = new_seats.strip()
        if not new_seats:  # If the input is empty, return the old seats
            return int(old_seats)

        try:
            seats = int(new_seats)
            if seats <= 0:
                raise ValueError("Number of seats must be a positive integer greater than 0!")
            if seats > 100000:
                raise ValueError("Number of seats cannot exceed 100,000!")
            return seats
        except ValueError:
            raise ValueError("Number of seats must be a positive integer!")

    @staticmethod
    def update_match(obj, match, new_data, edit_window=None):
        # Function to validate date format
        def is_valid_date(date_str):
            import re
            from calendar import monthrange
            pattern = r"^\d{4}-\d{2}-\d{2}$"  # Format: YYYY-MM-DD
            if not re.match(pattern, date_str):
                return False, "Date must be in YYYY-MM-DD format, e.g., 2025-04-15."
            try:
                year, month, day = map(int, date_str.split("-"))
                if year < datetime.now().year:
                    return False, "Year cannot be earlier than the current year."
                if not (1 <= month <= 12):
                    return False, "Month must be between 1 and 12."
                max_days = monthrange(year, month)[1]  # Maximum days in the month
                if not (1 <= day <= max_days):
                    return False, f"Day must be between 1 and {max_days} for {month}/{year}."
                return True, ""
            except ValueError:
                return False, "Invalid date."

        def is_valid_time(time_str):
            import re
            pattern = r"^(1[0-2]|0?[1-9]):([0-5][0-9]) (AM|PM)$"  # Format: HH:MM AM/PM
            if not re.match(pattern, time_str):
                return False, "Time must be in HH:MM AM/PM format, e.g., 08:30 PM."
            try:
                hour, minute, period = re.match(r"^(\d+):(\d+) (AM|PM)$", time_str).groups()
                hour, minute = int(hour), int(minute)
                if not (1 <= hour <= 12):
                    return False, "Hour must be between 1 and 12."
                if not (0 <= minute <= 59):
                    return False, "Minute must be between 0 and 59."
                return True, ""
            except ValueError:
                return False, "Invalid time."

        if "date" in new_data:
            date_valid, date_error = is_valid_date(new_data["date"])
            if not date_valid:
                messagebox.showerror("Error", date_error)
                if edit_window:
                    edit_window.lift()
                return
            new_date = new_data["date"]
        else:
            new_date = match["date"]

        if "time" in new_data:
            time_valid, time_error = is_valid_time(new_data["time"])
            if not time_valid:
                messagebox.showerror("Error", time_error)
                if edit_window:
                    edit_window.lift()
                return
            new_time = new_data["time"]
        else:
            new_time = match["time"]

        if "date" in new_data or "time" in new_data:
            current_datetime = datetime.now()
            new_match_datetime = datetime.strptime(f"{new_date} {new_time}", "%Y-%m-%d %I:%M %p")
            if new_match_datetime < current_datetime:
                messagebox.showerror("Error", "Date and time must be in the future!")
                if edit_window:
                    edit_window.lift()
                return

        if "tickets" in new_data:
            updated_tickets = []
            for ticket in new_data["tickets"]:
                area = ticket["area"]
                new_price = ticket["new_price"]
                new_seats = ticket["new_seats"]
                old_price = ticket["old_price"]
                old_seats = ticket["old_seats"]

                try:
                    # Validate and format price
                    price = AdminProcess_Main.validate_and_format_price(new_price, old_price)

                    # Validate and format seats
                    seats = AdminProcess_Main.validate_and_format_seats(new_seats, old_seats)

                    updated_tickets.append({
                        "area": area,
                        "price": price,
                        "available_seats": seats
                    })
                except ValueError as e:
                    messagebox.showerror("Error", f"Error in ticket category '{area}': {str(e)}")
                    if edit_window:
                        edit_window.lift()
                    return
        else:
            updated_tickets = match.get("tickets", [])

        # Update data in MongoDB
        for team_data in collection.find():
            updated_matches = []
            modified = False

            for m in team_data.get("matches", []):
                if (
                        m.get("date") == match["date"] and
                        m.get("time") == match["time"] and
                        m.get("home_team") == match["home_team"] and
                        m.get("away_team") == match["away_team"]
                ):
                    updated_matches.append({
                        "date": new_date,
                        "time": new_time,
                        "stadium": new_data.get("stadium", m["stadium"]),
                        "home_team": m["home_team"],
                        "away_team": m["away_team"],
                        "tickets": updated_tickets
                    })
                    modified = True
                else:
                    updated_matches.append(m)

            if modified:
                collection.update_one(
                    {"_id": team_data["_id"]},
                    {"$set": {"matches": updated_matches}})

        messagebox.showinfo("Success", "All matches have been updated successfully!")
        if edit_window:
            edit_window.destroy()

        # Tải lại danh sách và cập nhật self.all_matches
        AdminProcess_Main.load_matches(obj)
        obj.all_matches = obj.unique_matches.copy()
        obj.sort_matches(None)

    @staticmethod
    def delete_match(obj, match, edit_window=None): #Delete all matches with the same details from MongoDB
        confirm = messagebox.askyesno("Confirm",f"Are you sure you want to delete all matches between {match['home_team']} and {match['away_team']}?")
        if edit_window:
            edit_window.lift()

        if not confirm:
            return

        for team_data in collection.find():
            updated_matches = [m for m in team_data.get("matches", []) if not (
                    m.get("date") == match["date"] and
                    m.get("time") == match["time"] and
                    m.get("home_team") == match["home_team"] and
                    m.get("away_team") == match["away_team"])]

            if len(updated_matches) < len(team_data.get("matches", [])):
                collection.update_one(
                    {"_id": team_data["_id"]},
                    {"$set": {"matches": updated_matches}})

        messagebox.showinfo("Success", "All matches have been deleted successfully!")
        if edit_window:
            edit_window.lift()

        # Tải lại danh sách và hiển thị ngay lập tức
        AdminProcess_Main.load_matches(obj)
        obj.sort_matches(None)  # Gọi sort_matches để hiển thị lại danh sách

    @staticmethod
    def save_match(obj):
        from Modules.Admin.Admin_View import ProductsPage

        match_date = obj.date_entry.get().strip()
        match_time = obj.time_entry.get().strip()
        home_team = obj.home_team_combobox.get().strip()
        away_team = obj.visiting_team_combobox.get().strip()
        stadium = obj.stadium_combobox.get().strip()

        # Check for required fields
        if not all([match_date, match_time, home_team, away_team, stadium]):
            messagebox.showerror("Error", "Please fill in all required fields!")
            return
        if not match_date or not match_time or not home_team or not away_team or not stadium:
            messagebox.showerror("Error", "Fields cannot be empty or contain only whitespace!")
            return

        if home_team == away_team:  # Check if home team and away team are different
            messagebox.showerror("Error", "Home team and away team cannot be the same!")
            return

        def is_valid_date(date_str):
            import re
            from calendar import monthrange
            pattern = r"^\d{4}-\d{2}-\d{2}$"
            if not re.match(pattern, date_str):
                return False, "Date must be in YYYY-MM-DD format, e.g., 2025-04-15."
            try:
                year, month, day = map(int, date_str.split("-"))
                if year < datetime.now().year:
                    return False, "Year cannot be earlier than the current year."
                if not (1 <= month <= 12):
                    return False, "Month must be between 1 and 12."
                max_days = monthrange(year, month)[1]
                if not (1 <= day <= max_days):
                    return False, f"Day must be between 1 and {max_days} for {month}/{year}."
                return True, ""
            except ValueError:
                return False, "Invalid date."

        def is_valid_time(time_str):
            import re
            pattern = r"^(1[0-2]|0?[1-9]):([0-5][0-9]) (AM|PM)$"
            if not re.match(pattern, time_str):
                return False, "Time must be in HH:MM AM/PM format, e.g., 08:30 PM."
            try:
                hour, minute, period = re.match(r"^(\d+):(\d+) (AM|PM)$", time_str).groups()
                hour, minute = int(hour), int(minute)
                if not (1 <= hour <= 12):
                    return False, "Hour must be between 1 and 12."
                if not (0 <= minute <= 59):
                    return False, "Minute must be between 0 and 59."
                return True, ""
            except ValueError:
                return False, "Invalid time."

        date_valid, date_error = is_valid_date(match_date)
        if not date_valid:
            messagebox.showerror("Error", date_error)
            return

        time_valid, time_error = is_valid_time(match_time)
        if not time_valid:
            messagebox.showerror("Error", time_error)
            return

        current_datetime = datetime.now()
        match_datetime = datetime.strptime(f"{match_date} {match_time}", "%Y-%m-%d %I:%M %p")
        if match_datetime < current_datetime:
            messagebox.showerror("Error", "Date and time must be in the future!")
            return

        ticket_data = []
        for i, category in enumerate(obj.TICKET_CATEGORIES):
            seats = obj.seat_entries[i].get().strip()
            price = obj.price_entries[i].get().strip()
            try:
                seats = int(seats)
                if seats <= 0:
                    messagebox.showerror("Error", "Number of seats must be a positive integer greater than 0!")
                    return
                if seats > 100000:
                    messagebox.showerror("Error", "Number of seats cannot exceed 100,000!")
                    return
            except ValueError:
                messagebox.showerror("Error", "Number of seats must be an integer!")
                return

            if not price:
                continue  # Bỏ qua khu vực này nếu giá để trống

            if price.startswith("$"):
                formatted_price = price  # Giữ nguyên nếu đã có $
            else:
                formatted_price = f"${price}"  # Thêm $ nếu chưa có

            ticket_data.append({
                "area": category["area"],
                "price": formatted_price,  # Lưu giá đã định dạng
                "available_seats": seats })

        if not ticket_data: # Kiểm tra xem có ít nhất một khu vực được thêm không
            messagebox.showerror("Error", "At least one ticket category must have a valid price!")
            return

        # Save to database
        match_data = {
            "date": match_date,
            "time": match_time,
            "home_team": home_team,
            "away_team": away_team,
            "stadium": stadium,
            "tickets": ticket_data }

        if collection.find_one({"team": home_team}):
            collection.update_one({"team": home_team}, {"$push": {"matches": match_data}})

        if collection.find_one({"team": away_team}):
            collection.update_one({"team": away_team}, {"$push": {"matches": match_data}})

        # Clear all input fields by calling the new method
        obj.clear_all_entries()

        messagebox.showinfo("Success", f"Match between {home_team} and {away_team} has been saved successfully!")

        # Chuyển về trang ProductsPage và làm mới danh sách
        obj.controller.show_page(ProductsPage)

    @staticmethod
    def search_matches(unique_matches, search_text):  # Lọc danh sách trận đấu dựa trên từ khóa tìm kiếm
        search_text = search_text.strip().lower()
        if search_text == "search matches...":
            search_text = ""

        filtered_matches = []
        for match in unique_matches:  # Lọc danh sách trận đấu
            if (search_text in match["date"].lower() or
                    search_text in match["home_team"].lower() or
                    search_text in match["away_team"].lower() or
                    search_text in match.get("stadium", "").lower() or  # Dùng .get() để tránh lỗi nếu không có stadium
                    search_text in match.get("total", "").lower()):  # Tìm kiếm trong cột total
                filtered_matches.append(match)
        return filtered_matches
    @staticmethod
    def sort_products(matches, sort_option):  # này của trang Product Page , Sắp xếp danh sách trận đấu trong ProductsPage dựa trên tùy chọn.
        def is_valid_date(date_str):# Hàm kiểm tra định dạng ngày
            import re
            pattern = r"^\d{4}-\d{2}-\d{2}$"
            if not re.match(pattern, date_str):
                return False
            try:
                year, month, day = map(int, date_str.split("-"))
                if not (1 <= month <= 12):
                    return False
                if not (1 <= day <= 31):
                    return False
                return True
            except ValueError:
                return False

        def is_valid_time(time_str):
            import re
            pattern = r"^(1[0-2]|0?[1-9]):([0-5][0-9]) (AM|PM)$"
            if not re.match(pattern, time_str):
                return False
            return True

        # Hàm chuyển đổi ngày và thời gian thành datetime để so sánh
        def get_datetime(match):
            try:
                date_str = match['date']
                time_str = match['time']
                if not is_valid_date(date_str) or not is_valid_time(time_str):
                    return datetime.max
                return datetime.strptime(f"{date_str} {time_str}", "%Y-%m-%d %I:%M %p")
            except (ValueError, KeyError) as e:
                print(f"Error parsing datetime: {e} for match {match['home_team']} vs {match['away_team']}")
                return datetime.max

        if sort_option == "Sort by Date and Time":
            matches.sort(key=get_datetime)
        elif sort_option == "Sort by Home Team":
            matches.sort(key=lambda match: (match["home_team"].lower(), get_datetime(match)))
        return matches

    #=== invoice ===
    @staticmethod
    def sort_matches(matches, sort_option): #Sắp xếp danh sách trận đấu dựa trên tùy chọn
        def is_valid_date(date_str):
            import re
            pattern = r"^\d{4}-\d{2}-\d{2}$"
            if not re.match(pattern, date_str):
                return False
            try:
                year, month, day = map(int, date_str.split("-"))
                if not (1 <= month <= 12):
                    return False
                if not (1 <= day <= 31):
                    return False
                return True
            except ValueError:
                return False

        def is_valid_time(time_str):
            import re
            pattern = r"^(1[0-2]|0?[1-9]):([0-5][0-9]) (AM|PM)$"
            if not re.match(pattern, time_str):
                return False
            return True

        def get_datetime(match):
            try:
                date_str = match['date']
                time_str = match['time']
                if not is_valid_date(date_str) or not is_valid_time(time_str):
                    return datetime.max
                return datetime.strptime(f"{date_str} {time_str}", "%Y-%m-%d %I:%M %p")
            except (ValueError, KeyError) as e:
                print(f"Error parsing datetime: {e} for match {match['home_team']} vs {match['away_team']}")
                return datetime.max

        if sort_option == "Sort by Date and Time":
            matches.sort(key=get_datetime)
        elif sort_option == "Sort by Revenue (High to Low)":
            matches.sort(key=lambda match: int(match["total"].replace("$", "")), reverse=True)
        elif sort_option == "Sort by Home Team":
            matches.sort(key=lambda match: (match["home_team"].lower(), get_datetime(match)))
        return matches

    # =========================  XỬ LÝ CUSTOMER  ================================================

    @staticmethod
    def get_customers(obj):  # Lấy danh sách khách hàng từ MongoDB
        return list(user_collection.find({}, {"_id": 0, "username": 1, "email": 1}))

    @staticmethod
    def get_tickets_by_customer(obj):  # Lấy danh sách vé của khách hàng kèm theo thông tin trận đấu
        user_data = user_collection.find_one({"username": obj}, {"_id": 0, "match_info": 1})
        if user_data and "match_info" in user_data:
            match_tickets = []
            for match in user_data["match_info"]:
                match_name = f"{match['home_team']} vs {match['away_team']}"
                match_time = f"{match['date']}, {match['time']}"
                tickets = match.get("tickets", [])
                total = f"{match['total']}"
                stadium = match.get("stadium", "N/A")  # Nếu không có trường stadium, mặc định là "N/A"

                match_tickets.append({
                    "match_name": match_name,
                    "time": match_time,
                    "tickets": tickets,
                    "total": total,
                    "stadium": stadium })
            return match_tickets
        return []  # Trả về danh sách rỗng nếu không có dữ liệu

    # ==================================== XỬ LÝ ADD PRODUCTS ============================================
    @staticmethod
    def validate_input(obj):  # Kiểm tra dữ liệu nhập vào và trích xuất thông tin trận đấu
        match_date = obj.date_entry.get().strip()
        match_time = obj.time_entry.get().strip()
        home_team = obj.home_team_combobox.get().strip()
        away_team = obj.visiting_team_combobox.get().strip()
        stadium = obj.stadium_combobox.get().strip()

        ticket_data = []
        for i, category in enumerate(obj.TICKET_CATEGORIES):  # Kiểm tra số lượng ghế nhập vào
            seats = obj.seat_entries[i].get().strip()
            if not seats.isdigit():
                messagebox.showerror("Error", "Number of seats must be a positive integer!")
                return None
            ticket_data.append({
                "area": category["area"],
                "price": category['price'],  # Giá vé dạng str, ví dụ: '$500'
                "available_seats": int(seats)})
        if hasattr(obj, "scrollable_frame"):
            AdminProcess_Main.load_matches(obj)

        return {
            "date": match_date,
            "time": match_time,
            "home_team": home_team,
            "away_team": away_team,
            "stadium": stadium,
            "tickets": ticket_data}

    @staticmethod
    def search_customers(customers, search_text):  # Lọc danh sách khách hàng dựa trên từ khóa tìm kiếm
        search_text = search_text.strip().lower()
        if search_text == "search customers...":
            search_text = ""

        filtered_customers = []
        for customer in customers:  # Lọc danh sách khách hàng
            if (search_text in customer.get("username", "").lower() or
                    search_text in customer.get("email", "").lower()):
                filtered_customers.append(customer)
        return filtered_customers

# ================================= XỬ LÝ INVOICE  =================================================================
    @staticmethod
    def calculate_total_revenue(date, time, home_team, away_team):  # Tính tổng doanh thu từ vé của một trận đấu
        users = user_collection.find({"match_info": {
            "$elemMatch": {"date": date, 'time': time, "home_team": home_team, "away_team": away_team}}})
        total_revenue = 0

        for user in users:
            for match_info in user.get("match_info", []):
                if match_info.get("home_team") == home_team and match_info.get(
                        "away_team") == away_team and match_info.get("date") == date and match_info.get("time") == time:
                    total_str = str(match_info.get("total", "0")).replace("$", "").strip()
                    try:
                        total_revenue += int(total_str)
                    except ValueError:
                        print(f"Lỗi chuyển đổi total: {total_str}")
        return total_revenue

    @staticmethod
    def get_tickets_for_match(home_team, away_team, date, time):  # Lấy danh sách vé đã bán của một trận đấu
        users = user_collection.find({
            "match_info": {"$elemMatch": {"home_team": home_team, "away_team": away_team, 'date': date, 'time': time}}})
        ticket_info = []

        for user in users:
            for match_info in user.get("match_info", []):
                if match_info.get("home_team") == home_team and match_info.get(
                        "away_team") == away_team and match_info.get("date") == date and match_info.get("time") == time:
                    total_str = str(match_info.get("total", "0")).replace("$", "").strip()
                    try:
                        total_price = int(total_str)
                    except ValueError:
                        total_price = 0

                    ticket_info.append({
                        "username": user.get("username", "N/A"),
                        "total": total_price,
                        "tickets": match_info.get("tickets", []),
                        "stadium": match_info.get("stadium", "N/A")  # Thêm trường stadium
                    })
        return ticket_info

