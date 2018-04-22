from app.models import *
from app.models import db
from app.friends import get_non_friends, are_connected


def discover_friends(user_id_1):
	non_friends = get_non_friends(user_id_1)
	interests_1 = db.session.query(Interest).join(User_Interest).filter(User_Interest.user_id == user_id_1, Interest.id == User_Interest.interest_id).all()

	users_interests = []

	for user_2 in non_friends:
		added = False
		shared_interests = []
		interests_2 = db.session.query(Interest).join(User_Interest).filter(User_Interest.user_id == user_2.id, Interest.id == User_Interest.interest_id).all()
		if len(interests_1) > 0:
			for interest_1 in interests_1:
				for interest_2 in interests_2:
					if interest_1.name == interest_2.name:
						if added is False:
							added = True
						shared_interests.append(interest_1)
			if added is True:
				users_interests.append((user_2, shared_interests))
		else:
			if len(interests_2) > 0:
				users_interests.append((user_2, interests_2))

	return users_interests


def search_interests(interest, user_id):
	interest_1 = db.session.query(Interest).filter(Interest.name == interest).first()
	non_friends = []
	if interest_1 is not None:
		users = db.session.query(User).join(User_Interest, User_Interest.user_id == User.id).filter(interest_1.id == User_Interest.interest_id).all()
		for user in users:
			if user_id != user.id and not are_connected(user_id, user.id):
				non_friends.append(user)
	return non_friends


def get_interests(user_id):
	interests = db.session.query(Interest).join(User_Interest).filter(User_Interest.user_id == user_id, Interest.id == User_Interest.interest_id).all()
	return interests
