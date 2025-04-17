from .config import Config
from flask import Flask, Blueprint
from .extensions import db, jwt


def create_app():
    app = Flask(__name__)

    # Load file cấu hình
    app.config.from_object(Config)
    # Khởi tạo các extension
    db.init_app(app)
    jwt.init_app(app)

    # Đăng ký blueprint
    """ app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(task_bp, url_prefix='/task')
    """
    return app