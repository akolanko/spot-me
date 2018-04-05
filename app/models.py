from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app import db, login
import enum
from hashlib import md5
import time
from datetime import datetime


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(32), index=True, unique=True)
    email = db.Column(db.String(64), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    fname = db.Column(db.String(32))
    lname = db.Column(db.String(32))
    birthday = db.Column(db.Date, default=datetime.utcnow)
    profile = db.relationship('Profile', uselist=False, backref='owner', cascade="all, delete-orphan")

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def avatar(self, size):
        digest = md5(self.email.lower().encode('utf-8')).hexdigest()
        return 'https://www.gravatar.com/avatar/{}?d=identicon&s={}'.format(digest, size)

    def serialize(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'fname': self.fname,
            'lname': self.lname,
            'avatar': self.avatar(75)
        }


@login.user_loader
def load_user(id):
    return User.query.get(int(id))


class Profile(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id   = db.Column(db.Integer, db.ForeignKey('user.id'))
    about     = db.Column(db.Text)
    work      = db.Column(db.Text)
    skills    = db.Column(db.Text)
    location  = db.Column(db.Text)
    interests = db.Column(db.Text)
    meet      = db.Column(db.Text)


class Interest(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(32))

    def serialize(self):
        return {
            'id': self.id,
            'name': self.name
        }


class User_Interest(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), index=True, nullable=False)
    interest_id = db.Column(db.Integer, db.ForeignKey('interest.id'), index=True, nullable=False)
    user = db.relationship("User", foreign_keys=[user_id], backref=db.backref("user", cascade="all,delete"))
    interest = db.relationship("Interest", foreign_keys=[interest_id], backref=db.backref("interest", cascade="all,delete"))


class FriendStatus(enum.Enum):
    requested = 0
    accepted = 1


class Friends(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id_1 = db.Column(db.Integer, db.ForeignKey('user.id'), index=True, nullable=False)
    user_id_2 = db.Column(db.Integer, db.ForeignKey('user.id'), index=True, nullable=False)
    status = db.Column(db.Enum(FriendStatus))
    user_1 = db.relationship("User", foreign_keys=[user_id_1], backref=db.backref("sent_connections", cascade="all,delete"))
    user_2 = db.relationship("User", foreign_keys=[user_id_2], backref=db.backref("received_connections", cascade="all,delete"))

    def __repr__(self):
        return "<Friends id=%s user_id_1=%s user_id_2=%s status=%s>" % (self.id, self.user_id_1, self.user_id_2, self.status)


class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    sender = db.Column(db.Integer, db.ForeignKey('user.id'), index=True, nullable=False)
    body = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    read = db.Column(db.Boolean, default=False, nullable=False)
    conversation_id = db.Column(db.Integer, db.ForeignKey('conversation.id'))

    def serialize(self):
        return {
            'id': self.id,
            'sender': self.sender,
            'body': self.body,
            'timestamp': int(time.mktime((self.timestamp).timetuple())) * 1000,
            'read': self.read,
            'conversation_id': self.conversation_id
        }


class Conversation(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id_1 = db.Column(db.Integer, db.ForeignKey('user.id'),  index=True, nullable=False)
    user_id_2 = db.Column(db.Integer, db.ForeignKey('user.id'),  index=True, nullable=False)
    user_1 = db.relationship("User", foreign_keys=[user_id_1], backref=db.backref("started_conversations", cascade="all,delete"))
    user_2 = db.relationship("User", foreign_keys=[user_id_2], backref=db.backref("joined_conversations", cascade="all,delete"))
    messages = db.relationship('Message', backref='conversation', lazy='dynamic', cascade="all,delete")

    def serialize(self):
        return {
            'id': self.id,
            'user_id_1': self.user_id_1,
            'user_id_2': self.user_id_2
        }


class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    date = db.Column(db.Date, index=True, nullable=False)
    start_time = db.Column(db.Time, nullable=False)
    end_time = db.Column(db.Time, nullable=False)
    title = db.Column(db.String(32), nullable=False)
    location = db.Column(db.String(32))
    notes = db.Column(db.Text)


class UserEvent(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), index=True, nullable=False)
    event_id = db.Column(db.Integer, db.ForeignKey('event.id'), index=True, nullable=False)
    accepted = db.Column(db.Boolean, default=False, nullable=False)
    user = db.relationship("User", foreign_keys=[user_id], backref=db.backref("user_events", cascade="all,delete"))
    event = db.relationship("Event", foreign_keys=[event_id], backref=db.backref("user_events", cascade="all,delete"))

    def serialize(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'event_id': self.event_id,
            'accepted': self.accepted
        }


class EventInvitation(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    sender_id = db.Column(db.Integer, db.ForeignKey('user.id'), index=True, nullable=False)
    receiver_id = db.Column(db.Integer, db.ForeignKey('user.id'), index=True, nullable=False)
    event_id = db.Column(db.Integer, db.ForeignKey('event.id'), index=True, nullable=False)
    sender = db.relationship("User", foreign_keys=[sender_id], backref=db.backref("sent_invitations", cascade="all,delete"))
    receiver = db.relationship("User", foreign_keys=[receiver_id], backref=db.backref("received_invitations", cascade="all,delete"))
    event = db.relationship("Event", foreign_keys=[event_id], backref=db.backref("invitations", cascade="all,delete"))


class NotificationType(enum.Enum):
    event_invite = 0
    event_update = 1
    invite_accepted = 2
    invite_declined = 3


class Notification(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    body = db.Column(db.String(255), nullable=False)
    receiver_id = db.Column(db.Integer, db.ForeignKey('user.id'), index=True, nullable=False)
    event_id = db.Column(db.Integer, db.ForeignKey('event.id'))
    type = db.Column(db.Enum(NotificationType), nullable=False)
    created_at = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    receiver = db.relationship("User", foreign_keys=[receiver_id], backref=db.backref("notifications", cascade="all,delete"))
    event = db.relationship("Event", foreign_keys=[event_id], backref=db.backref("notifications", cascade="all,delete"))
