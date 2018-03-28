import sys
import os.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir, 'app')))
import unittest
from main import app
from app.models import *
from sample_db import example_data
from app.friends import *
from app.messages import *
from app import connect_to_db


class FlaskTestDatabase(unittest.TestCase):

	def setUp(self):
		"""Do before every test"""

		# Get the Flask test client
		self.client = app.test_client()
		app.config['TESTING'] = True

		# Connect to test database
		connect_to_db(app, 'sqlite:////tmp/test.db')

		# Create tables and add sample data
		db.create_all()
		example_data()

	def tearDown(self):
		"""Do at end of every test"""

		db.session.close()
		db.drop_all()

	"""Test friend functions"""

	def test_are_friends_or_pending(self):
		are_friends, is_pending_sent, is_pending_recieved = are_friends_or_pending(1, 2)
		self.assertEqual(are_friends, True)
		self.assertEqual(is_pending_sent, None)
		self.assertEqual(is_pending_recieved, None)
		are_friends, is_pending_sent, is_pending_recieved = are_friends_or_pending(3, 4)
		self.assertEqual(are_friends, None)
		self.assertEqual(is_pending_sent.id, 2)
		self.assertEqual(is_pending_recieved, None)
		are_friends, is_pending_sent, is_pending_recieved = are_friends_or_pending(1, 4)
		self.assertEqual(are_friends, None)
		self.assertEqual(is_pending_sent, None)
		self.assertEqual(is_pending_recieved, None)

	def test_get_friends(self):
		friends = get_friends(1)
		self.assertEqual(len(friends), 1)
		self.assertEqual(friends[0].id, 2)
		friends = get_friends(3)
		self.assertEqual(len(friends), 0)

	def test_find_friend(self):
		friend_id = find_friend('dale')
		self.assertEqual(friend_id.id, 2)
		friend_id = find_friend('abc')
		self.assertEqual(friend_id, None)


	"""Test conversation functions"""

	def test_conversation_exists(self):
		self.assertEqual(conversation_exists(1, 2).id, 1)
		self.assertEqual(conversation_exists(2, 1).id, 1)
		self.assertEqual(conversation_exists(3, 2), None)
		self.assertEqual(conversation_exists(7, 10), None)

	def test_update_read_messages(self):
		unread = Message.query.filter_by(conversation_id=1, read=False, sender=2).all()
		self.assertEqual(len(unread), 2)
		unread = update_read_messages(1, 1)
		self.assertEqual(unread, None)

	def test_most_recent_message(self):
		msg = most_recent_message(1)
		self.assertEqual(msg.id, 3)
		msg = most_recent_message(2)
		self.assertEqual(msg.id, 3)
		msg = most_recent_message(3)
		self.assertEqual(msg, None)

	def test_unread_messages(self):
		msg_count, conversations = unread_messages(1)
		self.assertEqual(msg_count, 2)
		self.assertEqual(conversations[0][0].id, 1)
		self.assertEqual(conversations[0][2].id, 2)
		msg_count, conversations = unread_messages(2)
		self.assertEqual(msg_count, 0)

	def test_build_conversation(self):
		conversation_id = build_conversation(3, 4)
		c_id = Conversation.query.filter_by(user_id_1=3, user_id_2=4).first().id
		self.assertEqual(conversation_id, c_id)
		conversation_id = build_conversation(2, 1)
		self.assertEqual(conversation_id, 1)


	"""Test Login"""

	# def test_login(self):
	# 	result = self.client.post("/login", data={"email": "karen@example.com", "password": "karen"}, follow_redirects=True)
	# 	self.assertEqual(result.status_code, 200)
	# 	self.assertIn("You have successfully logged in", result.data)

	# def test_signup_new_user(self):
	# 	result = self.client.post("/register", data={"email": "dan@test.com", "password": "dan", "password_repeat": "dan", "fname": "Dan", "lname": "Test"}, follow_redirects=True)
	# 	self.assertEqual(result.status_code, 200)
	# 	self.assertIn("Congratulations, you are now a registered user!", result.data)


if __name__ == '__main__':
	unittest.main()
