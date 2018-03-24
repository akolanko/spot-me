from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app import login, connect_to_db, db
import enum
from hashlib import md5
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
import os


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(32), index=True, unique=True)
    email = db.Column(db.String(64), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    fname = db.Column(db.String(32))
    lname = db.Column(db.String(32))
    profile = db.relationship('Profile', uselist=False, backref='owner')

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def avatar(self, size):
        digest = md5(self.email.lower().encode('utf-8')).hexdigest()
        return 'https://www.gravatar.com/avatar/{}?d=identicon&s={}'.format(digest, size)


@login.user_loader
def load_user(id):
    return User.query.get(int(id))


class Profile(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    about = db.Column(db.Text)
    # interests = db.Column(db.Text)
    # skills = db.Column(db.Text)
    # location = db.Column(db.Text)
    # work = db.Column(db.Text)
    # interests = db.Column(db.Text)
    # meet = db.Column(db.Text)


class FriendStatus(enum.Enum):
    requested = 0
    accepted = 1


class Friends(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id_1 = db.Column(db.Integer, db.ForeignKey('user.id'), index=True, nullable=False)
    user_id_2 = db.Column(db.Integer, db.ForeignKey('user.id'), index=True, nullable=False)
    status = db.Column(db.Enum(FriendStatus))
    user_1 = db.relationship("User", foreign_keys=[user_id_1], backref=db.backref("sent_connections"))
    user_2 = db.relationship("User", foreign_keys=[user_id_2], backref=db.backref("received_connections"))

    def __repr__(self):
        return "<Friends id=%s user_id_1=%s user_id_2=%s status=%s>" % (self.id, self.user_id_1, self.user_id_2, self.status)


class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    sender = db.Column(db.Integer, db.ForeignKey('user.id'), index=True, nullable=False)
    body = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    read = db.Column(db.Boolean, default=False, nullable=False)
    conversation_id = db.Column(db.Integer, db.ForeignKey('conversation.id'))


class Conversation(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id_1 = db.Column(db.Integer, db.ForeignKey('user.id'), index=True, nullable=False)
    user_id_2 = db.Column(db.Integer, db.ForeignKey('user.id'), index=True, nullable=False)
    messages = db.relationship('Message', backref='message', lazy='dynamic')
