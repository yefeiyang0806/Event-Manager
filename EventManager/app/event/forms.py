from app import db
from flask.ext.wtf import Form
from wtforms import StringField, BooleanField, PasswordField, IntegerField, DateTimeField, DateField, SelectField
from wtforms.validators import InputRequired, Length, Email, EqualTo, ValidationError
from ..models import Content, Format


class CreateEventForm(Form):
	topic = StringField('Topic', validators=[InputRequired()])
	description = StringField('Description', validators=[InputRequired()])
	speaker = StringField('Speaker', validators=[InputRequired()])
	
	contents = db.session.query(Content).all()
	radio_list = list()
	for c in contents:
		tup = (c.uuid, c.name)
		radio_list.append(tup)
	content = SelectField('Content', choices=radio_list)

	formats = db.session.query(Format).all()
	radio_list2 = list()
	for f in formats:
		tup2 = (f.uuid, f.name)
		radio_list2.append(tup2)
	format = SelectField('Format', choices=radio_list2)

	#format = StringField("Format", validators=[InputRequired()])
	min_attendance = IntegerField('Minimal attendance', default=10)
	max_attendance = IntegerField('Maximal attendance', default=200)