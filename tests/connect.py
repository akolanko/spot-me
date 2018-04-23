from app import db
import sys
import os.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir, 'app')))


def connect_to_db(app, db_uri=None):
    """Connect the database to our Flask app."""
    app.config['SQLALCHEMY_DATABASE_URI'] = db_uri or os.environ['SQLALCHEMY_DATABASE_URI']
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.app = app
    db.init_app(app)
