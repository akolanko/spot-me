from app.friends import get_friend_requests, have_pending_requests
from app.messages import most_recent_message, unread_messages


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

	return {'received_friend_requests': received_friend_requests, 'sent_friend_requests': sent_friend_requests, 'pending_recieved': pending_recieved, 'pending_sent': pending_sent, 'total_pending_recieved': total_pending_recieved, 'recent_conversation': recent_conversation, 'unread_msgs_count': unread_msgs_count, 'unread_conversations': unread_conversations}
