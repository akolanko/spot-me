import sys
import os.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir, 'app')))
import unittest
from main import app
from app.models import *
from sample_db import example_data
from connect import connect_to_db
from flask_login import login_user
from app.routes import cal


class FlaskTestCalendar(unittest.TestCase):

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

	def test_calendar_page(self):
		login_user(User.query.get(1))
		result1 = cal(2018,5)
		self.assertIn("May ",result1)
		self.assertIn("2018",result1)
		self.assertIn("<div class='add-event-btn add-btn'>", result1)
		

	def test_prev_next_month(self):
		year = 2018
		month = 4
		self.assertEqual((year - 1 if month == 1 else year), 2018)
		self.assertEqual((12 if month == 1 else month - 1), 3)
		month = 1 
		self.assertEqual((year - 1 if month == 1 else year), 2017)
		self.assertEqual((12 if month == 1 else month - 1), 12)
		month = 4
		self.assertEqual((year + 1 if month == 12 else year), 2018)
		self.assertEqual((1 if month == 12 else month + 1), 5)
		month = 12 
		self.assertEqual((year + 1 if month == 12 else year), 2019)
		self.assertEqual((1 if month == 12 else month - 1), 1)


if __name__ =='__main__':
	unittest.main()
