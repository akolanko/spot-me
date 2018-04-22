from app.models import *
from app.models import db
from app.friends import get_non_friends

def discover_friends(user_id_1):
	non_friends = get_non_friends(user_id_1)
	interests_1 = db.session.query(Interest).join(User_Interest).filter(User_Interest.user_id == user_id_1, Interest.id == User_Interest.interest_id)

	users_interests = []

	for user_2 in non_friends:
		added = False
		shared_interests = []
		interests_2 = db.session.query(Interest).join(User_Interest).filter(User_Interest.user_id == user_2.id, Interest.id == User_Interest.interest_id)
		for interest_1 in interests_1:
			for interest_2 in interests_2:
				if interest_1.name == interest_2.name:
					if added is False:
						added = True
					shared_interests.append(interest_1)
		if added is True:
			users_interests.append((user_2, shared_interests))

	return users_interests


def search_interests(interest, user_id):
	interest_1 = db.session.query(Interest).filter(Interest.name == interest).first()
	users = []
	if interest_1 is not None:
		interest_id = interest_1.id
		non_friends = get_non_friends(user_id)
		users = non_friends.join(User_Interest).filter(User_Interest.user_id == User.id, User_Interest.interest_id == interest_id).all()
	return users


def get_interests(user_id):
	interests = db.session.query(Interest).join(User_Interest).filter(User_Interest.user_id == user_id, Interest.id == User_Interest.interest_id).all()
	return interests
