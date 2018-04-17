import sys
import os.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir, 'app')))
import unittest
from main import app
from app.models import *
from sample_db import example_data
from app.notifications import *
from app import connect_to_db


def convert_list(list):
	id_list = []
	for item in list:
		id_list.append(item.id)
	return id_list


class FlaskTestNotifications(unittest.TestCase):

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


	"""Test notification functions"""

	def test_all_notifications(self):
		ntfs_count, notifications = all_notifications(2)
		self.assertEqual(ntfs_count, 3)
		self.assertEqual(convert_list(notifications), [4, 3, 1])
		ntfs_count, notifications = all_notifications(1)
		self.assertEqual(ntfs_count, 1)
		self.assertEqual(convert_list(notifications), [2])
		ntfs_count, notifications = all_notifications(10)
		self.assertEqual(ntfs_count, 0)
		self.assertEqual(notifications, [])

	def test_get_notification(self):
		notification = get_notification(1)
		self.assertEqual(notification.id, 1)
		notification = get_notification(20)
		self.assertIsNone(notification)

	def test_get_notifications(self):
		data = get_notifications(1)
		self.assertEqual(data['received_friend_requests'], [])
		self.assertEqual(data['sent_friend_requests'], [])
		self.assertIsNone(data['pending_received'])
		self.assertIsNone(data['pending_sent'])
		self.assertEqual(data['total_pending_received'], 0)
		self.assertEqual(data['recent_conversation'], 1)
		self.assertEqual(data['unread_msgs_count'], 2)
		self.assertEqual(data['ntfs_count'], 1)
		self.assertEqual(convert_list(data['notifications']), [2])
		data = get_notifications(2)
		self.assertEqual(data['recent_conversation'], 1)
		self.assertEqual(data['ntfs_count'], 3)
		self.assertEqual(convert_list(data['notifications']), [4, 3, 1])
		data = get_notifications(8)
		self.assertEqual(data['received_friend_requests'], [])
		self.assertEqual(data['sent_friend_requests'], [])
		self.assertIsNone(data['pending_received'])
		self.assertIsNone(data['pending_sent'])
		self.assertEqual(data['total_pending_received'], 0)
		self.assertEqual(data['recent_conversation'], 5)
		self.assertEqual(data['unread_msgs_count'], 4)
		self.assertEqual(data['ntfs_count'], 0)
		self.assertEqual(convert_list(data['notifications']), [])
		data = get_notifications(15)
		self.assertEqual(convert_list(data['received_friend_requests']), [14, 16])
		self.assertEqual(convert_list(data['sent_friend_requests']), [12, 13])
		self.assertIsNotNone(data['pending_received'])
		self.assertIsNotNone(data['pending_sent'])
		self.assertEqual(data['total_pending_received'], 2)

	def test_notification_exists(self):
		notification = notification_exists(2, 1)
		self.assertEqual(notification.id, 1)
		notification = notification_exists(2, 2)
		self.assertIsNone(notification)
		notification = notification_exists(8, 3)
		self.assertIsNone(notification)

	def test_remove_notification(self):
		notification = notification_exists(2, 3)
		self.assertEqual(notification.id, 3)
		remove_notification(2, 3)
		self.assertIsNone(notification_exists(2, 3))
		self.assertIsNone(notification_exists(8, 3))
		remove_notification(8, 3)
		self.assertIsNone(notification_exists(8, 3))

	def test_create_invite_notification(self):
		sender = User.query.get(1)
		notification_exists = db.session.query(Notification).filter(Notification.event_id == 4, Notification.receiver_id == 3, Notification.type == NotificationType.event_invite).first()
		self.assertIsNone(notification_exists)
		create_invite_notification(4, sender, 3)
		notification_exists = db.session.query(Notification).filter(Notification.event_id == 4, Notification.receiver_id == 3, Notification.type == NotificationType.event_invite).first()
		self.assertIsNotNone(notification_exists)

	def test_create_update_notification(self):
		sender = User.query.get(1)
		event = Event.query.get(4)
		notification_exists = db.session.query(Notification).filter(Notification.event_id == event.id, Notification.receiver_id == 3, Notification.type == NotificationType.event_update).first()
		self.assertIsNone(notification_exists)
		create_update_notification(event, sender, 3)
		notification_exists = db.session.query(Notification).filter(Notification.event_id == event.id, Notification.receiver_id == 3, Notification.type == NotificationType.event_update).first()
		self.assertIsNotNone(notification_exists)

	def test_create_decline_notification(self):
		user_event = UserEvent.query.get(10)
		notification_exists = db.session.query(Notification).filter(Notification.event_id == user_event.event.id, Notification.receiver_id == 1, Notification.type == NotificationType.invite_declined).first()
		self.assertIsNone(notification_exists)
		create_decline_notification(user_event, 1)
		notification_exists = db.session.query(Notification).filter(Notification.event_id == user_event.event.id, Notification.receiver_id == 1, Notification.type == NotificationType.invite_declined).first()
		self.assertIsNotNone(notification_exists)

	def test_create_accept_notification(self):
		user_event = UserEvent.query.get(10)
		notification_exists = db.session.query(Notification).filter(Notification.event_id == user_event.event.id, Notification.receiver_id == 1, Notification.type == NotificationType.invite_declined).first()
		self.assertIsNone(notification_exists)
		create_accept_notification(user_event, 1)
		notification_exists = db.session.query(Notification).filter(Notification.event_id == user_event.event.id, Notification.receiver_id == 1, Notification.type == NotificationType.invite_accepted).first()
		self.assertIsNotNone(notification_exists)

	def test_create_remove_event_notification(self):
		user_event = UserEvent.query.get(11)
		notification_exists = db.session.query(Notification).filter(Notification.event_id == user_event.event.id, Notification.receiver_id == 1, Notification.type == NotificationType.event_removed).first()
		self.assertIsNone(notification_exists)
		create_remove_event_notification(user_event, 1)
		notification_exists = db.session.query(Notification).filter(Notification.event_id == user_event.event.id, Notification.receiver_id == 1, Notification.type == NotificationType.event_removed).first()
		self.assertIsNotNone(notification_exists)


if __name__ == '__main__':
	unittest.main()
