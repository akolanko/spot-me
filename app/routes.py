import logging
from flask import render_template, flash, redirect, url_for, jsonify
from app import app, db
from app.forms import *
from flask_login import current_user, login_user, logout_user, login_required
from app.models import *
from flask import request
from werkzeug.urls import url_parse
from app.friends import are_friends_or_pending
from app.notifications import *
from app.messages import *
from app.discover import discover_friends, search_interests, get_interests
from sqlalchemy import asc
from app.accounts import validate_account, update_psw
from app.events import *
from app.search import search_user
from app.profile import update_profile, get_profile_data, get_user_data
from app.availabilities import get_availabilities, add_availability
from app.login import post_resistration
from datetime import date
from calendar import Calendar


@app.route('/', methods=['GET', 'POST'])
@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('home')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        post_resistration(form)
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route('/home')
@login_required
def home():
    users_interests = discover_friends(current_user.id)
    notifications = get_notifications(current_user.id)
    coming_up = get_recent_events(current_user.id)
    weekdays = get_availabilities(current_user.id)
    today = datetime.date.today()
    return render_template('home.html', notifications=notifications, coming_up=coming_up, weekdays=weekdays, today=today, users_interests=users_interests)


@app.route('/user/<user_id>')
@login_required
def user(user_id):
    user = User.query.filter_by(id=user_id).first_or_404()
    are_friends, is_pending_sent, is_pending_received, friends, limited_friends, total_friends, notifications, conversation, age = get_user_data(user, current_user)
    profile, weekdays, availform, interests, interests_str, form = get_profile_data(user, current_user)

    if current_user.profile.about is not None:
        form.about.data = current_user.profile.about
    if current_user.profile.meet is not None:
        form.meet.data = current_user.profile.meet
    if current_user.profile.skills is not None:
        form.skills.data = current_user.profile.skills
    form.interests.data = interests_str
    if current_user.profile.location is not None:
        form.location.data = current_user.profile.location
    if current_user.profile.work is not None:
        form.work.data = current_user.profile.work

    return render_template('profile.html', user=user, weekdays=weekdays, availform=availform,  profile=profile, total_friends=total_friends, are_friends=are_friends, is_pending_sent=is_pending_sent, is_pending_received=is_pending_received, friends=friends, notifications=notifications, limited_friends=limited_friends, conversation=conversation, age=age, form=form, interests=interests)


@app.route('/edit_profile', methods=['POST'])
@login_required
def edit_profile():
    user = current_user
    are_friends, is_pending_sent, is_pending_received, friends, limited_friends, total_friends, notifications, conversation, age = get_user_data(user, current_user)
    profile, weekdays, availform, interests, interests_str, form = get_profile_data(user, current_user)
    if form.validate_on_submit():
        update_profile(current_user, form)
        flash('Your changes have been saved.')
        return redirect(url_for('user', user_id=current_user.id))
    return render_template('profile.html', user=user, weekdays=weekdays, availform=availform,  profile=profile, total_friends=total_friends, are_friends=are_friends, is_pending_sent=is_pending_sent, is_pending_received=is_pending_received, friends=friends, notifications=notifications, limited_friends=limited_friends, conversation=conversation, age=age, form=form, interests=interests)


@app.route('/edit_availability', methods=['POST'])
@login_required
def edit_availability():
    user = current_user
    are_friends, is_pending_sent, is_pending_received, friends, limited_friends, total_friends, notifications, conversation, age = get_user_data(user, current_user)
    profile, weekdays, availform, interests, interests_str, form = get_profile_data(user, current_user)

    if availform.validate_on_submit():
        add_availability(current_user.id, availform)
        flash('Your changes have been saved.')
        return redirect(url_for('user', user_id=current_user.id))

    return render_template('profile.html', user=user, weekdays=weekdays, availform=availform,  profile=profile, total_friends=total_friends, are_friends=are_friends, is_pending_sent=is_pending_sent, is_pending_received=is_pending_received, friends=friends, notifications=notifications, limited_friends=limited_friends, conversation=conversation, age=age, form=form, interests=interests)


