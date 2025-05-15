# Dự án backend API 

Dự án sử dụng Flask và SQLAlchemy để xây dựng hệ thống.  
Mục tiêu: thực hành kiến trúc MVC, tổ chức mã sạch, quản lý dữ liệu quan hệ và triển khai bằng Docker.

---

# Tính năng chính


- Quản lý người dùng (Admin/User)
- Đăng nhập / Đăng ký người dùng
- CRUD task
- Tìm kiếm & phân trang kết quả review
- Unit test với Pytest
- CI/CD với GitHub Actions
- Deploy online bằng Railway
- Template HTML (demo dự án)
- Tổ chức project theo kiến trúc MVC
- Container hóa bằng Docker

---

# Công nghệ sử dụng

- **Backend**: Flask, SQLAlchemy, Flask-Login, Flask-WTF  
- **Database**: MySQL  
- **Test**: Pytest  
- **DevOps**: Docker, dotenv  
- **IDE**: VSCode  

---

# 📦 Cài đặt & chạy dự án (Local)

### 1. Clone project
```bash
git clone https://github.com/LuongTanTai200803/Review_flask.git
cd Review_flask

1. Tạo virtual environment (venv)
2. Cài đặt requirements
3. Chạy Flask server

```bash
python3 -m venv venv
source venv/bin/activate  # hoặc venv\Scripts\activate (Windows)
pip install -r requirements.txt
python run.py

