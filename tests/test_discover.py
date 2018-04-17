import sys
import os.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir, 'app')))
import unittest
from main import app
from app.models import *
from sample_db import example_data
from app.discover import *
from app import connect_to_db


def convert_list(list):
	id_list = []
	for interest in list:
		id_list.append(interest.id)
	return id_list


def convert_tuple_list(list):
	id_list = []
	for (user, interests) in list:
		id_list.append((user.id, convert_list(interests)))
	return id_list


class FlaskTestDatabase(unittest.TestCase):

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

	"""Test discover functions"""

	def test_discover_friends(self):
		users_interests = discover_friends(1)
		self.assertEqual(convert_tuple_list(users_interests), [(3, [1, 2]), (4, [3]), (5, [1]), (6, [1]), (7, [3])])
		users_interests = discover_friends(2)
		self.assertEqual(convert_tuple_list(users_interests), [(3, [1]), (5, [1]), (6, [1])])
		users_interests = discover_friends(10)
		self.assertEqual(users_interests, [])
		users_interests = discover_friends(15)
		self.assertEqual(convert_tuple_list(users_interests), [(7, [5]), (8, [5, 6])])
		users_interests = discover_friends(3)
		self.assertEqual(convert_tuple_list(users_interests), [(1, [1, 2]), (2, [1]), (5, [1]), (6, [1])])

	def test_search_interests(self):
		users = search_interests("running", 1)
		self.assertEqual(convert_list(users), [3, 5, 6])
		users = search_interests("abc", 1)
		self.assertEqual(users, [])
		users = search_interests("hiking", 3)
		self.assertEqual(users, [])
		users = search_interests("tennis", 3)
		self.assertEqual(convert_list(users), [1])
		users = search_interests("soccer", 15)
		self.assertEqual(convert_list(users), [7, 8])
		users = search_interests("squash", 15)
		self.assertEqual(convert_list(users), [8])
		users = search_interests("tennis", 15)
		self.assertEqual(convert_list(users), [1, 3])
		users = search_interests("soccer", 10)
		self.assertEqual(convert_list(users), [15, 16, 12, 7, 8])
		users = search_interests("lifting", 10)
		self.assertEqual(users, [])

	def test_get_interests(self):
		interests = get_interests(1)
		self.assertEqual(convert_list(interests), [1, 2, 3])
		interests = get_interests(4)
		self.assertEqual(convert_list(interests), [3])
		interests = get_interests(10)
		self.assertEqual(interests, [])


if __name__ == '__main__':
	unittest.main()
