from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from flask_caching import Cache
from sqlalchemy.exc import SQLAlchemyError

db = SQLAlchemy()
jwt = JWTManager()
migrate = Migrate()
cache = Cache()

def register_db_session_handlers(app: Flask):
    @app.teardown_request
    def shutdown_session(exception=None):
        if exception:
            db.session.rollback()
        else:
            try:
                db.session.commit()
            except SQLAlchemyError:
                db.session.rollback()
                raise  # Ném lỗi ra ngoài để Flask xử lý

        db.session.remove()  # Luôn luôn remove session sau mỗi request