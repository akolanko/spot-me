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
