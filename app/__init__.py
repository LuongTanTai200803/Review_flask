import os
import logging
import time

from app.error_handler import register_error_handlers

from .celery_worker import celery 
from sqlalchemy import text
from .config import Config, ProductingConfig, Testing
from flask import Flask, Blueprint
from .extensions import db, jwt, migrate, cache, register_db_session_handlers
from app.routes.auth import auth_bp
from app.routes.task import task_bp
from app.routes.post import post_bp
from app.log_request import setup_request_logger
from sqlalchemy.exc import OperationalError

""" import pymysql
pymysql.install_as_MySQLdb()
 """
def create_app(config_class= Testing):
    app = Flask(__name__)

    # Load file cấu hình
    app.config.from_object(config_class)
    # Khởi tạo các extension
    db.init_app(app)
    jwt.init_app(app)
    migrate.init_app(app, db)
    cache.init_app(app)
    
    # Cấu hình celery
    celery.conf.update(app.config)
    
    # Đăng ký blueprint
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(task_bp, url_prefix='/task')
    app.register_blueprint(post_bp, url_prefix='/post')

    from flask import url_for

    with app.app_context():
        for rule in app.url_map.iter_rules():
            print(f"{rule.methods} {rule.rule}")
    register_error_handlers(app)
    setup_request_logger(app)
    register_db_session_handlers(app)
    print(app.config['SQLALCHEMY_DATABASE_URI'])
    # Không khởi tạo ở create_app()
    with app.app_context():
        if not os.getenv("TESTING"):
            db.create_all()
    return app

def setup_logging():
    if not os.path.exists("logs"):
        os.makedirs("logs")

    # Cấu hình log
    log_format = "%(asctime)s - %(levelname)s - %(name)s - %(message)s"

    logging.basicConfig(
        level=logging.DEBUG,
        format=log_format,
        handlers=[logging.StreamHandler()]
    ) 

    werkzeug_log = logging.getLogger('werkzeug')
    werkzeug_log.setLevel(logging.ERROR)
    #werkzeug_log.propagate = False 

def wait_for_db(app, db, retries=5, delay=2):
    last_exception = None

    with app.app_context():
        for i in range(retries):
            try:
                db.session.execute(text('SELECT 1'))  # test raw sql query
                print("Database is ready!")
                #db.create_all()
                break
            except OperationalError as e:
                last_exception = e
                print(f"Database not ready yet, retry {i + 1}/{retries}...")
                time.sleep(delay)
        else:
            print("Database connection failed after retries. Exiting.")
            if last_exception:
                raise last_exception
            else:
                raise Exception("Database connection failed, but no exception captured.")