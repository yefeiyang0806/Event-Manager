from app import db
from flask.ext.wtf import Form
from wtforms import StringField, BooleanField, PasswordField, IntegerField, DateTimeField, DateField
from wtforms.validators import InputRequired, Length, Email, EqualTo, ValidationError


class CreateEventForm(Form):
	topic = StringField('Topic', validators=[InputRequired()])
	description = StringField('Description', validators=[InputRequired()])
	min_attendance = IntegerField('Minimal attendance', default=10)
	max_attendance = IntegerField('Maximal attendance', default=200)
	location = StringField('Location', validators=[InputRequired()], default='TBD')
	host = StringField('Host', validators=[InputRequired()], default='TBD')
	duration = IntegerField("Event Duration", default=30, validators=[InputRequired()])
	start_date = DateField("Event Starts at", validators=[InputRequired()], id="start_date")