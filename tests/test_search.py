import sys
import os.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir, 'app')))
import unittest
from main import app
from app.models import *
from sample_db import example_data
from connect import connect_to_db
from json import loads
from app.search import search_user


class FlaskTestSearch(unittest.TestCase):

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

	"""Test search function"""

	def test_search_user(self):
		response = search_user("Karen", 1)
		data = loads(response.get_data())
		self.assertEqual(len(data), 0)
		response = search_user("Karen Smith", 1)
		data = loads(response.get_data())
		self.assertEqual(len(data), 0)
		response = search_user("Abc", 1)
		data = loads(response.get_data())
		self.assertEqual(len(data), 0)
		response = search_user("Dale", 1)
		data = loads(response.get_data())
		self.assertEqual(len(data), 1)
		self.assertEqual(data[0]["fname"], "Dale")
		response = search_user("Dale Sue", 1)
		data = loads(response.get_data())
		self.assertEqual(len(data), 1)
		self.assertEqual(data[0]["fname"], "Dale")
		self.assertEqual(data[0]["lname"], "Sue")
		response = search_user("Dan", 1)
		data = loads(response.get_data())
		self.assertEqual(len(data), 3)
		self.assertEqual(data[0]["fname"], "Dan")
		self.assertEqual(data[0]["lname"], "Kay")
		self.assertEqual(data[1]["fname"], "Dan")
		self.assertEqual(data[1]["lname"], "Smith")
		self.assertEqual(data[2]["fname"], "Dan")
		self.assertEqual(data[2]["lname"], "Allen")
		response = search_user("Dan", 7)
		data = loads(response.get_data())
		self.assertEqual(len(data), 2)
		self.assertEqual(data[0]["fname"], "Dan")
		self.assertEqual(data[0]["lname"], "Smith")
		self.assertEqual(data[1]["fname"], "Dan")
		self.assertEqual(data[1]["lname"], "Allen")


if __name__ == '__main__':
	unittest.main()
