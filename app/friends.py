"""Functions for the connection/relationship between users"""

from app.models import Friends, User, FriendStatus
from app.models import db


def are_friends_or_pending(user_id_1, user_id_2):
	are_friends_sent = Friends.query.filter_by(user_id_1=user_id_1, user_id_2=user_id_2, status=FriendStatus.accepted).first()
	are_friends_recieved = Friends.query.filter_by(user_id_1=user_id_2, user_id_2=user_id_1, status=FriendStatus.accepted).first()
	if are_friends_sent:
		are_friends = are_friends_sent
	else:
		are_friends = are_friends_recieved
	if are_friends_sent is not None or are_friends_recieved is not None:
		are_friends = True
	is_pending_sent = Friends.query.filter_by(user_id_1=user_id_1, user_id_2=user_id_2, status=FriendStatus.requested).first()
	is_pending_recieved = Friends.query.filter_by(user_id_1=user_id_2, user_id_2=user_id_1, status=FriendStatus.requested).first()
	return are_friends, is_pending_sent, is_pending_recieved


def are_connected(user_id_1, user_id_2):
	are_friends, is_pending_sent, is_pending_recieved = are_friends_or_pending(user_id_1, user_id_2)
	if are_friends or is_pending_sent or is_pending_recieved:
		return True
	else:
		return False


def get_friend_requests(user_id):
	received_friend_requests = db.session.query(User).filter(Friends.user_id_2 == user_id, Friends.status == FriendStatus.requested).join(Friends, Friends.user_id_1 == User.id).all()
	sent_friend_requests = db.session.query(User).filter(Friends.user_id_1 == user_id, Friends.status == FriendStatus.requested).join(Friends, Friends.user_id_2 == User.id).all()
	return received_friend_requests, sent_friend_requests


def have_pending_requests(user_id):
	pending_recieved = db.session.query(User).filter(Friends.user_id_2 == user_id, Friends.status == FriendStatus.requested).join(Friends, Friends.user_id_1 == User.id).first()
	pending_sent = db.session.query(User).filter(Friends.user_id_1 == user_id, Friends.status == FriendStatus.requested).join(Friends, Friends.user_id_2 == User.id).first()
	return pending_recieved, pending_sent


def get_friends(user_id):
	f1 = db.session.query(User).filter(Friends.user_id_1 == user_id, Friends.status == FriendStatus.accepted).join(Friends, Friends.user_id_2 == User.id)
	f2 = db.session.query(User).filter(Friends.user_id_2 == user_id, Friends.status == FriendStatus.accepted).join(Friends, Friends.user_id_1 == User.id)
	friends = f1.union(f2).all()
	return friends


def get_non_friends(user_id):
	f1 = db.session.query(User).join(Friends, Friends.user_id_1 == User.id).filter(Friends.user_id_1 != user_id, Friends.user_id_2 != user_id)
	f2 = db.session.query(User).join(Friends, Friends.user_id_2 == User.id).filter(Friends.user_id_1 != user_id, Friends.user_id_2 != user_id)
	non_friends = f1.union(f2)
	return non_friends


def friend_search(users, current_user_id):
	connected = False
	if len(users) == 1:
		connected = are_connected(users[0].id, current_user_id)
	if len(users) < 1 or (len(users) == 1 and (users[0].id == current_user_id or not connected)):
		return {"status": "none", "results": "Your search did not return any results."}
	elif len(users) > 1:
		return {"status": "multiple", "results": [u.serialize() for u in users]}
	else:
		return {"status": "single", "results": users[0]}


def find_friend(name, current_user_id):
	names = name.split(' ')
	if len(names) == 1:
		users = User.query.filter_by(fname=names[0]).all()
	elif len(names) > 1:
		users = User.query.filter_by(fname=names[0], lname=names[1]).all()
	if len(users) > 1:
		connected_users = []
		for user in users:
			connected = are_connected(user.id, current_user_id)
			if user.id != current_user_id and connected:
				connected_users.append(user)
		return friend_search(connected_users, current_user_id)
	return friend_search(users, current_user_id)
