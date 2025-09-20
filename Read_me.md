# PHẦN MỀM QUẢN LÝ VÀ BÁN VÉ BÓNG ĐÁ - GROUP 8 ⚽

## Giới thiệu 📖

**Phần mềm Quản lý và Bán vé Bóng đá** là một Desktop Application được phát triển bằng Python, giúp người dùng dễ dàng đăng ký, đăng nhập, tìm kiếm và đặt vé xem các trận đấu bóng đá. Ứng dụng được thiết kế với giao diện thân thiện , hỗ trợ cả người dùng thông thường (User) và quản trị viên (Admin). Người dùng có thể xem danh sách trận đấu, chọn khu vực ghế ngồi, đặt vé và quản lý vé đã đặt. Quản trị viên có thể quản lý thông tin trận đấu, vé và người dùng thông qua bảng điều khiển quản trị.

### Các tính năng chính:
- **Đăng ký và Đăng nhập** : Người dùng có thể tạo tài khoản và đăng nhập để sử dụng ứng dụng. (User, Admin)
- **Xem danh sách trận đấu** : Hiển thị các trận đấu bóng đá sắp diễn ra theo đội bóng. (User)
- **Chọn khu vực và đặt vé** : Người dùng có thể chọn khu vực ghế ngồi và đặt vé dễ dàng. (User)
- **Quản lý vé đã đặt** : Xem và quản lý các vé đã đặt trong mục "My Tickets". (User)
- **Bảng điều khiển quản trị** : Quản trị viên có thể quản lý trận đấu, vé và thông tin người dùng. (Admin)

Ứng dụng được xây dựng với kiến trúc mô-đun, tách biệt rõ ràng giữa xử lý logic (`Process`) và giao diện (`View`), giúp dễ dàng bảo trì và mở rộng. 🚀

## Hướng dẫn sử dụng 📚

### 1. Cài đặt ứng dụng 🛠️

Để chạy ứng dụng trên máy tính của bạn, hãy làm theo các bước sau:

#### Bước 1: Tải mã nguồn 
Tải mã nguồn của ứng dụng từ kho lưu trữ (nếu có) hoặc sao chép thư mục dự án vào máy tính của bạn.

#### Bước 2: Thiết lập môi trường ảo 
- Mở terminal/command prompt và điều hướng đến thư mục dự án:
- Tạo môi trường ảo:
  ```bash
  python -m venv .venv
  ```
- Kích hoạt môi trường ảo:
  - Trên Windows:
    ```bash
    .venv\Scripts\activate
    ```
  - Trên macOS/Linux:
    ```bash
    source .venv/bin/activate
    ```

#### Bước 3: Cài đặt các thư viện cần thiết 
Cài đặt các thư viện được liệt kê trong file `requirements.txt`:
Chạy file script cài đặt:
  ```bash
    python Install_Libs.py
  ```

