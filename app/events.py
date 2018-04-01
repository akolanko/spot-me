from app.models import *
from app import db
from sqlalchemy import desc, asc
import datetime


def create_event(event, sender, receiver_id):
	user_event_1 = UserEvent(user_id=sender.id, event_id=event.id)
	user_event_2 = UserEvent(user_id=receiver_id, event_id=event.id)
	db.session.add(user_event_1)
	db.session.add(user_event_2)
	event_invitation = EventInvitation(sender_id=sender.id, receiver_id=receiver_id, event_id=event.id)
	db.session.add(event_invitation)
	body = "New event invitation from " + sender.fname
	notification = Notification(body=body, receiver_id=receiver_id, event_id=event.id, type=NotificationType.event_invite)
	db.session.add(notification)
	db.session.commit()


def user_event_exists(user_id, event_id):
	user_event = UserEvent.query.filter_by(user_id=user_id, event_id=event_id).first()
	return user_event


def get_recent_events(user_id):
	today = datetime.date.today()
	events = db.session.query(Event).join(UserEvent, UserEvent.event_id == Event.id).filter(UserEvent.user_id == user_id, UserEvent.accepted == 1, Event.date >= today).order_by(asc(Event.date)).limit(3).all()
	return events


def get_event_invitation(event_id, user_id):
	sent_invitation = db.session.query(EventInvitation).filter(EventInvitation.event_id == event_id, EventInvitation.sender_id == user_id).first()
	recieved_invitation = db.session.query(EventInvitation).filter(EventInvitation.event_id == event_id, EventInvitation.receiver_id == user_id).first()
	return sent_invitation, recieved_invitation
