import logging
import os
import MySQLdb

from google.appengine.ext import vendor
vendor.add('lib')

from flask import Flask, render_template, request

app = Flask(__name__)

# These environment variables are configured in app.yaml.
CLOUDSQL_CONNECTION_NAME = os.environ.get('CLOUDSQL_CONNECTION_NAME')
CLOUDSQL_USER = os.environ.get('CLOUDSQL_USER')
CLOUDSQL_PASSWORD = os.environ.get('CLOUDSQL_PASSWORD')


def connect_to_cloudsql():
    # When deployed to App Engine, the `SERVER_SOFTWARE` environment variable
    # will be set to 'Google App Engine/version'.
    if os.getenv('SERVER_SOFTWARE', '').startswith('Google App Engine/'):
        # Connect using the unix socket located at
        # /cloudsql/cloudsql-connection-name.
        cloudsql_unix_socket = os.path.join(
            '/cloudsql', CLOUDSQL_CONNECTION_NAME)

        db = MySQLdb.connect(
            unix_socket=cloudsql_unix_socket,
            user=CLOUDSQL_USER,
            passwd=CLOUDSQL_PASSWORD)

    # If the unix socket is unavailable, then try to connect using TCP. This
    # will work if you're running a local MySQL server or using the Cloud SQL
    # proxy, for example:
    #
    #   $ cloud_sql_proxy -instances=your-connection-name=tcp:3306
    #
    else:
        db = MySQLdb.connect(
            host='127.0.0.1', user=CLOUDSQL_USER, passwd=CLOUDSQL_PASSWORD)

    return db

# dynamodb = boto3.resource(
#     'dynamodb',
#     endpoint_url='http://localhost:8000',
#     region_name='dummy_region',
#     aws_access_key_id='dummy_access_key',
#     aws_secret_access_key='dummy_secret_key',
#     verify=False)



@app.route('/')

def index():
<<<<<<< HEAD
    return "Hello, World! We're SPOT ME."


# Code copied from: https://github.com/GoogleCloudPlatform/python-docs-samples

def get(self):
   # """Simple request handler that shows all of the MySQL variables."""
    self.response.headers['Content-Type'] = 'text/plain'

    db = connect_to_cloudsql()
    cursor = db.cursor()
    cursor.execute('SHOW VARIABLES')

    for r in cursor.fetchall():
        self.response.write('{}\n'.format(r))


@app.errorhandler(500)
def server_error(e):
    logging.exception('An error occurred during a request.')
    return """
    An internal error occurred: <pre>{}</pre>
    See logs for full stacktrace.
    """.format(e), 500
=======
    return "Hello, World! We're SpotMe!"
>>>>>>> 7744e3a1dc3ca34ef23a7f296bd849f0917fac09

if __name__ == '__main__':
     app.run()
