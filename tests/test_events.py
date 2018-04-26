import sys
import os.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir, 'app')))
import unittest
from main import app
from app.models import *
from sample_db import example_data
from app.events import *
from app.notifications import notification_exists
from connect import connect_to_db
from json import loads
from app.routes import event, event_new, accept_invitation, decline_invitation, remove_event, add_invite_single
from flask_login import login_user, logout_user
import datetime
from app.forms import UpdateEventForm


def convert_list(list):
	id_list = []
	for item in list:
		id_list.append(item.id)
	return id_list


def ntfn_exists(event_id, receiver_id, notification_type):
	return db.session.query(Notification).filter(Notification.event_id == event_id, Notification.receiver_id == receiver_id, Notification.type == notification_type).first()


class FlaskTestEvents(unittest.TestCase):

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

	"""Test event functions"""

	def test_create_friend_event(self):
		event = Event.query.get(4)
		sender = User.query.get(7)
		receiver_id = 8
		sender_event_exists = db.session.query(UserEvent).filter(UserEvent.event_id == event.id, UserEvent.user_id == sender.id).first()
		self.assertIsNone(sender_event_exists)
		receiver_event_exists = db.session.query(UserEvent).filter(UserEvent.event_id == event.id, UserEvent.user_id == receiver_id).first()
		self.assertIsNone(receiver_event_exists)
		invite_exists = db.session.query(EventInvitation).filter(EventInvitation.event_id == event.id, EventInvitation.sender_id == sender.id, EventInvitation.receiver_id == receiver_id).first()
		self.assertIsNone(invite_exists)
		notification_exists = db.session.query(Notification).filter(Notification.event_id == event.id, Notification.receiver_id == receiver_id, Notification.type == NotificationType.event_invite).first()
		self.assertIsNone(notification_exists)
		create_friend_event(event, sender, receiver_id)
		sender_event_exists = db.session.query(UserEvent).filter(UserEvent.event_id == event.id, UserEvent.user_id == sender.id).first()
		self.assertIsNotNone(sender_event_exists)
		self.assertTrue(sender_event_exists.accepted)
		receiver_event_exists = db.session.query(UserEvent).filter(UserEvent.event_id == event.id, UserEvent.user_id == receiver_id).first()
		self.assertIsNotNone(receiver_event_exists)
		self.assertFalse(receiver_event_exists.accepted)
		invite_exists = db.session.query(EventInvitation).filter(EventInvitation.event_id == event.id, EventInvitation.sender_id == sender.id, EventInvitation.receiver_id == receiver_id).first()
		self.assertIsNotNone(invite_exists)
		notification_exists = db.session.query(Notification).filter(Notification.event_id == event.id, Notification.receiver_id == receiver_id, Notification.type == NotificationType.event_invite).first()
		self.assertIsNotNone(notification_exists)

	def test_user_event_exists(self):
		self.assertIsNotNone(user_event_exists(1, 1))
		self.assertIsNotNone(user_event_exists(2, 1))
		self.assertIsNone(user_event_exists(8, 4))
		self.assertIsNone(user_event_exists(3, 2))
		self.assertIsNone(user_event_exists(9, 20))

	def test_get_recent_events(self):
		events = get_recent_events(1)
		self.assertEqual(convert_list(events), [4, 3, 1])
		events = get_recent_events(3)
		self.assertEqual(events, [])
		events = get_recent_events(7)
		self.assertEqual(events, [])
		events = get_recent_events(6)
		self.assertEqual(convert_list(events), [6])
		events = get_recent_events(2)
		self.assertEqual(convert_list(events), [2, 4])
		events = get_recent_events(13)
		self.assertEqual(convert_list(events), [7, 6])

	def test_get_event_invitation(self):
		sent, received = get_event_invitation(1, 1)
		self.assertIsNotNone(sent)
		self.assertIsNone(received)
		sent, received = get_event_invitation(1, 2)
		self.assertIsNone(sent)
		self.assertIsNotNone(received)
		sent, received = get_event_invitation(1, 10)
		self.assertIsNone(sent)
		self.assertIsNone(received)

	def test_create_user_event(self):
		self.assertIsNone(user_event_exists(5, 7))
		self.assertIsNone(notification_exists(5, 7))
		invite_exists = db.session.query(EventInvitation).filter(EventInvitation.event_id == 7, EventInvitation.sender_id == 13, EventInvitation.receiver_id == 5).first()
		self.assertIsNone(invite_exists)
		user_event = create_user_event(5, 7, 13)
		self.assertIsNotNone(user_event)
		self.assertIsNotNone(user_event_exists(5, 7))
		self.assertIsNotNone(notification_exists(5, 7))
		invite_exists = db.session.query(EventInvitation).filter(EventInvitation.event_id == 7, EventInvitation.sender_id == 13, EventInvitation.receiver_id == 5).first()
		self.assertIsNotNone(invite_exists)
		self.assertIsNotNone(user_event_exists(13, 6))
		user_event = create_user_event(13, 6, 6)
		self.assertIsNone(user_event)

	def test_check_results(self):
		response = check_results([], 6, 6)
		data = loads(response.get_data())
		self.assertEqual(data, "Your search did not return any results.")
		u = User.query.get(13)
		response = check_results([u], 7, 13)
		data = loads(response.get_data())
		self.assertEqual(data, "Your search did not return any results.")
		u = User.query.get(1)
		response = check_results([u], 7, 13)
		data = loads(response.get_data())
		self.assertEqual(data, "Your search did not return any results.")
		u = User.query.get(2)
		response = check_results([u], 1, 1)
		data = loads(response.get_data())
		self.assertEqual(data, "Dale is already invited.")
		u = User.query.get(2)
		response = check_results([u], 4, 1)
		data = loads(response.get_data())
		self.assertEqual(data, "Dale is already invited.")
		u = User.query.get(16)
		response = check_results([u], 7, 13)
		data = loads(response.get_data())
		self.assertEqual(data[0], "success")
		self.assertEqual(data[1]["id"], 16)
		u1 = User.query.get(9)
		u2 = User.query.get(8)
		response = check_results([u1, u2], 5, 6)
		data = loads(response.get_data())
		self.assertEqual(data[0], "multiple results")
		self.assertEqual(data[1][0]["id"], 9)
		self.assertEqual(data[1][1]["id"], 8)

	def test_post_event_update(self):
		event = Event.query.get(1)
		self.assertEqual(event.date, datetime.date(2018, 11, 30))
		self.assertEqual(event.start_time, datetime.time(20, 15))
		self.assertEqual(event.end_time, datetime.time(11, 15))
		self.assertEqual(event.title, 'Event 1')
		self.assertEqual(event.location, 'Campus')
		self.assertEqual(event.notes, 'Lorem ipsum')
		eventform = UpdateEventForm(title="Soccer", date=datetime.date(2018, 5, 10), start_time=datetime.time(13, 30), end_time=datetime.time(15, 30), location="Columbia", notes="Some notes")
		post_event_update(eventform, event)
		self.assertEqual(event.date, datetime.date(2018, 5, 10))
		self.assertEqual(event.start_time, datetime.time(13, 30))
		self.assertEqual(event.end_time, datetime.time(15, 30))
		self.assertEqual(event.title, "Soccer")
		self.assertEqual(event.location, "Columbia")
		self.assertEqual(event.notes, "Some notes")

	def test_add_event(self):
		user = User.query.get(1)
		login_user(User.query.get(1))
		event = Event.query.filter_by(title="My Event").first()
		self.assertIsNone(event)
		new_event = Event(title="My Event", date=datetime.date(2018, 9, 30), start_time=datetime.time(10, 15), end_time=datetime.time(11, 15), location='Columbia', notes='Lorem ipsum')
		add_event(new_event, user)
		event = Event.query.filter_by(title="My Event").first()
		self.assertIsNotNone(event)
		user_event = UserEvent.query.filter_by(user_id=user.id, event_id=event.id, accepted=True).first()
		self.assertIsNotNone(user_event)

	"""Test event routes"""

	def test_event_page(self):
		login_user(User.query.get(1))
		result = event(1)
		self.assertIn("<span id='title-main'>Event 1</span>", result)
		self.assertIn("<button class='button button-1' id='edit-event-btn'>Edit</button>", result)
		self.assertIn("<h2 class='page-title'>Invited</h2>", result)
		self.assertIn("<button class='non-btn add-friends'>+ Add More Friends</button>", result)
		self.assertNotIn("<button type=\"submit\" class='button button-1'>Accept</button>", result)
		self.assertNotIn("<button type=\"submit\" class='button button-5'>Decline</button>", result)
		result = event(2)
		self.assertIn("<span id='title-main'>Event 2</span>", result)
		self.assertNotIn("<button class='button button-1' id='edit-event-btn'>Edit</button>", result)
		self.assertNotIn("<h2 class='page-title'>Invited</h2>", result)
		self.assertIn("<div class='adding-friends-hidden'>", result)
		self.assertIn("Invitation sent by Dale Sue", result)
		self.assertIn("<button type=\"submit\" class='button button-1'>Accept</button>", result)
		self.assertIn("<button type=\"submit\" class='button button-5'>Decline</button>", result)
		result = event(4)
		self.assertIn("<span id='title-main'>Event 4</span>", result)
		self.assertIn("<h2 class='page-title'>Invited</h2>", result)
		self.assertIn("Dale Sue", result)
		self.assertIn("Matt Anderson", result)
		self.assertIn("Jake Brown", result)
		self.assertNotIn("Karen Smith", result)
		self.assertIn("<button class='non-btn add-friends'>+ Add More Friends</button>", result)
		logout_user()
		login_user(User.query.get(3))
		result = event(4)
		self.assertIn("<span id='title-main'>Event 4</span>", result)
		self.assertIn("<h2 class='page-title'>Invited</h2>", result)
		self.assertNotIn("<button class='button button-1' id='edit-event-btn'>Edit</button>", result)
		self.assertIn("<button type=\"submit\" class='button button-1'>Accept</button>", result)
		self.assertIn("<button type=\"submit\" class='button button-5'>Decline</button>", result)
		self.assertIn("<h2 class='page-title'>Invited</h2>", result)
		self.assertIn("Dale Sue", result)
		self.assertIn("Karen Smith", result)
		self.assertIn("Jake Brown", result)
		self.assertNotIn("Matt Anderson", result)
		self.assertIn("<div class='adding-friends-hidden'>", result)
		result = event(1)
		self.assertEqual(result.status_code, 302)

	def test_event_new_page(self):
		login_user(User.query.get(1))
		result = event_new()
		self.assertIn("<h1 id='event-title' class='page-title-large'>New Event</h1>", result)
		self.assertIn("<form id='create-event-form' action=\"/event/create/\" method=\"post\">", result)

	def test_accept_invitation(self):
		login_user(User.query.get(2))
		self.assertFalse(UserEvent.query.get(2).accepted)
		self.assertIsNotNone(Notification.query.get(1))
		self.assertIsNotNone(EventInvitation.query.get(1))
		self.assertIsNone(ntfn_exists(1, 1, NotificationType.invite_accepted))
		response = accept_invitation(2)
		data = loads(response.get_data())
		self.assertEqual(data[0], "Invitation accepted.")
		self.assertTrue(UserEvent.query.get(2).accepted)
		self.assertIsNone(Notification.query.get(1))
		self.assertIsNone(EventInvitation.query.get(1))
		self.assertIsNotNone(ntfn_exists(1, 1, NotificationType.invite_accepted))

	def test_decline_invitation(self):
		login_user(User.query.get(1))
		self.assertIsNotNone(UserEvent.query.get(4))
		self.assertFalse(UserEvent.query.get(4).accepted)
		self.assertIsNotNone(Notification.query.get(2))
		self.assertIsNotNone(EventInvitation.query.get(2))
		self.assertIsNone(ntfn_exists(2, 2, NotificationType.invite_declined))
		result = decline_invitation(4)
		self.assertEqual(result.status_code, 302)
		self.assertIsNone(UserEvent.query.get(4))
		self.assertIsNone(Notification.query.get(2))
		self.assertIsNone(EventInvitation.query.get(2))
		self.assertIsNotNone(ntfn_exists(2, 2, NotificationType.invite_declined))

	def test_remove_event(self):
		login_user(User.query.get(1))
		self.assertIsNotNone(UserEvent.query.get(8))
		self.assertIsNone(ntfn_exists(4, 2, NotificationType.event_removed))
		self.assertIsNone(ntfn_exists(4, 3, NotificationType.event_removed))
		self.assertIsNone(ntfn_exists(4, 4, NotificationType.event_removed))
		result = remove_event(8)
		self.assertEqual(result.status_code, 302)
		self.assertIsNone(UserEvent.query.get(8))
		self.assertIsNotNone(ntfn_exists(4, 2, NotificationType.event_removed))
		self.assertIsNotNone(ntfn_exists(4, 3, NotificationType.event_removed))
		self.assertIsNotNone(ntfn_exists(4, 4, NotificationType.event_removed))

	def test_add_invite_single(self):
		login_user(User.query.get(1))
		self.assertIsNone(UserEvent.query.filter_by(event_id=1, user_id=3).first())
		self.assertIsNone(EventInvitation.query.filter_by(sender_id=1, receiver_id=3, event_id=1).first())
		self.assertIsNone(ntfn_exists(1, 3, NotificationType.event_invite))
		response = add_invite_single(1, 3)
		data = loads(response.get_data())
		self.assertEqual(data["id"], 3)
		self.assertIsNotNone(UserEvent.query.filter_by(event_id=1, user_id=3).first())
		self.assertIsNotNone(EventInvitation.query.filter_by(sender_id=1, receiver_id=3, event_id=1).first())
		self.assertIsNotNone(ntfn_exists(1, 3, NotificationType.event_invite))


if __name__ == '__main__':
	unittest.main()
