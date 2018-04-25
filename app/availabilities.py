from app.models import *
from sqlalchemy import asc


def get_availabilities(user_id):
	sunday = db.session.query(Availability).join(User, Availability.user_id == User.id).filter(Availability.weekday == 1, User.id == user_id).order_by(asc(Availability.start_time)).all()
	monday = db.session.query(Availability).join(User, Availability.user_id == User.id).filter(Availability.weekday == 2, User.id == user_id).order_by(asc(Availability.start_time)).all()
	tuesday = db.session.query(Availability).join(User, Availability.user_id == User.id).filter(Availability.weekday == 3, User.id == user_id).order_by(asc(Availability.start_time)).all()
	wednesday = db.session.query(Availability).join(User, Availability.user_id == User.id).filter(Availability.weekday == 4, User.id == user_id).order_by(asc(Availability.start_time)).all()
	thursday = db.session.query(Availability).join(User, Availability.user_id == User.id).filter(Availability.weekday == 5, User.id == user_id).order_by(asc(Availability.start_time)).all()
	friday = db.session.query(Availability).join(User, Availability.user_id == User.id).filter(Availability.weekday == 6, User.id == user_id).order_by(asc(Availability.start_time)).all()
	saturday = db.session.query(Availability).join(User, Availability.user_id == User.id).filter(Availability.weekday == 7, User.id == user_id).order_by(asc(Availability.start_time)).all()
	weekdays = [(1, "Sunday", sunday), (2, "Monday", monday), (3, "Tuesday", tuesday), (4, "Wednesday", wednesday), (5, "Thursday", thursday), (6, "Friday", friday), (7, "Saturday", saturday)]
	return weekdays


def add_availability(user_id, form):
	availability = Availability(user_id=user_id, weekday=form.weekday.data, start_time=form.start_time.data, end_time=form.end_time.data)
	db.session.add(availability)
	db.session.commit()
