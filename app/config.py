import os
from dotenv import load_dotenv
load_dotenv()

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY")
    SQLALCHEMY_DATABASE_URI= os.getenv("MYSQL_PUBLIC_URL")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ENGINE_OPTIONS = {
        'connect_args': {
            'connect_timeout': 10,  # Thời gian chờ kết nối ban đầu, 10 giây
            'read_timeout': 60,     # Tăng thời gian chờ đọc lên 60 giây
        },
        'pool_recycle': 7200,  # Tái sử dụng kết nối sau 2 giờ
    }
    JWT_SECRET_KEY = os.getenv("SECRET_KEY")
    