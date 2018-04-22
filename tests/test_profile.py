import sys
import os.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir, 'app')))
import unittest
from main import app
from app.models import *
from sample_db import example_data
from connect import connect_to_db
from app.routes import user, edit_profile
from app.profile import check_and_update_interests, get_user_interests
from flask_login import login_user, logout_user
import datetime

class FlaskTestProfile(unittest.TestCase):
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


    def test_user_profile(self):

        karen = db.session.query(User).get(1)
        k_interests, k_string = get_user_interests(karen)

        # test Karen's interests -- intially running, tennis, and biking
        k_str = "running reading programming hiking"
        check_and_update_interests(k_str , 1)
        k_interests, k_string = get_user_interests(karen)
        self.assertEqual(len(k_interests), 4)

        # create and test a new user
        jess = User(username='jess', email='jess@example.com', fname='Jess', lname='Holmes', birthday=datetime.date(1996, 5, 28))
        jess.set_password('jess')
        db.session.add_all([jess])
        db.session.commit()

        jess = db.session.query(User).filter_by(username="jess").first()

        profile_jess= Profile(user_id=jess.id, about="Journalism student with a passion for all things exciting and new!", location="LA", skills=3)

        # # jess has two interests
        user_interest1 = User_Interest(user_id=jess.id, interest_id=1)
        user_interest2 = User_Interest(user_id=jess.id, interest_id=4)
        db.session.commit()
        db.session.add_all([profile_jess, user_interest1, user_interest2])

        db.session.commit()

        # remove all interests
        jess_str = ""
        j_intersts, j_string = get_user_interests(jess)

        check_and_update_interests(jess_str , jess.id)
        j_intersts, j_string = get_user_interests(jess)

        self.assertEqual(len(j_intersts), 0)

        # insert completely new interests
        jess_str = "kayaking painting origami"
        j_intersts, j_string = get_user_interests(jess)

        check_and_update_interests(jess_str , jess.id)
        j_intersts, j_string = get_user_interests(jess)

        self.assertEqual(len(j_intersts), 3)


if __name__ == '__main__':
	unittest.main()
