from app import db
from flask.ext.wtf import Form
from wtforms import StringField, BooleanField, PasswordField, IntegerField, DateTimeField, DateField
from wtforms.validators import InputRequired, Length, Email, EqualTo, ValidationError


class CreateEventForm(Form):
	topic = StringField('Topic', validators=[InputRequired()])
	description = StringField('Description', validators=[InputRequired()])
	speaker = StringField('Speaker', validators=[InputRequired()])
	content = StringField("Content Type", validators=[InputRequired()])
	format = StringField("Format", validators=[InputRequired()])
	min_attendance = IntegerField('Minimal attendance', default=10)
	max_attendance = IntegerField('Maximal attendance', default=200)
