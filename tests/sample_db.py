from app.models import *


def example_data():
    karen = User(username='karen', email='karen@example.com', fname='Karen', lname='Smith')
    karen.set_password('karen')
    dale = User(username='dale', email='dale@example.com', fname='Dale', lname='Sue')
    dale.set_password('dale')
    matt = User(username='matt', email='matt@example.com', fname='Matt', lname='Anderson')
    matt.set_password('matt')
    jake = User(username='jake', email='jake@example.com', fname='Jake', lname='Brown')
    jake.set_password('jake')

    friendship1 = Friends(user_id_1=1, user_id_2=2, status=FriendStatus.accepted)
    friendship2 = Friends(user_id_1=3, user_id_2=4, status=FriendStatus.requested)

    conversation1 = Conversation(user_id_1=1, user_id_2=2)
    conversation2 = Conversation(user_id_1=4, user_id_2=1)
    message1 = Message(sender=1, conversation_id=1, body='hello', read=True)
    message2 = Message(sender=2, conversation_id=1, body='hey')
    message3 = Message(sender=2, conversation_id=1, body='how are you?')

    db.session.add_all([karen, dale, matt, friendship1, friendship2, conversation1, conversation2, message1, message2, message3])
    db.session.commit()
