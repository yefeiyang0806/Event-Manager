from app import db
from flask.ext.wtf import Form
from wtforms import StringField, BooleanField, PasswordField, IntegerField, DateTimeField, DateField
from wtforms.validators import InputRequired, Length, Email, EqualTo, ValidationError


class CreateRoleForm(Form):
	rolename = StringField('Rolename', validators=[InputRequired()])
	description = StringField('Description', validators=[InputRequired()])