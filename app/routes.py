import logging
from flask import render_template, flash, redirect, url_for, session
from app import app
from app.forms import LoginForm
from flask_login import current_user, login_user
from app.models import User, Profile, Friends, FriendStatus
from flask_login import logout_user
from flask_login import login_required
from flask import request
from werkzeug.urls import url_parse
from app import db
from app.forms import RegistrationForm
from friends import are_friends_or_pending, get_friend_requests, get_friends


@app.route('/home')
def home():
    return render_template('home.html', title='Home')


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
        session["current_user"] = {
            "username": user.username,
            "id": user.id
        }
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)


@app.route('/logout')
def logout():
    del session["current_user"]
    logout_user()
    return redirect(url_for('login'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data, fname=form.fname.data, lname=form.lname.data)
        user.set_password(form.password.data)
        db.session.add(user)
        profile = Profile()
        db.session.add(profile)
        user.profile = profile
        db.session.commit()
        session["current_user"] = {
            "username": user.username,
            "id": user.id
        }
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('home'))
    return render_template('register.html', title='Register', form=form)


@app.route('/user/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    profile = user.profile

    total_friends = len(get_friends(user.id))
    user_id_1 = session["current_user"]["id"]
    user_id_2 = user.id

    # Check connection status between user_id_1 and user_id_2
    are_friends, is_pending = are_friends_or_pending(user_id_1, user_id_2)

    return render_template('user.html', user=user, profile=profile, total_friends=total_friends, friends=are_friends, pending_request=is_pending)


@app.route("/add_friend", methods=["POST"])
def add_friend():
    """Send a friend request to another user."""
    user_id_1 = session["current_user"]["id"]
    # user_id_2 = request.form.get("user_id_2")
    user_id_2 = request.form["user_id"]

    # Check connection status between user_id_1 and user_id_2
    are_friends, is_pending = are_friends_or_pending(user_id_1, user_id_2)

    if user_id_1 == user_id_2:
        return "You cannot add yourself as a friend."
    elif are_friends:
        return "You are already friends."
    elif is_pending:
        return "Your friend request is pending."
    else:
        friend_request = Friends(user_id_1=user_id_1, user_id_2=user_id_2, status=FriendStatus.requested)
        db.session.add(friend_request)
        db.session.commit()
        print "User ID %s has sent a friend request to User ID %s" % (user_id_1, user_id_2)
        return "Request Sent"


@app.route("/friends")
def friends():
    """Show all friends"""
    friends = get_friends(session["current_user"]["id"]).all()
    return render_template("friends.html", friends=friends)


@app.route("/friend_requests")
def friend_requests():
    """Show friend requests"""
    received_friend_requests, sent_friend_requests = get_friend_requests(session["current_user"]["id"])
    return render_template("friend_requests.html", received_friend_requests=received_friend_requests, sent_friend_requests=sent_friend_requests)


@app.errorhandler(500)
def server_error(e):
    logging.exception('An error occurred during a request.')
    return """
    An internal error occurred: <pre>{}</pre>
    See logs for full stacktrace.
    """.format(e), 500
