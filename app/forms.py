from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo, Length
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
	submit = SubmitField('Register')

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

class EditProfileForm(FlaskForm):
	username  = StringField('Username', validators=[DataRequired()])
	# left col
	skills    = TextAreaField('Skill Level', validators=[Length(min=0, max=140)])
	location  = TextAreaField('Location', validators=[Length(min=0, max=140)])
	work      = TextAreaField('Work', validators=[Length(min=0, max=140)])
	interests = TextAreaField('Interests', validators=[Length(min=0, max=140)])

	# right col
	about     = TextAreaField('About', validators=[Length(min=0, max=140)])
	meet      = TextAreaField('Looking to Meet', validators=[Length(min=0, max=140)])

	submit    = SubmitField('Submit')
