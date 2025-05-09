import os
from flask_caching import Cache
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
    
    CELERY_BROKER_URL = 'redis://localhost:6379/0'
    CELERY_RESULT_BACKEND = 'redis://localhost:6379/1'

    CACHE_TYPE = 'RedisCache'
    CACHE_REDIS_URL = 'redis://localhost:6379/2'
    CACHE_DEFAULT_TIMEOUT = 30

class Testing(Config):
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:3366@mysql:3306/review_test"
class ProductingConfig(Config):
    SQLALCHEMY_DATABASE_URI = "mysql://root:GkyaiaZygsNgWYWusQUqLzzivDdxymzq@gondola.proxy.rlwy.net:49132/railway"  # Hoặc PostgreSQL test DB
