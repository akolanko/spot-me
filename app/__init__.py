import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
# from app.models import db
from flask_login import LoginManager
from flask_migrate import Migrate


db = SQLAlchemy()


app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret'

migrate = Migrate(app, db)


def connect_to_db(app, db_uri=None):
    """Connect the database to our Flask app."""
    # Environment variables are defined in app.yaml.
    app.config['SQLALCHEMY_DATABASE_URI'] = db_uri or os.environ['SQLALCHEMY_DATABASE_URI']
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.app = app
    db.init_app(app)

login = LoginManager(app)
login.login_view = 'login'


from app import routes, models
