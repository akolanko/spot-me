import sys
import os.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir, 'app')))
import unittest
from main import app
from app.models import *
from sample_db import example_data
from app.accounts import *
from connect import connect_to_db
from app import db
import datetime
from app.routes import account, delete_account, update_psw
from flask_login import login_user
from app.forms import UpdatePasswordForm


class FlaskTestAccounts(unittest.TestCase):

	def setUp(self):
		"""Do before every test"""

		# Get the Flask test client
		self.client = app.test_client()
		app.config['TESTING'] = True
		app.config['WTF_CSRF_ENABLED'] = False
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

	"""Test account functions"""

	def test_validate_account(self):
		user = User.query.get(1)
		found_err, username_err, email_err = validate_account(user, "karen", "karen@example.com")
		self.assertFalse(found_err)
		found_err, username_err, email_err = validate_account(user, "lily", "karen@example.com")
		self.assertFalse(found_err)
		found_err, username_err, email_err = validate_account(user, "karen", "lily@example.com")
		self.assertFalse(found_err)
		found_err, username_err, email_err = validate_account(user, "lily", "lily@example.com")
		self.assertFalse(found_err)
		found_err, username_err, email_err = validate_account(user, "dale", "lily@example.com")
		self.assertTrue(found_err)
		self.assertEqual(username_err, 'Please use a different username.')
		self.assertEqual(email_err, '')
		found_err, username_err, email_err = validate_account(user, "karen", "dale@example.com")
		self.assertTrue(found_err)
		self.assertEqual(username_err, '')
		self.assertEqual(email_err, 'Please use a different email address.')
		found_err, username_err, email_err = validate_account(user, "lisa", "dale@example.com")
		self.assertTrue(found_err)
		self.assertEqual(username_err, 'Please use a different username.')
		self.assertEqual(email_err, 'Please use a different email address.')

	def test_calculate_age(self):
		born = datetime.date(1990, 1, 1)
		age = calculate_age(born)
		self.assertEqual(age, 28)
		born = datetime.date(1990, 10, 1)
		age = calculate_age(born)
		self.assertEqual(age, 27)

	def test_update_psw(self):
		user = User.query.get(1)
		check = user.check_password("karen")
		self.assertTrue(check)
		pswform = UpdatePasswordForm(password="pass", password_repeat="pass")
		update_psw(pswform, user)
		check = user.check_password("pass")
		self.assertTrue(check)


	"""Test account routes"""

	def test_account_page(self):
		login_user(User.query.get(1))
		result = account()
		self.assertIn('<div class=\'block account\'>', result)
		self.assertIn('<span id=\'username-main\'>karen</span>', result)

	def test_delete_account(self):
		login_user(User.query.get(1))
		self.assertIsNotNone(User.query.get(1))
		result = delete_account()
		self.assertEqual(result.status_code, 302)
		self.assertIsNone(User.query.get(1))


if __name__ == '__main__':
	unittest.main()
