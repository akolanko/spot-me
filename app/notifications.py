from friends import get_friend_requests, have_pending_requests


def get_notifications(user_id):
	received_friend_requests, sent_friend_requests = get_friend_requests(user_id)
	pending_recieved, pending_sent = have_pending_requests(user_id)
	total_pending_recieved = len(received_friend_requests)
	return {'received_friend_requests': received_friend_requests, 'sent_friend_requests': sent_friend_requests, 'pending_recieved': pending_recieved, 'pending_sent': pending_sent, 'total_pending_recieved': total_pending_recieved}
