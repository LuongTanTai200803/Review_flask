import os

from .config import Config
from flask import Flask, Blueprint
from .extensions import db, jwt, migrate
from app.routes.auth import auth_bp
from app.routes.task import task_bp

def create_app():
    app = Flask(__name__)

    # Load file cấu hình
    app.config.from_object(Config)
    # Khởi tạo các extension
    db.init_app(app)
    jwt.init_app(app)
    migrate.init_app(app, db)

    # Đăng ký blueprint
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(task_bp, url_prefix='/task')
    with app.app_context():
        db.create_all()
    return app