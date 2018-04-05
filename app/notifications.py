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


def remove_notification(receiver_id, event_id):
	old_notification = notification_exists(receiver_id, event_id)
	if old_notification is not None:
		db.session.delete(old_notification)
		db.session.commit()


def create_invite_notification(event_id, sender, receiver_id):
	body = "New event invitation from " + sender.fname
	notification = Notification(body=body, receiver_id=receiver_id, event_id=event_id, type=NotificationType.event_invite)
	db.session.add(notification)
	db.session.commit()


def create_decline_notification(user_event, receiver_id):
	body = user_event.user.fname + " declined your invitation to " + user_event.event.title
	notification = Notification(body=body, receiver_id=receiver_id, event_id=user_event.event.id, type=NotificationType.invite_declined)
	db.session.add(notification)
	db.session.commit()


def create_accept_notification(user_event, receiver_id):
	body = user_event.user.fname + " accepted your invitation to " + user_event.event.title
	notification = Notification(body=body, receiver_id=receiver_id, event_id=user_event.event.id, type=NotificationType.invite_accepted)
	db.session.add(notification)
	db.session.commit()


def create_remove_event_notification(user_event, receiver_id):
	body = user_event.user.fname + " is no longer attending " + user_event.event.title
	notification = Notification(body=body, receiver_id=receiver_id, event_id=user_event.event.id, type=NotificationType.event_removed)
	db.session.add(notification)
	db.session.commit()
