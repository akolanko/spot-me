import sys
import os.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir, 'app')))
import unittest
from main import app
from app.models import *
from sample_db import example_data
from app.events import *
from app.notifications import notification_exists
from app import connect_to_db
from flask import jsonify


def convert_list(list):
	id_list = []
	for item in list:
		id_list.append(item.id)
	return id_list


class FlaskTestEvents(unittest.TestCase):

	def setUp(self):
		"""Do before every test"""

		# Get the Flask test client
		self.client = app.test_client()
		app.config['TESTING'] = True
		# self.app_context = app.app_context()
		# self.app_context.push()

		# Connect to test database
		connect_to_db(app, 'sqlite:////tmp/test.db')

		# Create tables and add sample data
		db.create_all()
		example_data()

	def tearDown(self):
		"""Do at end of every test"""

		db.session.close()
		db.drop_all()
		# self.app_context.pop()

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

	# def test_check_results(self):
	# 	with app.app_context():
	# 		data = check_results([], 6, 6)
	# 		self.assertEqual(data, "Your search did not return any results.")

if __name__ == '__main__':
	unittest.main()
