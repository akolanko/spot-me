import sys
import os.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir, 'app')))
import unittest
import datetime
from main import app
from app.models import *
from app.forms import UpdateAvailabilityForm
from app.availabilities import *
from sample_db import example_data
from connect import connect_to_db
from app.routes import remove_availability
from json import loads
from flask_login import login_user, logout_user

def convert_list(list):
    weekday_list = []
    for item in list:
        weekday_list.append(len(item[2]))
    return weekday_list

class FlaskTestAvailabilities(unittest.TestCase):
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

    def test_add_availability(self):
        user = User.query.get(1)
        weekdays = get_availabilities(user.id)
        self.assertEqual(convert_list(weekdays), [1, 0, 0, 2, 1, 0, 0])
        form = UpdateAvailabilityForm(weekday=1, start_time=datetime.strptime('03:55', '%H:%M').time(), end_time=datetime.strptime('08:55', '%H:%M').time())
        add_availability(user.id, form)
        weekdays = get_availabilities(user.id)
        self.assertEqual(convert_list(weekdays), [2, 0, 0, 2, 1, 0, 0])


    def test_get_availabilities(self):
        user = User.query.get(1)
        weekdays = get_availabilities(user.id)
        self.assertEqual(convert_list(weekdays), [1, 0, 0, 2, 1, 0, 0])
        user = User.query.get(9)
        weekdays = get_availabilities(user.id)
        self.assertEqual(convert_list(weekdays), [0, 0, 0, 0, 0, 0, 0])

    def test_remove_availability(self):
        user = User.query.get(1)
        login_user(user)
        avail = Availability.query.get(1)
        self.assertIsNotNone(avail)
        self.assertEqual(avail.user_id, user.id)
        response = remove_availability(avail.id)
        data = loads(response.get_data())
        self.assertEqual(data["status"], "success")
        avail = Availability.query.get(1)
        self.assertIsNone(avail)
        logout_user()
        user = User.query.get(2)
        login_user(user)
        avail = Availability.query.get(3)
        self.assertIsNotNone(avail)
        self.assertNotEqual(avail.user_id, user.id)
        response = remove_availability(avail.id)
        data = loads(response.get_data())
        self.assertEqual(data["status"], "error")
        avail = Availability.query.get(3)
        self.assertIsNotNone(avail)


if __name__ == '__main__':
	unittest.main()