@app.route('/remove_availability/<availability_id>/', methods=['POST'])
@login_required
def remove_availability(availability_id):
    availability = Availability.query.get(availability_id)
    if availability.user_id == current_user.id:
        db.session.delete(availability)
        db.session.commit()
        return jsonify({"status": "success", "id": availability_id})
    return jsonify({"status": "error"})


@app.route("/friends/<user_id>")
@login_required
def friends(user_id):
    user = User.query.filter_by(id=user_id).first_or_404()
    are_friends, is_pending_sent, is_pending_received, friends, limited_friends, total_friends, notifications, conversation, age = get_user_data(user, current_user)
    return render_template("friends.html", user=user, friends=friends, total_friends=total_friends, are_friends=are_friends, is_pending_sent=is_pending_sent, is_pending_received=is_pending_received, notifications=notifications, limited_friends=limited_friends, conversation=conversation, age=age)


@app.route("/add_friend/<friend_id>/", methods=["POST"])
@login_required
def add_friend(friend_id):
    are_friends, is_pending_sent, is_pending_received = are_friends_or_pending(current_user.id, friend_id)
    if current_user.id == friend_id:
        return "You cannot add yourself as a friend."
    elif are_friends:
        return "You are already friends."
    elif is_pending_sent:
        return "Your friend request is pending."
    elif is_pending_received:
        return "You have already received a request from this user."
    else:
        friend_request = Friends(user_id_1=current_user.id, user_id_2=friend_id, status=FriendStatus.requested)
        db.session.add(friend_request)
        db.session.commit()
        return "Request sent."


@app.route("/accept_friend/<friend_id>/", methods=["POST"])
@login_required
def accept_friend(friend_id):
    are_friends, is_pending_sent, is_pending_received = are_friends_or_pending(current_user.id, friend_id)
    if current_user.id == friend_id:
        return "You cannot add yourself as a friend."
    elif are_friends:
        return "You are already friends."
    elif is_pending_received:
        friend_request = Friends.query.filter_by(user_id_1=friend_id, user_id_2=current_user.id, status=FriendStatus.requested).first()
        friend_request.status = FriendStatus.accepted
        db.session.commit()
        return jsonify({"status": "Request accepted.", "user": current_user.serialize()})
    else:
        return "An error occured."


@app.route("/unfriend/<friend_id>/", methods=["POST"])
@login_required
def unfriend(friend_id):
    are_friends, is_pending_sent, is_pending_received = are_friends_or_pending(current_user.id, friend_id)
    if are_friends:
        relationship = Friends.query.filter_by(user_id_1=current_user.id, user_id_2=friend_id, status=FriendStatus.accepted).first()
        if relationship is None:
            relationship = Friends.query.filter_by(user_id_1=friend_id, user_id_2=current_user.id, status=FriendStatus.accepted).first()
        db.session.delete(relationship)
        db.session.commit()
        return jsonify({"status": "Sucessfully unfriended.", "user": current_user.serialize()})
    else:
        return "You cannot unfriend this user."


@app.route("/delete_friend_request/<friend_id>/", methods=["POST"])
@login_required
def delete_friend_request(friend_id):
    are_friends, is_pending_sent, is_pending_received = are_friends_or_pending(current_user.id, friend_id)
    if is_pending_received:
        relationship = Friends.query.filter_by(user_id_1=friend_id, user_id_2=current_user.id, status=FriendStatus.requested).first()
        db.session.delete(relationship)
        db.session.commit()
        return "Request removed."
    else:
        return "You cannot remove this request."


