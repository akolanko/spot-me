from app.models import *
from app import db

def get_user_interests(user):
	interests = db.session.query(Interest).join(User_Interest).filter(User_Interest.user_id == user.id, Interest.id == User_Interest.interest_id).all()
	interests_str = ""
	for interest in interests:
		interests_str += interest.name.capitalize()
		if (len(interests) - 1 != interests.index(interest)):
			interests_str += ", "

	return interests, interests_str


def check_and_update_interests(prof_interests, user_id):
	"""check the db for exisitng interest, otherwise update if non existent"""
	# delete all previous user interests to prepare for update_event
	user = db.session.query(User).get(user_id)

	for i in user.user_interests:
		db.session.delete(i)
		db.session.commit()

	# parse interests
	arr = prof_interests.lower().split(', ')

	# search each interest in the array in the database
	for i in arr:
		# if empty string, just empty database
		if i:
			interest_1 = db.session.query(Interest).filter(Interest.name == i).first()
			if interest_1 is not None:
				user_interest = User_Interest(user_id=user_id, interest_id=interest_1.id)
				db.session.add(user_interest)
				db.session.commit()
			else:
				interest = Interest(name=i)
				db.session.add(interest)
				db.session.commit()
				user_interest = User_Interest(user_id=user_id, interest_id=interest.id)
				db.session.add(user_interest)
				db.session.commit()
