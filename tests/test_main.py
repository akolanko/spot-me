# Copyright 2015 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
import sys
import os.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir, 'app')))


from main import app
import unittest
from flask_testing import TestCase
from flask import Flask

class MainTest(unittest.TestCase):
    """This class uses the Flask tests app to run an integration test against a
    local instance of the server."""

    # def create_app(self):
    #     app = Flask(__name__)
    #     app.config['TESTING'] = True
    #     return app

    # def test_homepage(self):
    #     self.client.get('/')
    #     self.assert_template_used('index.html')

    def setUp(self):
        self.app = app.test_client()

    def test_homepage(self):
    	rv = self.app.get('/')
        self.assertIn('SPOT ME', rv.data)


if __name__ == '__main__':
    unittest.main()
