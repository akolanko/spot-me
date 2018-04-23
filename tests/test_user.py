import sys
import os.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir, 'app')))
import unittest
from main import app
from app.models import *
from sample_db import example_data
from connect import connect_to_db
from app.routes import user, friends
from flask_login import login_user, logout_user


class FlaskTestUser(unittest.TestCase):

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

	"""Test user page"""

	def test_user_page(self):
		login_user(User.query.get(1))
		result = user(1)
		self.assertIn('Karen Smith', result)
		self.assertIn("<div class='block profile-basic'>", result)
		self.assertNotIn("<button class='button button-2'>Message</button>", result)
		result = user(2)
		self.assertIn('Dale Sue', result)
		self.assertIn('<a href="/conversation/1">', result)
		self.assertIn('<button class="button button-2">Message</button>', result)
		self.assertIn("<button class='button button-2 disabled'>Friends</button>", result)
		result = user(6)
		self.assertIn('Katie Wolf', result)
		self.assertIn('<a href="/create_conversation/6/">', result)
		self.assertIn('<button class="button button-2">Message</button>', result)
		self.assertIn('<button type="submit" class=\'button button-2\'>Connect</button>', result)
		logout_user()
		login_user(User.query.get(5))
		result = user(6)
		self.assertIn('Katie Wolf', result)
		self.assertIn("<button class='button button-2 disabled'>Pending</button>", result)

	def test_friends_page(self):
		login_user(User.query.get(1))
		result = friends(1)
		self.assertIn('Karen Smith', result)
		self.assertIn("<h2 class='block-title'>Connections</h2>", result)
		self.assertIn("<button type=\"submit\" class='button button-3' id=\"unfriend-btn\">Unfriend</button>", result)
		result = friends(2)
		self.assertIn('Dale Sue', result)
		self.assertNotIn("<button type=\"submit\" class='button button-3' id=\"unfriend-btn\">Unfriend</button>", result)


if __name__ == '__main__':
	unittest.main()
