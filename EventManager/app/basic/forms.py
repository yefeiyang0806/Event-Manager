from app import db
from flask.ext.wtf import Form
from wtforms import StringField, BooleanField, PasswordField, IntegerField, DateTimeField, DateField
from wtforms.validators import InputRequired, Length, Email, EqualTo, ValidationError
from werkzeug.security import check_password_hash
from app.models import User


#Check if the login information is right.
def login_info_check(form, field):
	saved_hash_pwd = db.session.query(User.password).filter(User.email == field.data).first()
	if saved_hash_pwd is None:
		raise ValidationError('Invalid Email or password')

	hash_pwd = saved_hash_pwd[0]
	# print(hash_pwd)
	# print("Input value: " + form.password.data)
	if not check_password_hash(hash_pwd, form.password.data):
		raise ValidationError('Invalid Email or password')


#make sure the email address is unique before registering
def unique_email(form, field):
	exist_email = db.session.query(User).filter(User.email == form.email.data).first()
	if exist_email is not None:
		raise ValidationError('Email address already exists')


#When retrieve the forgot password, check if the given email address existed in the database
def email_check(form, field):
	fetched_email = db.session.query(User.email).filter(User.email == field.data).first()
	if fetched_email is None:
		raise ValidationError('No records for this Email address')


class LoginForm(Form):
    email = StringField('Email', validators=[InputRequired(), login_info_check, Email(message="Please input a valid Email address")])
    password = PasswordField('Password', validators=[InputRequired()])
    remember_me = BooleanField('Remember me', default=False)


#registering form
class JoinForm(Form):
    email = StringField('Email', validators=[InputRequired(), unique_email, Email(message="Please input a valid Email address")])
    password = PasswordField('Password', validators=[InputRequired(), EqualTo('confirm_password', message='Two passwords must match')])
    confirm_password = PasswordField('Confirm password', validators=[InputRequired()])
    first_name = StringField('First Name', validators=[InputRequired(), Length(max=10)])
    last_name = StringField('Last Name', validators=[InputRequired(), Length(max=10)])
    user_id = StringField('User ID', validators=[InputRequired(), Length(max=10)])
    department = StringField('Department', [InputRequired(), Length(max=40)])


class RetrievePwdForm(Form):
	email = StringField('Email', validators=[InputRequired(), email_check, Email(message="Please input a valid Email address")])


class PwdResetForm(Form):
	password = PasswordField('New password', validators=[InputRequired(), EqualTo('confirm_password', message='Two passwords must match')])
	confirm_password = PasswordField('Confirm new password', validators=[InputRequired()])