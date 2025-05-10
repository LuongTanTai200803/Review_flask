from app import create_app, wait_for_db
from app import setup_logging
from app.config import Production
from app.extensions import db

setup_logging()
app = create_app(config_class=Production)


if __name__ == '__main__':
    wait_for_db(app, db) 
    app.run(debug=False, use_reloader=False)