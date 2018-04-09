from app.models import *
from app import db
from sqlalchemy import asc
import datetime
from app.notifications import create_invite_notification
from flask import jsonify
from app.friends import are_connected


def create_friend_event(event, sender, receiver_id):
	user_event_1 = UserEvent(user_id=sender.id, event_id=event.id, accepted=True)
	user_event_2 = UserEvent(user_id=receiver_id, event_id=event.id)
	db.session.add(user_event_1)
	db.session.add(user_event_2)
	event_invitation = EventInvitation(sender_id=sender.id, receiver_id=receiver_id, event_id=event.id)
	db.session.add(event_invitation)
	create_invite_notification(event.id, sender, receiver_id)
	db.session.commit()


def user_event_exists(user_id, event_id):
	user_event = UserEvent.query.filter_by(user_id=user_id, event_id=event_id)
	if user_event is None:
		return None
	else:
		return user_event.first()


def get_recent_events(user_id):
	today = datetime.date.today()
	events = db.session.query(Event).join(UserEvent, UserEvent.event_id == Event.id).filter(UserEvent.user_id == user_id, UserEvent.accepted == 1, Event.date >= today).order_by(asc(Event.date), asc(Event.start_time)).limit(3).all()
	return events


def get_event_invitation(event_id, user_id):
	sent_invitation = db.session.query(EventInvitation).filter(EventInvitation.event_id == event_id, EventInvitation.sender_id == user_id).first()
	received_invitation = db.session.query(EventInvitation).filter(EventInvitation.event_id == event_id, EventInvitation.receiver_id == user_id).first()
	return sent_invitation, received_invitation


def create_user_event(user_id, event_id, sender_id):
	sender = User.query.filter_by(id=sender_id).first()
	exists = user_event_exists(user_id, event_id)
	if exists is None:
		user_event = UserEvent(user_id=user_id, event_id=event_id)
		db.session.add(user_event)
		event_invitation = EventInvitation(sender_id=sender_id, receiver_id=user_id, event_id=event_id)
		db.session.add(event_invitation)
		create_invite_notification(event_id, sender, user_id)
		db.session.commit()
		return user_event
	else:
		return None


def check_results(users, event_id, sender_id):
	connected = False
	if len(users) == 1:
		connected = are_connected(users[0].id, sender_id)
	if len(users) < 1 or (len(users) == 1 and (users[0].id == sender_id or not connected)):
		return jsonify("Your search did not return any results.")
	elif len(users) > 1:
		return jsonify(["multiple results", [u.serialize() for u in users], event_id])
	else:
		user_event = create_user_event(users[0].id, event_id, sender_id)
		if user_event is None:
			return jsonify(users[0].fname + " is already invited.")
		return jsonify(["success", users[0].serialize()])


def invite_search(users, event_id, sender_id):
	if len(users) > 1:
		not_ivited_users = []
		for user in users:
			user_event = user_event_exists(user.id, event_id)
			connected = are_connected(user.id, sender_id)
			if user_event is None and user.id != sender_id and connected:
				not_ivited_users.append(user)
		return check_results(not_ivited_users, event_id, sender_id)
	return check_results(users, event_id, sender_id)
