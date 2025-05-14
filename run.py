from app import create_app, wait_for_db
from app import setup_logging
from app.config import Production, Testing
from app.extensions import db

setup_logging()
app = create_app(config_class=Testing)


if __name__ == '__main__':
    wait_for_db(app, db) 
    app.run(debug=True, use_reloader=False)