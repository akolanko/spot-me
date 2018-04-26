from app.models import *
from datetime import date


def validate_account(cur_user, form_username, form_email):
	username_err = ''
	email_err = ''
	found_err = False
	user = User.query.filter_by(username=form_username).first()
	if user is not None and user.id != cur_user.id:
		username_err = 'Please use a different username.'
		found_err = True
	user = User.query.filter_by(email=form_email).first()
	if user is not None and user.id != cur_user.id:
		email_err = 'Please use a different email address.'
		found_err = True
	return found_err, username_err, email_err


def calculate_age(born):
	today = date.today()
	return today.year - born.year - ((today.month, today.day) < (born.month, born.day))


def update_psw(pswform, current_user):
	current_user.set_password(pswform.password.data)
	db.session.add(current_user)
	db.session.commit()
