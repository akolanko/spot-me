from app.models import User, db
from flask import jsonify


def search_user(name, current_user_id):
	names = name.split(' ')
	users = []
	if len(names) == 1:
		users = db.session.query(User).filter(User.id != current_user_id, User.fname == names[0]).all()
	elif len(names) > 1:
		users = db.session.query(User).filter(User.id != current_user_id, User.fname == names[0], User.lname == names[1]).all()
	return jsonify([u.serialize() for u in users])
