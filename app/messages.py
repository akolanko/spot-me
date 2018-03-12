from app.models import Conversation, User
from app.models import db


def get_conversations(user_id):
	c1 = db.session.query(User).filter(Conversation.user_id_1 == user_id).join(Conversation, Conversation.user_id_1 == User.id)
	c2 = db.session.query(User).filter(Conversation.user_id_2 == user_id).join(Conversation, Conversation.user_id_2 == User.id)
	conversations = c1.union(c2).all()
	return conversations