@app.route("/conversation/<id>", methods=['GET'])
@login_required
def conversation(id):
    conversation = Conversation.query.filter_by(id=id).first_or_404()
    if current_user.id == conversation.user_id_1:
        user_2 = User.query.filter_by(id=conversation.user_id_2).first()
    elif current_user.id == conversation.user_id_2:
        user_2 = User.query.filter_by(id=conversation.user_id_1).first()
    else:
        return redirect(url_for('home'))
    update_read_messages(conversation.id, user_2.id)
    notifications = get_notifications(current_user.id)
    messages = conversation.messages.order_by(asc(Message.timestamp)).all()
    conversations = get_conversations(current_user.id)
    eventform = NewEventForm()
    return render_template("messenger.html", conversation=conversation, user_2=user_2, conversations=conversations, messages=messages, notifications=notifications, eventform=eventform)


@app.route("/new_message/", methods=["POST"])
@login_required
def new_message():
    conversation_id = request.form.get("conversation_id")
    body = request.form.get("body")
    message = Message(sender=current_user.id, conversation_id=conversation_id, body=body)
    db.session.add(message)
    db.session.commit()
    return "Message sent"


@app.route("/new_conversation")
@login_required
def new_conversation():
    eventform = NewEventForm()
    notifications = get_notifications(current_user.id)
    conversations = get_conversations(current_user.id)
    return render_template("new_conversation.html", conversations=conversations, notifications=notifications, eventform=eventform)


@app.route("/create_conversation/<user_id>/", methods=['GET', "POST"])
@login_required
def create_conversation(user_id):
    conversation_id = build_conversation(current_user.id, user_id)
    if conversation_id:
        return redirect(url_for('conversation', id=conversation_id))
    else:
        return "An error occurred."


@app.route("/create_new_conversation/", methods=["POST"])
@login_required
def create_new_conversation():
    name = request.form.get("name")
    return post_conversation(name, current_user)


@app.route("/post_conversation_single/<user_id>/", methods=["POST"])
@login_required
def post_conversation_single(user_id):
    user = User.query.get(user_id)
    return post_single(user, current_user)


@app.route("/discover")
@login_required
def discover():
    notifications = get_notifications(current_user.id)
    users_interests = discover_friends(current_user.id)
    return render_template("discover.html", notifications=notifications, users_interests=users_interests)


@app.route("/search_discover/", methods=["POST"])
def search_discover():
    interest = request.form.get("interest")
    users = search_interests(interest, current_user.id)
    if len(users) == 0:
        return "Your search did not return any results."
    else:
        return jsonify([[u.serialize(), [i.serialize() for i in get_interests(u.id)]] for u in users])


@app.route("/account", methods=['GET'])
@login_required
def account():
    notifications = get_notifications(current_user.id)
    accform = UpdateAccountForm()
    pswform = UpdatePasswordForm()
    return render_template("account.html", notifications=notifications, user=current_user, pswform=pswform, accform=accform)


@app.route("/update_account/", methods=['POST'])
@login_required
def update_account():
    accform = UpdateAccountForm()
    if accform.validate_on_submit():
        current_user.fname = accform.fname.data
        current_user.lname = accform.lname.data

        found_err, username_err, email_err = validate_account(current_user, accform.username.data, accform.email.data)
        if found_err is True:
            return jsonify(["error", accform.errors, {"username": username_err, "email": email_err}])

        current_user.username = accform.username.data
        current_user.email = accform.email.data
        current_user.birthday = accform.birthday.data

        db.session.add(current_user)
        db.session.commit()
        return jsonify(["success", {"fname": accform.fname.data, "lname": accform.lname.data, "username": accform.username.data, "email": accform.email.data, "birthday": accform.birthday.data}])
    return jsonify(["error", accform.errors, False])


@app.route("/update_password/", methods=['POST'])
@login_required
def update_password():
    pswform = UpdatePasswordForm()
    if pswform.validate_on_submit():
        update_psw(pswform, current_user)
        return jsonify("Password updated.")
    return jsonify(pswform.errors)


@app.route("/delete_account/", methods=['POST'])
@login_required
def delete_account():
    db.session.delete(current_user)
    db.session.commit()
    return redirect(url_for('login'))


