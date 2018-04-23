from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField, SelectField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo, Length
from app.models import *
from wtforms.fields.html5 import DateField
from wtforms_components import TimeField


class LoginForm(FlaskForm):
	username = StringField('Username', validators=[DataRequired()])
	password = PasswordField('Password', validators=[DataRequired()])
	remember_me = BooleanField('Remember Me')
	submit = SubmitField('Sign In')


class RegistrationForm(FlaskForm):
	username = StringField('Username', validators=[DataRequired()])
	email = StringField('Email', validators=[DataRequired(), Email()])
	password = PasswordField('Password', validators=[DataRequired()])
	password_repeat = PasswordField(
		'Repeat Password', validators=[DataRequired(), EqualTo('password')])
	fname = StringField('First Name', validators=[DataRequired()])
	lname = StringField('Last Name', validators=[DataRequired()])
	birthday = DateField('Birthday', format='%Y-%m-%d', validators=[DataRequired()], render_kw={"placeholder": "yyyy-mm-dd"})
	submit = SubmitField('Register')

	def validate_username(self, username):
		user = User.query.filter_by(username=username.data).first()
		if user is not None:
			raise ValidationError('Please use a different username.')

	def validate_email(self, email):
		user = User.query.filter_by(email=email.data).first()
		if user is not None:
			raise ValidationError('Please use a different email address.')


class UpdateAccountForm(FlaskForm):
	fname = StringField('First Name', validators=[DataRequired()])
	lname = StringField('Last Name', validators=[DataRequired()])
	username = StringField('Username', validators=[DataRequired()])
	email = StringField('Email', validators=[DataRequired(), Email()])
	birthday = DateField('Birthday', validators=[DataRequired()])
	submit = SubmitField('Update')


class UpdatePasswordForm(FlaskForm):
	password = PasswordField('Password', validators=[DataRequired()])
	password_repeat = PasswordField(
		'Repeat Password', validators=[DataRequired(), EqualTo('password')])
	submit = SubmitField('Update')


class NewEventForm(FlaskForm):
	title = StringField('Title', validators=[DataRequired()])
	date = DateField('Date', format='%Y-%m-%d', validators=[DataRequired()], render_kw={"placeholder": "yyyy-mm-dd"})
	start_time = TimeField('Start Time', validators=[DataRequired()], render_kw={"placeholder": "hh:mm"})
	end_time = TimeField('End Time', validators=[DataRequired()], render_kw={"placeholder": "hh:mm"})
	location = StringField('Location')
	notes = TextAreaField('Notes', validators=[Length(min=0, max=140)])
	submit = SubmitField('Send')


class UpdateEventForm(FlaskForm):
	title = StringField('Title', validators=[DataRequired()])
	date = DateField('Date', format='%Y-%m-%d', validators=[DataRequired()])
	start_time = TimeField('Start Time', validators=[DataRequired()])
	end_time = TimeField('End Time', validators=[DataRequired()])
	location = StringField('Location')
	notes = TextAreaField('Notes', validators=[Length(min=0, max=140)])
	submit = SubmitField('Send')


class EditProfileForm(FlaskForm):
	username  = StringField('Username', validators=[DataRequired()])
	# left col
	skills    = SelectField('Skill Level', choices=[(1, 'Beginner'),
	(2, 'Intermediate'), (3, 'Advanced')])
	location  = StringField('Location', validators=[Length(min=0, max=40)])
	work      = StringField('Work', validators=[Length(min=0, max=30)])
	interests = TextAreaField('Interests', validators=[Length(min=0, max=100)])
	# right col
	about     = TextAreaField('About', validators=[Length(min=0, max=140)])
	meet      = TextAreaField('Looking to Meet', validators=[Length(min=0, max=100)])
	submit    = SubmitField('Update')


class AddFriendForm(FlaskForm):
	name = StringField('Name', validators=[DataRequired()])
	submit = SubmitField('Submit')
