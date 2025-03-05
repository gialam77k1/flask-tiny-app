# 📌 Dự án Flask Tiny App

## 👤 Thông tin cá nhân
- *Họ và tên*: Nguyễn Gia Lâm 
- *Mã số sinh viên*: 22685611

## 📝 Mô tả dự án  
- Người dùng : 
    - Thực hiện đăng ký rồi đăng nhập để sử dụng blog.
    - Có thể tạo, chỉnh sửa hoặc xóa bài viết theo ý muốn.
- Quản lý người dùng:
    - Admin có thể **block** người dùng nếu cần.
    - Admin có thể đổi mật khẩu mới cho người dùng.
- Ngoài ra blog ở version cuối cùng chỉ có 10 bài viết trên 1 trang.
## ⚙️ Hướng dẫn cài đặt và chạy  
***Yêu cầu hệ thống***: Python *3.10* hoặc mới hơn. 

 ***Để chạy được dự án, bạn cần mở **Windows PowerShell** lên và chạy lần lượt các lệnh dưới đây.***
1. Clone the repository
- Đầu tiên để bạn cần clone reposity.
```PowerShell
git clone https://github.com/NamNam2004-77k1/flask-tiny-app.git #Lệnh này dùng để clone repo 
```
```PowerShell
cd flask-tiny-app #Lệnh này dùng để di chuyển vào thư mục app
```
***Đối với các version từ 1 đến 5 thì thực hiện các bước dưới đây:***

2. Khởi tạo môi trường ảo (vitural environments)
- Để khởi tạo môi trường ảo và đảm bảo cho việc chạy được ứng dụng, bạn hãy chạy lần lượt các lệnh dưới đây.
```PowerShell
python -m venv venv #Lệnh này dùng để tạo môi trường ảo có tên là venv
```
```PowerShell
venv\Scripts\activate  #Lệnh này dùng để kích hoạt môi trường ảo venv đã tạo
```
3. Tải các framework cần thiết:
```PowerShell
python.exe -m pip install --upgrade pip #Lệnh này đảm bảo pip ở phiên bản mới nhất để tải được requirements.txt mà không gặp lỗi
```
```PowerShell
pip install -r requirements.txt #Lệnh này dùng để cài đặt các framework mà app sử dụng
```
4. Khởi tạo cơ sở dữ liệu
```PowerShell
flask --app flaskr init-db #Lệnh này dùng để khởi tạo database
```
5. Chạy ứng dụng 
```PowerShell
flask --app flaskr run --debug #Lệnh này dùng để chạy ứng dụng
```
***Đối với version có sử dụng shell script***

2. Khởi tạo ứng dụng bằng cách chạy lệnh này
```PowerShell
.\run.ps1 #lệnh này dùng để kích hoạt ứng dụng
```
***Đối với version sử dụng Dockerfile***
- Đầu tiên bạn cần phải khởi động Docker Desktop lên
- Sau đó bạn hãy thực hiện lệnh bên dưới đây:
```PowerShell
docker build -t flask_app .
```
- Sau đó đợi buid thành công rồi thực hiện chạy câu lệnh bên dưới đây:
```PowerShell
docker run -p 5000:5000 flask_app
```
## 🌍 Link triển khai  
- Sau khi đã thực hiện hết các bước bên trên, bạn hãy truy cập *[http://127.0.0.1:5000](http://127.0.0.1:5000)* trên trình duyệt để sử dụng ứng dụng.
