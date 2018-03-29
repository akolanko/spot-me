from app import app, connect_to_db, db
from app.models import *
from seed import example_data


@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'Profile': Profile, 'Friends': Friends, 'FriendStatus': FriendStatus, 'Message': Message, 'Conversation': Conversation, 'Interest': Interest, 'User_Interest': User_Interest}

if __name__ == '__main__':
    # This is used when running locally. Gunicorn is used to run the
    # application on Google App Engine. See entrypoint in app.yaml.

    # connect_to_db(app, 'sqlite:////tmp/tst.db')
    connect_to_db(app)
    db.drop_all()
    db.create_all()
    example_data()

    app.run(host='127.0.0.1', port=8080, debug=True)