@app.route("/view_notification/<notification_id>/", methods=['POST'])
@login_required
def view_notification(notification_id):
    notification = get_notification(notification_id)
    db.session.delete(notification)
    db.session.commit()
    return "Notification deleted."


@app.route("/new_event/<user_id>/", methods=["POST"])
def new_event(user_id):
    eventform = NewEventForm()
    if eventform.validate_on_submit():
        event = Event(title=eventform.title.data, date=eventform.date.data, start_time=eventform.start_time.data, end_time=eventform.end_time.data, location=eventform.location.data, notes=eventform.notes.data)
        db.session.add(event)
        create_friend_event(event, current_user, user_id)
        return jsonify("Event Created.")
    return jsonify(eventform.errors)


@app.route("/event/<event_id>")
@login_required
def event(event_id):
    event = Event.query.filter_by(id=event_id).first_or_404()
    user_event = user_event_exists(current_user.id, event.id)
    if user_event is None:
        return redirect(url_for('home'))
    notifications = get_notifications(current_user.id)
    coming_up = get_recent_events(current_user.id)
    length = len(event.user_events)
    sent_invitation, received_invitation = get_event_invitation(event_id, current_user.id)
    friendform = AddFriendForm()
    eventform = UpdateEventForm()
    weekdays = get_availabilities(current_user.id)
    today = datetime.date.today()
    return render_template('event.html', notifications=notifications, event=event, coming_up=coming_up, user_event=user_event, length=length, sent_invitation=sent_invitation, received_invitation=received_invitation, weekdays=weekdays, friendform=friendform, eventform=eventform, today=today)


@app.route("/update_event/<event_id>/", methods=['POST'])
@login_required
def update_event(event_id):
    event = Event.query.filter_by(id=event_id).first()
    eventform = UpdateEventForm()
    if eventform.validate_on_submit():
        post_event_update(eventform, event)
        return jsonify(["success", {"title": eventform.title.data, "date": eventform.date.data, "start_time": str(event.start_time), "end_time": str(event.end_time), "location": eventform.location.data, "notes": eventform.notes.data}])
    return jsonify(["error", eventform.errors])


@app.route("/event/new")
@login_required
def event_new():
    eventform = NewEventForm()
    notifications = get_notifications(current_user.id)
    coming_up = get_recent_events(current_user.id)
    weekdays = get_availabilities(current_user.id)
    return render_template('new_event.html', notifications=notifications, coming_up=coming_up, weekdays=weekdays, eventform=eventform)


@app.route("/event/create/", methods=['POST'])
@login_required
def create_event():
    eventform = NewEventForm()
    if eventform.validate_on_submit():
        event = Event(title=eventform.title.data, date=eventform.date.data, start_time=eventform.start_time.data, end_time=eventform.end_time.data, location=eventform.location.data, notes=eventform.notes.data)
        add_event(event, current_user)
        return jsonify(["success", event.id])
    return jsonify(["error", eventform.errors])


@app.route("/accept_invitation/<user_event_id>/", methods=['POST'])
@login_required
def accept_invitation(user_event_id):
    user_event = UserEvent.query.filter_by(id=user_event_id).first()
    user_event.accepted = True
    db.session.add(user_event)
    sent_invitation, received_invitation = get_event_invitation(user_event.event_id, current_user.id)
    remove_notification(received_invitation.receiver.id, user_event.event.id)
    create_accept_notification(user_event, received_invitation.sender.id)
    db.session.delete(received_invitation)
    db.session.commit()
    return jsonify(["Invitation accepted.", [{"user_event": u_e.serialize(), "user": u_e.user.serialize()} for u_e in user_event.event.user_events]])


@app.route("/decline_invitation/<user_event_id>/", methods=['POST'])
@login_required
def decline_invitation(user_event_id):
    user_event = UserEvent.query.filter_by(id=user_event_id).first()
    sent_invitation, received_invitation = get_event_invitation(user_event.event_id, current_user.id)
    remove_notification(received_invitation.receiver.id, user_event.event.id)
    create_decline_notification(user_event, received_invitation.sender.id)
    db.session.delete(user_event)
    db.session.delete(received_invitation)
    db.session.commit()
    flash('Invitation declined.')
    return redirect(url_for('event_new'))


