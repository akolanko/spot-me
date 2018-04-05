from app.friends import get_friend_requests, have_pending_requests
from app.messages import most_recent_message, unread_messages
from app import db
from app.models import Notification, NotificationType
from sqlalchemy import desc


def all_notifications(user_id):
	notifications = db.session.query(Notification).filter(Notification.receiver_id == user_id).order_by(desc(Notification.created_at)).all()
	ntfs_count = len(notifications)
	return ntfs_count, notifications


def get_notification(notification_id):
	notification = db.session.query(Notification).filter(Notification.id == notification_id).first()
	return notification


def get_notifications(user_id):
	received_friend_requests, sent_friend_requests = get_friend_requests(user_id)
	pending_recieved, pending_sent = have_pending_requests(user_id)
	total_pending_recieved = len(received_friend_requests)

	recent_msg = most_recent_message(user_id)
	if recent_msg is not None:
		recent_conversation = recent_msg.conversation_id
	else:
		recent_conversation = None

	unread_msgs_count, unread_conversations = unread_messages(user_id)
	ntfs_count, notifications = all_notifications(user_id)

	return {'received_friend_requests': received_friend_requests, 'sent_friend_requests': sent_friend_requests, 'pending_recieved': pending_recieved, 'pending_sent': pending_sent, 'total_pending_recieved': total_pending_recieved, 'recent_conversation': recent_conversation, 'unread_msgs_count': unread_msgs_count, 'unread_conversations': unread_conversations, 'ntfs_count': ntfs_count, 'notifications': notifications}


def notification_exists(receiver_id, event_id):
	notifications = db.session.query(Notification).filter(Notification.receiver_id == receiver_id, Notification.event_id == event_id)
	if notifications is not None:
		return notifications.first()
	else:
		return None