#### Bước 4: Tải các font chữ cần thiết 
Ứng dụng sử dụng các font chữ **Montserrat** và **Inter** để có trải nghiệm tốt hơn.  
Tải các font này từ Google Fonts hoặc các nguồn đáng tin cậy, sau đó cài đặt vào hệ thống của bạn:
- [Montserrat](https://fonts.google.com/specimen/Montserrat) 
- [Inter](https://fonts.google.com/specimen/Inter) 

#### Bước 5: Khởi chạy ứng dụng 
- Chạy file chính của ứng dụng:
  ```bash
   python App.py
  ```

---

### 2. Sử dụng ứng dụng (User) 👤

#### 2.1. Đăng nhập tài khoản 
- Truy cập vào màn hình đăng nhập (Login).
- Chọn vai trò **User** để đăng nhập.
- Nếu bạn là User và chưa có tài khoản, nhấn vào **Signup Now** để đăng ký tài khoản mới. 
- Nếu không muốn đăng kí :
  - Username: `emvu`  
  - Password: `123`  

#### 2.2. Màn hình chính bán vé 
- Sau khi đăng nhập, bạn sẽ thấy trang chính hiển thị danh sách các đội bóng.
- Nhấn vào một đội bóng để xem chi tiết các trận đấu sắp tới của đội bóng đó.

#### 2.3. Xem danh sách trận đấu theo đội bóng 
- Từ danh sách đội bóng, nhấn vào một đội bóng để xem chi tiết các trận đấu sắp tới.
- Xem thông tin chi tiết của từng trận đấu như thời gian, địa điểm, và vé còn lại.

#### 2.4. Chọn khu vực và đặt vé
- Từ trang chi tiết trận đấu, nhấn vào nút **View Ticket** của trận đấu bạn muốn mua.
- Chọn khu vực ghế ngồi mà bạn muốn và điền số lượng vé cần đặt.
- Nhấn **Payment** để xác nhận thanh toán, sau đó kiểm tra lại thông tin vé.
- Nếu thông tin đã chính xác, chọn **CONFIRM PAYMENT**  để hoàn tất.
- Nếu không muốn tiếp tục, nhấn **CANCEL** để hủy đặt vé.

#### 2.5. Quản lý vé đã đặt
- Truy cập vào mục **My Tickets** từ menu.
- Tại đây, bạn có thể xem danh sách các vé đã đặt, bao gồm thông tin trận đấu, khu vực ghế ngồi và tổng số tiền.

#### 2.6. Cập nhật thông tin cá nhân 
- Truy cập mục **User Information** từ menu.
- Tại đây, bạn có thể xem và chỉnh sửa thông tin cá nhân của mình. Nếu có vấn đề cần hỗ trợ, bạn cũng có thể liên hệ với đội ngũ phát triển từ đây.

#### 2.7. Đăng xuất 
- Nhấn vào biểu tượng **Logout** để thoát khỏi tài khoản và quay lại màn hình đăng nhập.

---

### 3. Sử dụng bảng điều khiển quản trị (Admin) 🧑‍💼

#### 3.1. Đăng nhập với tài khoản quản trị 
- Sử dụng tài khoản quản trị với thông tin:  
  - Username: `1`  
  - Password: `1`  
- Sau khi đăng nhập, bạn sẽ được chuyển đến bảng điều khiển quản trị.

#### 3.2. Quản lý trận đấu và vé ⚙
- Trong bảng điều khiển, bạn có thể:  
  - **Dashboard** : Xem doanh thu được thể hiện qua biểu đồ, phân tích theo từng đội bóng và tổng doanh thu của tất cả các đội.  
  - **Invoices** : Xem doanh thu từ các trận đấu đã bán vé.  
  - **Products** : Xem danh sách các trận đấu hiện tại, chỉnh sửa hoặc cập nhật thông tin trận đấu bằng cách chọn trận đấu trong danh sách. Bạn cũng có thể thêm trận đấu mới bằng cách nhấn **Add New Product**.

#### 3.3. Quản lý người dùng
- Cũng trong bảng điều khiển, xem danh sách người dùng trong trang **Customers** đã đăng ký trên hệ thống.
- Xem danh sách các trận đấu mà từng người dùng đã mua vé.

### 4. Lưu ý ⚠️
- Đảm bảo bạn đã cài đặt đầy đủ các thư viện trong file `requirements.txt` để tránh lỗi khi chạy ứng dụng.
- Nếu gặp vấn đề khi chạy ứng dụng, hãy kiểm tra file `.env` (nếu có) để đảm bảo các biến môi trường (như kết nối cơ sở dữ liệu) được thiết lập chính xác.
- Ứng dụng có thể yêu cầu kết nối internet để tải một số tài nguyên (như font chữ hoặc dữ liệu từ server).

### 5. Hỗ trợ 📧
Nếu bạn gặp bất kỳ vấn đề nào khi sử dụng ứng dụng, hãy liên hệ với nhóm phát triển qua email: [quyenll23406@st.uel.edu.vn].

## Lời cảm ơn 💖
Cảm ơn thầy Phúc đã hướng dẫn tụi em trong suốt quá trình làm dự án này!  Nhờ thầy mà tụi em học được bao nhiêu là kiến thức hay ho, từ cách code cho tới cách làm việc nhóm. Thầy không chỉ truyền đạt kiến thức mà còn truyền cả cảm hứng, làm tụi em mê lập trình hơn bao giờ hết! Một lần nữa, tụi em cảm ơn thầy thật nhiều và chúc thầy luôn mạnh khỏe, vui vẻ ạ!