@app.route("/remove_event/<user_event_id>/", methods=['POST'])
@login_required
def remove_event(user_event_id):
    user_event = UserEvent.query.filter_by(id=user_event_id).first()
    for u_e in user_event.event.user_events:
        if u_e.id != user_event.id:
            create_remove_event_notification(user_event, u_e.user.id)
    db.session.delete(user_event)
    db.session.commit()
    flash('Event removed.')
    return redirect(url_for('event_new'))


@app.route("/add_invite/<event_id>/", methods=['POST'])
@login_required
def add_invite(event_id):
    friendform = AddFriendForm()
    if friendform.validate_on_submit():
        names = friendform.name.data.split(' ')
        if len(names) == 1:
            users = User.query.filter_by(fname=names[0]).all()
        elif len(names) > 1:
            users = User.query.filter_by(fname=names[0], lname=names[1]).all()
        return invite_search(users, event_id, current_user.id)
    return jsonify(["error", friendform.errors])


@app.route("/add_invite_single/<event_id>/<user_id>/", methods=['POST'])
@login_required
def add_invite_single(event_id, user_id):
    create_user_event(user_id, event_id, current_user.id)
    user = User.query.get(user_id)
    return jsonify(user.serialize())


@app.route("/search/", methods=['POST'])
@login_required
def search():
    name = request.form.get("name")
    return search_user(name, current_user.id)


@app.route("/calendar/<int:year>/<int:month>", methods=["GET", "POST"])
@login_required
def cal(year, month):
    notifications = get_notifications(current_user.id)
    cal = Calendar(6)
    if year == 0 and month == 0:
        year = date.today().year
        month = date.today().month
        return redirect(url_for('cal', year=year, month=month))
    weeks = cal.monthdatescalendar(year, month)
    coming_up = db.session.query(Event).join(UserEvent, UserEvent.event_id == Event.id).filter(UserEvent.user_id == current_user.id, UserEvent.accepted == 1).all()
    eventform = NewEventForm()
    return render_template("cal.html", notifications=notifications, user=current_user, year=year, mon=month, weeks=weeks, coming_up=coming_up, eventform=eventform)


@app.route("/calendar/<event_id>/<int:year>/<int:month>", methods=["GET", "POST"])
@login_required
def cal_event(event_id, year, month):
    notifications = get_notifications(current_user.id)
    cal = Calendar(6)
    if year == 0 and month == 0:
        year = date.today().year
        month = date.today().month
        return redirect(url_for('cal_event', year=year, month=month, event_id=event_id))
    weeks = cal.monthdatescalendar(year, month)
    coming_up = db.session.query(Event).join(UserEvent, UserEvent.event_id == Event.id).filter(UserEvent.user_id == current_user.id, UserEvent.accepted == 1).all()
    event = Event.query.get(event_id)
    user_event = UserEvent.query.filter_by(event_id=event_id, user_id=current_user.id).first()
    eventform = eventform = UpdateEventForm()
    friendform = AddFriendForm()
    today = datetime.date.today()
    return render_template("cal_event.html", notifications=notifications, user=current_user, year=year, mon=month, weeks=weeks, coming_up=coming_up, event=event, user_event=user_event, eventform=eventform, friendform=friendform, today=today)


@app.errorhandler(500)
def server_error(e):
    logging.exception('An error occurred during a request.')
    return """
    An internal error occurred: <pre>{}</pre>
    See logs for full stacktrace.
    """.format(e), 500


@app.errorhandler(404)
def page_not_found(e):
    if current_user.is_authenticated:
        notifications = get_notifications(current_user.id)
        return render_template('404.html', notifications=notifications), 404
    return render_template('404.html'), 404
