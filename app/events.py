from app.models import *


def create_event(event, sender_id, receiver_id):
	user_event_1 = UserEvent(user_id=sender_id, event_id=event.id)
	user_event_2 = UserEvent(user_id=receiver_id, event_id=event.id)
	db.session.add(user_event_1)
	db.session.add(user_event_2)
	event_invitation = EventInvitation(sender_id=sender_id, receiver_id=receiver_id)
	db.session.add(event_invitation)
	db.session.commit()