import os
import logging
from .config import Config
from flask import Flask, Blueprint
from .extensions import db, jwt, migrate, cache
from app.routes.auth import auth_bp
from app.routes.task import task_bp
from app.routes.post import post_bp

def create_app():
    app = Flask(__name__)

    # Load file cấu hình
    app.config.from_object(Config)
    # Khởi tạo các extension
    db.init_app(app)
    jwt.init_app(app)
    migrate.init_app(app, db)
    cache.init_app(app)

    # Đăng ký blueprint
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(task_bp, url_prefix='/task')
    app.register_blueprint(post_bp, url_prefix='/post')

    with app.app_context():
        db.create_all()
    return app

def setup_logging():
    # Cấu hình log
    log_format = "%(asctime)s - %(levelname)s - %(name)s - %(message)s"

    app_log_handler = logging.FileHandler("logs/app.log")
    app_log_handler.setLevel(logging.DEBUG)

    error_log_handler = logging.FileHandler("logs/error.log")
    error_log_handler.setLevel(logging.ERROR)

    log_handlers = [
        logging.StreamHandler(), # Hiển thị log terminal
        app_log_handler,
        error_log_handler
    ]

    logging.basicConfig(
        level=logging.DEBUG,
        format=log_format,
        handlers=log_handlers
    )