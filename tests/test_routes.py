import sys
import os.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir, 'app')))
import unittest
from main import app
from app.models import *
from sample_db import example_data
from app import connect_to_db
from app.routes import *
from json import loads
from app.friends import are_connected


def notification_exists(event_id, receiver_id, notification_type):
	return db.session.query(Notification).filter(Notification.event_id == event_id, Notification.receiver_id == receiver_id, Notification.type == notification_type).first()


class FlaskTestRoutes(unittest.TestCase):

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

	"""Test routes"""

	# def test_login(self):
	# 	with self.client:
	# 		result = self.client.post("/login", data={"email": "karen@example.com", "password": "karen"}, follow_redirects=True)
	# 		self.assertEquals(current_user.username, 'dale')
	# 		self.assertEqual(result.status_code, 200)
	# 		self.assertIn("Discover", result.data)

	# def test_register_page(self):
	# 	result = register()
	# 	self.assertIn("Sign Up", result)
		# u = User.query.get(1)
		# login_user(u)
		# result = self.client.get("/register", follow_redirects=True)
		# self.assertIn('Discover', result.data)

	# def test_user_page(self):
	# 	login_user(User.query.get(1))
	# 	result = user(1)
	# 	self.assertIn('Karen Smith', result)
	# 	self.assertIn("<div class='block profile-basic'>", result)
	# 	self.assertNotIn("<button class='button button-2'>Message</button>", result)
	# 	result = user(2)
	# 	self.assertIn('Dale Sue', result)
	# 	self.assertIn('<a href="/conversation/1">', result)
	# 	self.assertIn('<button class="button button-2">Message</button>', result)
	# 	self.assertIn("<button class='button button-2 disabled'>Friends</button>", result)
	# 	result = user(6)
	# 	self.assertIn('Katie Wolf', result)
	# 	self.assertIn('<a href="/create_conversation/6">', result)
	# 	self.assertIn('<button class="button button-2">Message</button>', result)
	# 	self.assertIn('<button type="submit" class=\'button button-2\'>Connect</button>', result)
	# 	logout_user()
	# 	login_user(User.query.get(5))
	# 	result = user(6)
	# 	self.assertIn('Katie Wolf', result)
	# 	self.assertIn("<button class='button button-2 disabled'>Pending</button>", result)

	# def test_friends_page(self):
	# 	login_user(User.query.get(1))
	# 	result = friends(1)
	# 	self.assertIn('Karen Smith', result)
	# 	self.assertIn("<h2 class='block-title'>Connections</h2>", result)
	# 	self.assertIn("<button type=\"submit\" class='button button-3' id=\"unfriend-btn\">Unfriend</button>", result)
	# 	result = friends(2)
	# 	self.assertIn('Dale Sue', result)
	# 	self.assertNotIn("<button type=\"submit\" class='button button-3' id=\"unfriend-btn\">Unfriend</button>", result)

	# def test_add_friend(self):
	# 	login_user(User.query.get(1))
	# 	self.assertFalse(are_connected(1, 10))
	# 	result = add_friend(10)
	# 	self.assertTrue(are_connected(1, 10))
	# 	self.assertIsNotNone(Friends.query.filter_by(user_id_1=1, user_id_2=10, status=FriendStatus.requested))
	# 	self.assertEqual("Request sent.", result)
	# 	self.assertTrue(are_connected(1, 2))
	# 	result = add_friend(2)
	# 	self.assertEqual("You are already friends.", result)
	# 	self.assertFalse(are_connected(1, 1))
	# 	result = add_friend(1)
	# 	self.assertEqual("You cannot add yourself as a friend.", result)
	# 	self.assertFalse(are_connected(1, 1))
	# 	logout_user()
	# 	login_user(User.query.get(5))
	# 	self.assertIsNotNone(Friends.query.filter_by(user_id_1=5, user_id_2=6, status=FriendStatus.requested))
	# 	result = add_friend(6)
	# 	self.assertEqual("Your friend request is pending.", result)
	# 	self.assertIsNotNone(Friends.query.filter_by(user_id_1=7, user_id_2=5, status=FriendStatus.requested))
	# 	result = add_friend(7)
	# 	self.assertEqual("You have already received a request from this user.", result)

	def test_accept_friend(self):
		login_user(User.query.get(6))
		request = Friends.query.filter_by(user_id_1=5, user_id_2=6).first()
		self.assertEqual(request.status, FriendStatus.requested)
		result = accept_friend(5)
		self.assertEqual(request.status, FriendStatus.accepted)
		self.assertEqual("Request accepted.", result)

	# def test_create_conversation(self):
	# 	login_user(User.query.get(1))
	# 	self.assertIsNone(Conversation.query.filter_by(user_id_1=1, user_id_2=10).first())
	# 	self.assertIsNone(Conversation.query.filter_by(user_id_1=10, user_id_2=1).first())
	# 	result = create_conversation(10)
	# 	self.assertIsNotNone(Conversation.query.filter_by(user_id_1=1, user_id_2=10).first())
	# 	self.assertEqual(result.status_code, 302)
	# 	self.assertIsNotNone(Conversation.query.filter_by(user_id_1=1, user_id_2=2).first())
	# 	result = create_conversation(2)
	# 	self.assertEqual(result.status_code, 302)

	# def test_post_conversation_single(self):
	# 	u = User.query.get(1)
	# 	login_user(u)
	# 	self.assertIsNotNone(Conversation.query.filter_by(user_id_1=1, user_id_2=2).first())
	# 	response = post_conversation_single(2)
	# 	data = loads(response.get_data())
	# 	self.assertEqual(data["status"], "conversation exists")
	# 	self.assertIsNone(Conversation.query.filter_by(user_id_1=1, user_id_2=10).first())
	# 	self.assertIsNone(Conversation.query.filter_by(user_id_1=10, user_id_2=1).first())
	# 	response = post_conversation_single(10)
	# 	data = loads(response.get_data())
	# 	self.assertEqual(data["status"], "new conversation")
	# 	self.assertEqual(data["friend"]["id"], 10)
	# 	self.assertIsNotNone(Conversation.query.filter_by(user_id_1=1, user_id_2=10).first())

	# def test_discover_page(self):
	# 	login_user(User.query.get(1))
	# 	result = discover()
	# 	self.assertIn("<h2 class='page-block-title left-page-title'>Discover</h2>", result)
	# 	self.assertIn("Matt Anderson", result)
	# 	self.assertIn("Ellen James", result)
	# 	self.assertIn("Katie Wolf", result)
	# 	self.assertIn("Jake Brown", result)
	# 	self.assertIn("Dan Kay", result)
	# 	self.assertNotIn("Dale Sue", result)
	# 	self.assertNotIn("Dylan Parker", result)
	# 	self.assertNotIn("Karen Smith", result)

	# def test_account_page(self):
	# 	login_user(User.query.get(1))
	# 	result = account()
	# 	self.assertIn('<div class=\'block account\'>', result)
	# 	self.assertIn('<span id=\'username-main\'>karen</span>', result)

	# def test_delete_account(self):
	# 	login_user(User.query.get(1))
	# 	self.assertIsNotNone(User.query.get(1))
	# 	result = delete_account()
	# 	self.assertEqual(result.status_code, 302)
	# 	self.assertIsNone(User.query.get(1))

	# def test_event_page(self):
	# 	login_user(User.query.get(1))
	# 	result = event(1)
	# 	self.assertIn("<span id='title-main'>Event 1</span>", result)
	# 	self.assertIn("<button class='button button-1' id='edit-event-btn'>Edit</button>", result)
	# 	self.assertIn("<h2 class='page-title'>Invited</h2>", result)
	# 	self.assertIn("<button class='non-btn add-friends'>+ Add More Friends</button>", result)
	# 	self.assertNotIn("<button type=\"submit\" class='button button-1'>Accept</button>", result)
	# 	self.assertNotIn("<button type=\"submit\" class='button button-5'>Decline</button>", result)
	# 	result = event(2)
	# 	self.assertIn("<span id='title-main'>Event 2</span>", result)
	# 	self.assertNotIn("<button class='button button-1' id='edit-event-btn'>Edit</button>", result)
	# 	self.assertNotIn("<h2 class='page-title'>Invited</h2>", result)
	# 	self.assertIn("<div class='adding-friends-hidden'>", result)
	# 	self.assertIn("Invitation sent by Dale Sue", result)
	# 	self.assertIn("<button type=\"submit\" class='button button-1'>Accept</button>", result)
	# 	self.assertIn("<button type=\"submit\" class='button button-5'>Decline</button>", result)
	# 	result = event(4)
	# 	self.assertIn("<span id='title-main'>Event 4</span>", result)
	# 	self.assertIn("<h2 class='page-title'>Invited</h2>", result)
	# 	self.assertIn("Dale Sue", result)
	# 	self.assertIn("Matt Anderson", result)
	# 	self.assertIn("Jake Brown", result)
	# 	self.assertNotIn("Karen Smith", result)
	# 	self.assertIn("<button class='non-btn add-friends'>+ Add More Friends</button>", result)
	# 	logout_user()
	# 	login_user(User.query.get(3))
	# 	result = event(4)
	# 	self.assertIn("<span id='title-main'>Event 4</span>", result)
	# 	self.assertIn("<h2 class='page-title'>Invited</h2>", result)
	# 	self.assertNotIn("<button class='button button-1' id='edit-event-btn'>Edit</button>", result)
	# 	self.assertIn("<button type=\"submit\" class='button button-1'>Accept</button>", result)
	# 	self.assertIn("<button type=\"submit\" class='button button-5'>Decline</button>", result)
	# 	self.assertIn("<h2 class='page-title'>Invited</h2>", result)
	# 	self.assertIn("Dale Sue", result)
	# 	self.assertIn("Karen Smith", result)
	# 	self.assertIn("Jake Brown", result)
	# 	self.assertNotIn("Matt Anderson", result)
	# 	self.assertIn("<div class='adding-friends-hidden'>", result)
	# 	result = event(1)
	# 	self.assertEqual(result.status_code, 302)

	# def test_event_new_page(self):
	# 	login_user(User.query.get(1))
	# 	result = event_new()
	# 	self.assertIn("<h1 id='event-title' class='page-title-large'>New Event</h1>", result)
	# 	self.assertIn("<form id='create-event-form' action=\"/event/create/\" method=\"post\">", result)

	# def test_accept_invitation(self):
	# 	login_user(User.query.get(2))
	# 	self.assertFalse(UserEvent.query.get(2).accepted)
	# 	self.assertIsNotNone(Notification.query.get(1))
	# 	self.assertIsNotNone(EventInvitation.query.get(1))
	# 	self.assertIsNone(notification_exists(1, 1, NotificationType.invite_accepted))
	# 	response = accept_invitation(2)
	# 	data = loads(response.get_data())
	# 	self.assertEqual(data[0], "Invitation accepted.")
	# 	self.assertTrue(UserEvent.query.get(2).accepted)
	# 	self.assertIsNone(Notification.query.get(1))
	# 	self.assertIsNone(EventInvitation.query.get(1))
	# 	self.assertIsNotNone(notification_exists(1, 1, NotificationType.invite_accepted))

	# def test_decline_invitation(self):
	# 	login_user(User.query.get(1))
	# 	self.assertIsNotNone(UserEvent.query.get(4))
	# 	self.assertFalse(UserEvent.query.get(4).accepted)
	# 	self.assertIsNotNone(Notification.query.get(2))
	# 	self.assertIsNotNone(EventInvitation.query.get(2))
	# 	self.assertIsNone(notification_exists(2, 2, NotificationType.invite_declined))
	# 	result = decline_invitation(4)
	# 	self.assertEqual(result.status_code, 302)
	# 	self.assertIsNone(UserEvent.query.get(4))
	# 	self.assertIsNone(Notification.query.get(2))
	# 	self.assertIsNone(EventInvitation.query.get(2))
	# 	self.assertIsNotNone(notification_exists(2, 2, NotificationType.invite_declined))

	# def test_remove_event(self):
	# 	login_user(User.query.get(1))
	# 	self.assertIsNotNone(UserEvent.query.get(8))
	# 	self.assertIsNone(notification_exists(4, 2, NotificationType.event_removed))
	# 	self.assertIsNone(notification_exists(4, 3, NotificationType.event_removed))
	# 	self.assertIsNone(notification_exists(4, 4, NotificationType.event_removed))
	# 	result = remove_event(8)
	# 	self.assertEqual(result.status_code, 302)
	# 	self.assertIsNone(UserEvent.query.get(8))
	# 	self.assertIsNotNone(notification_exists(4, 2, NotificationType.event_removed))
	# 	self.assertIsNotNone(notification_exists(4, 3, NotificationType.event_removed))
	# 	self.assertIsNotNone(notification_exists(4, 4, NotificationType.event_removed))

	# def test_add_invite_single(self):
	# 	login_user(User.query.get(1))
	# 	self.assertIsNone(UserEvent.query.filter_by(event_id=1, user_id=3).first())
	# 	self.assertIsNone(EventInvitation.query.filter_by(sender_id=1, receiver_id=3, event_id=1).first())
	# 	self.assertIsNone(Notification.query.filter_by(receiver_id=3, event_id=1, type=NotificationType.event_invite).first())
	# 	response = add_invite_single(1, 3)
	# 	data = loads(response.get_data())
	# 	self.assertEqual(data["id"], 3)
	# 	self.assertIsNotNone(UserEvent.query.filter_by(event_id=1, user_id=3).first())
	# 	self.assertIsNotNone(EventInvitation.query.filter_by(sender_id=1, receiver_id=3, event_id=1).first())
	# 	self.assertIsNotNone(Notification.query.filter_by(receiver_id=3, event_id=1, type=NotificationType.event_invite).first())


if __name__ == '__main__':
	unittest.main()