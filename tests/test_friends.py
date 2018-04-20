import sys
import os.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir, 'app')))
import unittest
from main import app
from app.models import *
from sample_db import example_data
from app.friends import *
from app import connect_to_db
from json import loads
from app.routes import add_friend, accept_friend, unfriend, delete_friend_request
from flask_login import login_user, logout_user


def convert_user_list(user_list):
	id_list = []
	for user in user_list:
		id_list.append(user.id)
	return id_list


class FlaskTestFriends(unittest.TestCase):

	def setUp(self):
		"""Do before every test"""

		# Get the Flask test client
		self.client = app.test_client()
		app.config['TESTING'] = True
		self._ctx = app.test_request_context()
		self._ctx.push()

		# Connect to test database
		connect_to_db(app, 'sqlite:////tmp/test.db')

		# Create tables and add sample data
		db.create_all()
		example_data()

	def tearDown(self):
		"""Do at end of every test"""

		if self._ctx is not None:
			self._ctx.pop()

		db.session.close()
		db.drop_all()

	"""Test friend functions"""

	def test_are_friends_or_pending(self):
		are_friends, is_pending_sent, is_pending_received = are_friends_or_pending(1, 2)
		self.assertTrue(are_friends)
		self.assertIsNone(is_pending_sent)
		self.assertIsNone(is_pending_received)
		are_friends, is_pending_sent, is_pending_received = are_friends_or_pending(3, 4)
		self.assertIsNone(are_friends)
		self.assertEqual(is_pending_sent.id, 2)
		self.assertIsNone(is_pending_received)
		are_friends, is_pending_sent, is_pending_received = are_friends_or_pending(1, 4)
		self.assertIsNone(are_friends)
		self.assertIsNone(is_pending_sent)
		self.assertIsNone(is_pending_received)

	def test_are_connected(self):
		self.assertTrue(are_connected(1, 2))
		self.assertTrue(are_connected(3, 4))
		self.assertTrue(are_connected(5, 6))
		self.assertTrue(are_connected(6, 5))
		self.assertTrue(are_connected(6, 8))
		self.assertTrue(are_connected(8, 6))
		self.assertFalse(are_connected(9, 15))
		self.assertFalse(are_connected(12, 9))
		self.assertFalse(are_connected(10, 11))

	def test_get_friends(self):
		friends = get_friends(1)
		self.assertEqual(len(friends), 1)
		self.assertEqual(friends[0].id, 2)
		friends = get_friends(3)
		self.assertEqual(len(friends), 0)

	def test_get_friend_requests(self):
		received, sent = get_friend_requests(15)
		self.assertEqual(convert_user_list(received), [14, 16])
		self.assertEqual(convert_user_list(sent), [12, 13])
		received, sent = get_friend_requests(16)
		self.assertEqual(convert_user_list(received), [13])
		self.assertEqual(convert_user_list(sent), [15])
		received, sent = get_friend_requests(14)
		self.assertEqual(received, [])
		self.assertEqual(convert_user_list(sent), [15])
		received, sent = get_friend_requests(10)
		self.assertEqual(received, [])
		self.assertEqual(sent, [])
		received, sent = get_friend_requests(1)
		self.assertEqual(received, [])
		self.assertEqual(sent, [])
		received, sent = get_friend_requests(2)
		self.assertEqual(received, [])
		self.assertEqual(sent, [])

	def test_have_pending_requests(self):
		received, sent = have_pending_requests(15)
		self.assertEqual(received.id, 14)
		self.assertEqual(sent.id, 12)
		received, sent = have_pending_requests(1)
		self.assertIsNone(received)
		self.assertIsNone(sent)
		received, sent = have_pending_requests(2)
		self.assertIsNone(received)
		self.assertIsNone(sent)
		received, sent = have_pending_requests(14)
		self.assertIsNone(received)
		self.assertEqual(sent.id, 15)
		received, sent = have_pending_requests(13)
		self.assertEqual(received.id, 15)
		self.assertEqual(sent.id, 16)
		received, sent = have_pending_requests(12)
		self.assertEqual(received.id, 15)
		self.assertIsNone(sent)

	def test_get_non_friends(self):
		non_friends = get_non_friends(1)
		self.assertEqual(convert_user_list(non_friends), [3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16])
		non_friends = get_non_friends(2)
		self.assertEqual(convert_user_list(non_friends), [3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16])
		non_friends = get_non_friends(3)
		self.assertEqual(convert_user_list(non_friends), [1, 2, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16])
		non_friends = get_non_friends(4)
		self.assertEqual(convert_user_list(non_friends), [1, 2, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16])
		non_friends = get_non_friends(10)
		self.assertEqual(convert_user_list(non_friends), [1, 2, 3, 4, 5, 6, 7, 8, 9, 11, 12, 13, 14, 15, 16])
		non_friends = get_non_friends(15)
		self.assertEqual(convert_user_list(non_friends), [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11])
		non_friends = get_non_friends(9)
		self.assertEqual(convert_user_list(non_friends), [1, 2, 3, 4, 7, 10, 11, 12, 13, 15, 16])

	def test_find_friend(self):
		data = find_friend("Dan", 6)
		self.assertEqual(data["status"], "multiple")
		self.assertEqual(len(data["results"]), 2)
		self.assertEqual(data["results"][0]["id"], 8)
		self.assertEqual(data["results"][1]["id"], 9)
		data = find_friend("Dan Smith", 6)
		self.assertEqual(data["status"], "single")
		self.assertEqual(data["results"].id, 8)
		data = find_friend("Ellen", 6)
		self.assertEqual(data["status"], "single")
		self.assertEqual(data["results"].id, 5)
		data = find_friend("Katie", 6)
		self.assertEqual(data["status"], "none")
		data = find_friend("Katie Wolf", 6)
		self.assertEqual(data["status"], "none")
		data = find_friend("Dan", 8)
		self.assertEqual(data["status"], "multiple")
		self.assertEqual(len(data["results"]), 2)
		self.assertEqual(data["results"][0]["id"], 7)
		self.assertEqual(data["results"][1]["id"], 9)
		data = find_friend("Karen", 1)
		self.assertEqual(data["status"], "none")
		data = find_friend("Karen Smith", 1)
		self.assertEqual(data["status"], "none")

	"""Friend post routes"""

	def test_add_friend(self):
		login_user(User.query.get(1))
		self.assertFalse(are_connected(1, 10))
		result = add_friend(10)
		self.assertTrue(are_connected(1, 10))
		self.assertIsNotNone(Friends.query.filter_by(user_id_1=1, user_id_2=10, status=FriendStatus.requested))
		self.assertEqual("Request sent.", result)
		self.assertTrue(are_connected(1, 2))
		result = add_friend(2)
		self.assertEqual("You are already friends.", result)
		self.assertFalse(are_connected(1, 1))
		result = add_friend(1)
		self.assertEqual("You cannot add yourself as a friend.", result)
		self.assertFalse(are_connected(1, 1))
		logout_user()
		login_user(User.query.get(5))
		self.assertIsNotNone(Friends.query.filter_by(user_id_1=5, user_id_2=6, status=FriendStatus.requested))
		result = add_friend(6)
		self.assertEqual("Your friend request is pending.", result)
		self.assertIsNotNone(Friends.query.filter_by(user_id_1=7, user_id_2=5, status=FriendStatus.requested))
		result = add_friend(7)
		self.assertEqual("You have already received a request from this user.", result)

	def test_accept_friend(self):
		login_user(User.query.get(6))
		request = Friends.query.filter_by(user_id_1=5, user_id_2=6).first()
		self.assertEqual(request.status, FriendStatus.requested)
		result = accept_friend(5)
		data = loads(result.get_data())
		self.assertEqual(request.status, FriendStatus.accepted)
		self.assertEqual(data["status"], "Request accepted.")
		result = accept_friend(6)
		self.assertEqual(result, "You cannot add yourself as a friend.")
		request = Friends.query.filter_by(user_id_1=6, user_id_2=8).first()
		self.assertEqual(request.status, FriendStatus.accepted)
		result = accept_friend(8)
		self.assertEqual(result, "You are already friends.")

	def test_unfriend(self):
		login_user(User.query.get(6))
		request = Friends.query.filter_by(user_id_1=6, user_id_2=8).first()
		self.assertEqual(request.status, FriendStatus.accepted)
		result = unfriend(8)
		data = loads(result.get_data())
		self.assertIsNone(Friends.query.filter_by(user_id_1=6, user_id_2=8).first())
		self.assertEqual(data["status"], "Sucessfully unfriended.")
		request = Friends.query.filter_by(user_id_1=6, user_id_2=2).first()
		self.assertIsNone(request)
		request = Friends.query.filter_by(user_id_1=2, user_id_2=6).first()
		self.assertIsNone(request)
		result = unfriend(2)
		self.assertEqual(result, "You cannot unfriend this user.")
		result = unfriend(6)
		self.assertEqual(result, "You cannot unfriend this user.")
		logout_user()
		login_user(User.query.get(15))
		request = Friends.query.filter_by(user_id_1=15, user_id_2=12, status=FriendStatus.requested).first()
		self.assertIsNotNone(request)
		result = unfriend(12)
		self.assertEqual(result, "You cannot unfriend this user.")
		request = Friends.query.filter_by(user_id_1=16, user_id_2=15, status=FriendStatus.requested).first()
		self.assertIsNotNone(request)
		result = unfriend(16)
		self.assertEqual(result, "You cannot unfriend this user.")

	def test_delete_friend_request(self):
		login_user(User.query.get(15))
		request = Friends.query.filter_by(user_id_1=16, user_id_2=15, status=FriendStatus.requested).first()
		self.assertIsNotNone(request)
		result = delete_friend_request(16)
		self.assertEqual(result, "Request removed.")
		request = Friends.query.filter_by(user_id_1=16, user_id_2=15, status=FriendStatus.requested).first()
		self.assertIsNone(request)
		request = Friends.query.filter_by(user_id_1=15, user_id_2=12, status=FriendStatus.requested).first()
		self.assertIsNotNone(request)
		result = delete_friend_request(12)
		self.assertEqual(result, "You cannot remove this request.")
		result = delete_friend_request(15)
		self.assertEqual(result, "You cannot remove this request.")
		request = Friends.query.filter_by(user_id_1=15, user_id_2=2).first()
		self.assertIsNone(request)
		request = Friends.query.filter_by(user_id_1=2, user_id_2=15).first()
		self.assertIsNone(request)
		result = delete_friend_request(2)
		self.assertEqual(result, "You cannot remove this request.")
		logout_user()
		login_user(User.query.get(6))
		request = Friends.query.filter_by(user_id_1=6, user_id_2=8, status=FriendStatus.accepted).first()
		self.assertIsNotNone(request)
		result = delete_friend_request(8)
		self.assertEqual(result, "You cannot remove this request.")
		request = Friends.query.filter_by(user_id_1=9, user_id_2=6, status=FriendStatus.accepted).first()
		self.assertIsNotNone(request)
		result = delete_friend_request(9)
		self.assertEqual(result, "You cannot remove this request.")


if __name__ == '__main__':
	unittest.main()
