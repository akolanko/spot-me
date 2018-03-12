from app.models import Conversation, User, Message
from app.models import db
from sqlalchemy import desc


def get_conversations(user_id):
	c1 = db.session.query(User, Conversation).filter(Conversation.user_id_1 == user_id).join(Conversation, Conversation.user_id_2 == User.id)
	c2 = db.session.query(User, Conversation).filter(Conversation.user_id_2 == user_id).join(Conversation, Conversation.user_id_1 == User.id)
	conversations = c1.union(c2).all()
	return conversations


def update_read_messages(conversation_id, user_id):
	unread = Message.query.filter_by(conversation_id=conversation_id, read=False, sender=user_id)
	for message in unread:
		message.read = True
		db.session.commit()


def most_recent_message(user_id):
	m1 = db.session.query(Message).join(Conversation).filter(Conversation.user_id_1 == user_id).order_by(desc(Message.timestamp)).first()
	m2 = db.session.query(Message).join(Conversation).filter(Conversation.user_id_2 == user_id).order_by(desc(Message.timestamp)).first()
	if m1 is not None and m2 is not None:
		if m1.timestamp > m2.timestamp:
			return m1
		else:
			return m2
	elif m1 is None:
		return m2
	else:
		return m1
	return m1


def unread_messages(user_id):
	m1 = db.session.query(Message).filter(Conversation.user_id_1 == user_id, Message.read == 0).join(Conversation, Conversation.user_id_2 == Message.sender)
	m2 = db.session.query(Message).filter(Conversation.user_id_2 == user_id, Message.read == 0).join(Conversation, Conversation.user_id_1 == Message.sender)
	# msg_count = len(m1.union(m2).all())
	msg_count = m1.union(m2).all()
	return msg_count
