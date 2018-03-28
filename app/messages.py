from app.models import Conversation, User, Message
from app.models import db
from sqlalchemy import desc


def get_conversations(user_id):
	c1 = db.session.query(User, Conversation).filter(Conversation.user_id_1 == user_id).join(Conversation, Conversation.user_id_2 == User.id)
	c2 = db.session.query(User, Conversation).filter(Conversation.user_id_2 == user_id).join(Conversation, Conversation.user_id_1 == User.id)
	conversations = c1.union(c2).all()

	# c1 = db.session.query(Conversation, Message, User).filter(Conversation.user_id_1 == user_id).join(Message, User).filter(User.id == Conversation.user_id_2)
	# c2 = db.session.query(Conversation, Message, User).filter(Conversation.user_id_2 == user_id).join(Message, User).filter( User.id == Conversation.user_id_1)
	# conversations = c1.union(c2).order_by(desc(Message.timestamp)).group_by(Message.conversation_id, Conversation.id).all()

	return conversations


def update_read_messages(conversation_id, user_id):
	unread = Message.query.filter_by(conversation_id=conversation_id, read=False, sender=user_id)
	for message in unread:
		message.read = True
		db.session.commit()


def most_recent_message(user_id):
	m1 = db.session.query(Message).join(Conversation).filter(Conversation.user_id_1 == user_id)
	m2 = db.session.query(Message).join(Conversation).filter(Conversation.user_id_2 == user_id)
	message = m1.union(m2).order_by(desc(Message.timestamp)).first()
	return message


def unread_messages(user_id):
	cm1 = db.session.query(Conversation, Message, User).filter(Message.read == 0, Conversation.user_id_1 == user_id).join(Message).filter(Conversation.user_id_2 == Message.sender, User.id == Message.sender)
	cm2 = db.session.query(Conversation, Message, User).filter(Message.read == 0, Conversation.user_id_2 == user_id).join(Message).filter(Conversation.user_id_1 == Message.sender, User.id == Message.sender)
	union = cm1.union(cm2).order_by(desc(Message.timestamp))
	msg_count = len(union.all())
	conversations = union.group_by(Message.conversation_id, Conversation.id).all()
	return msg_count, conversations


def conversation_exists(user_id_1, user_id_2):
	c1 = Conversation.query.filter_by(user_id_1=user_id_1, user_id_2=user_id_2).first()
	if c1:
		return c1
	c2 = Conversation.query.filter_by(user_id_1=user_id_2, user_id_2=user_id_1).first()
	if c2:
		return c2
	return None


def build_conversation(user_id_1, user_id_2):
	conversation = conversation_exists(user_id_1, user_id_2)
	if conversation is None:
		conversation = Conversation(user_id_1=user_id_1, user_id_2=user_id_2)
		db.session.add(conversation)
		db.session.commit()
		conversation = conversation_exists(user_id_1, user_id_2)
	return conversation.id


def get_conversation(conversation_id):
	conversation = db.session.query(Conversation).filter(Conversation.id == conversation_id).first()
	return conversation


def get_conversation_user(cur_user_id, coversation):
	if Conversation.user_id_1 == cur_user_id:
		friend_id = Conversation.user_id_2
	else:
		friend_id = Conversation.user_id_1
	friend = db.session.query(User).filter(User.id == friend_id).first()
	return friend
