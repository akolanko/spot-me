from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, DateTimeField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo
from app.models import User


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
	birthday = DateTimeField('Birthday', validators=[DataRequired()])
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
	birthday = DateTimeField('Birthday', validators=[DataRequired()])
	submit = SubmitField('Update')

	def validate_username(self, username):
		user = User.query.filter_by(username=username.data).first()
		if user is not None:
			raise ValidationError('Please use a different username.')

	def validate_email(self, email):
		user = User.query.filter_by(email=email.data).first()
		if user is not None:
			raise ValidationError('Please use a different email address.')


class UpdatePasswordForm(FlaskForm):
	password = PasswordField('Password', validators=[DataRequired()])
	password_repeat = PasswordField(
		'Repeat Password', validators=[DataRequired(), EqualTo('password')])
	submit = SubmitField('Update')
