from app.models import *


def post_resistration(form):
	user = User(username=(form.username.data).lower(), email=form.email.data, fname=form.fname.data, lname=form.lname.data, birthday=form.birthday.data)
	user.set_password(form.password.data)
	db.session.add(user)
	profile = Profile(user_id=user.id)
	db.session.add(profile)
	user.profile = profile
	db.session.commit()