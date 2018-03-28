from app.models import User, db


def get_user(user_id):
	user = db.session.query(User).filter(User.id == user_id)
	return user