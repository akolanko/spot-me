from werkzeug.security import generate_password_hash, check_password_hash
from app import db
from flask_login import UserMixin
from app import login


class Visit(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime())
    user_ip = db.Column(db.String(46))

    def __init__(self, timestamp, user_ip):
        self.timestamp = timestamp
        self.user_ip = user_ip


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(32), index=True, unique=True)
    email = db.Column(db.String(64), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    profile = db.relationship('Profile', uselist=False, backref='owner')

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


@login.user_loader
def load_user(id):
    return User.query.get(int(id))


class Profile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    about = db.Column(db.Text)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
