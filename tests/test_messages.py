import sys
import os.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir, 'app')))
import unittest
from main import app
from app.models import *
from sample_db import example_data
from app.messages import *
from app import connect_to_db
from json import loads


def convert_tuple_list(list):
	id_list = []
	for (user, conversation) in list:
		id_list.append((user.id, conversation.id))
	return id_list


class FlaskTestMessages(unittest.TestCase):

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


	"""Test conversation functions"""

	def test_get_conversations(self):
		conversations = get_conversations(1)
		self.assertEqual(convert_tuple_list(conversations), [(2, 1), (4, 2)])
		conversations = get_conversations(3)
		self.assertEqual(conversations, [])
		conversations = get_conversations(8)
		self.assertEqual(convert_tuple_list(conversations), [(5, 3), (7, 4), (9, 5), (12, 6)])
		conversations = get_conversations(12)
		self.assertEqual(convert_tuple_list(conversations), [(8, 6)])

	def test_update_read_messages(self):
		unread = Message.query.filter_by(conversation_id=1, read=False, sender=2).all()
		self.assertEqual(len(unread), 2)
		unread = update_read_messages(1, 1)
		self.assertIsNone(unread)

	def test_most_recent_message(self):
		msg = most_recent_message(1)
		self.assertEqual(msg.id, 3)
		msg = most_recent_message(2)
		self.assertEqual(msg.id, 3)
		msg = most_recent_message(3)
		self.assertIsNone(msg)

	def test_unread_messages(self):
		msg_count, conversations = unread_messages(1)
		self.assertEqual(msg_count, 2)
		self.assertEqual(conversations[0][0].id, 1)
		self.assertEqual(conversations[0][2].id, 2)
		msg_count, conversations = unread_messages(2)
		self.assertEqual(msg_count, 0)

	def test_conversation_exists(self):
		self.assertEqual(conversation_exists(1, 2).id, 1)
		self.assertEqual(conversation_exists(2, 1).id, 1)
		self.assertIsNone(conversation_exists(3, 2))
		self.assertIsNone(conversation_exists(25, 50))

	def test_build_conversation(self):
		conversation_id = build_conversation(3, 4)
		c_id = Conversation.query.filter_by(user_id_1=3, user_id_2=4).first().id
		self.assertEqual(conversation_id, c_id)
		conversation_id = build_conversation(2, 1)
		self.assertEqual(conversation_id, 1)

	def test_get_conversation(self):
		conversation = get_conversation(1)
		self.assertEqual(conversation.id, 1)
		conversation = get_conversation(40)
		self.assertIsNone(conversation)

	def test_post_single(self):
		with app.test_request_context():
			f = User.query.get(2)
			u = User.query.get(1)
			self.assertIsNotNone(conversation_exists(1, 2))
			response = post_single(f, u)
			data = loads(response.get_data())
			self.assertEqual(data["status"], "conversation exists")
			f = User.query.get(13)
			u = User.query.get(14)
			self.assertIsNone(conversation_exists(13, 14))
			response = post_single(f, u)
			data = loads(response.get_data())
			self.assertEqual(data["status"], "new conversation")
			self.assertEqual(data["friend"]["id"], 13)
			self.assertEqual(conversation_exists(13, 14).id, 7)

	def test_post_conversation(self):
		with app.test_request_context():
			user = User.query.get(15)
			self.assertIsNone(conversation_exists(15, 16))
			response = post_conversation("Dylan", user)
			data = loads(response.get_data())
			self.assertEqual(data["status"], "new conversation")
			self.assertEqual(data["friend"]["id"], 16)
			self.assertEqual(conversation_exists(15, 16).id, 7)

			user = User.query.get(13)
			self.assertIsNone(conversation_exists(13, 14))
			response = post_conversation("Blaine Davis", user)
			data = loads(response.get_data())
			self.assertEqual(data["status"], "new conversation")
			self.assertEqual(data["friend"]["id"], 14)
			self.assertEqual(conversation_exists(13, 14).id, 8)

			user = User.query.get(1)
			response = post_conversation("Karen", user)
			data = loads(response.get_data())
			self.assertEqual(data["status"], "none")
			self.assertEqual(data["results"], "Your search did not return any results.")

			response = post_conversation("Abc", user)
			data = loads(response.get_data())
			self.assertEqual(data["status"], "none")
			self.assertEqual(data["results"], "Your search did not return any results.")

			response = post_conversation("Katie Wolf", user)
			data = loads(response.get_data())
			self.assertEqual(data["status"], "none")
			self.assertEqual(data["results"], "Your search did not return any results.")

			self.assertIsNotNone(conversation_exists(1, 2))
			response = post_conversation("Dale", user)
			data = loads(response.get_data())
			self.assertEqual(data["status"], "conversation exists")
			self.assertEqual(data["friend"]["id"], 2)

			response = post_conversation("Dale Sue", user)
			data = loads(response.get_data())
			self.assertEqual(data["status"], "conversation exists")
			self.assertEqual(data["friend"]["id"], 2)

if __name__ == '__main__':
	unittest.main()
