import unittest
from app.friends import find_friend
from app.messages import conversation_exists


class MainTest(unittest.TestCase):

	def test_find_friend(self):
		friend_id = find_friend('akolanko')
		self.assertEqual(friend_id, 6)
		friend_id = find_friend('abc')
		self.assertEqual(friend_id, None)

	def test_conversation_exists(self):
		self.assertEqual(conversation_exists(8, 6), 1)
		self.assertEqual(conversation_exists(6, 8), 1)
		self.assertEqual(conversation_exists(8, 10), None)

if __name__ == '__main__':
	unittest.main()
