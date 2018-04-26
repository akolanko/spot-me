from app.models import *
from app import db
from app.forms import UpdateAvailabilityForm, EditProfileForm
from app.availabilities import get_availabilities
from app.friends import are_friends_or_pending, get_friends
from app.notifications import get_notifications
from app.messages import conversation_exists
from app.accounts import calculate_age


def get_user_data(user, current_user):
	are_friends, is_pending_sent, is_pending_received = are_friends_or_pending(current_user.id, user.id)
	friends = get_friends(user.id)
	limited_friends = friends[:6]
	total_friends = len(friends)
	notifications = get_notifications(current_user.id)
	conversation = conversation_exists(user.id, current_user.id)
	age = calculate_age(user.birthday)
	return are_friends, is_pending_sent, is_pending_received, friends, limited_friends, total_friends, notifications, conversation, age


def get_profile_data(user, current_user):
	profile = user.profile
	weekdays = get_availabilities(user.id)
	availform = UpdateAvailabilityForm()
	interests, interests_str = get_user_interests(current_user)
	form = EditProfileForm()
	return profile, weekdays, availform, interests, interests_str, form


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


def update_profile(user, form):
	user.profile.about = form.about.data
	user.profile.meet = form.meet.data
	user.profile.skills = form.skills.data
	user.profile.work = form.work.data
	user.profile.location = form.location.data
	passed_interests = form.interests.data
	db.session.commit()
	check_and_update_interests(passed_interests, user.id)
