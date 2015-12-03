from app import db
from flask.ext.wtf import Form
from wtforms import StringField, BooleanField, PasswordField, IntegerField, DateTimeField, DateField, SelectField
from wtforms.validators import InputRequired, Length, Email, EqualTo, ValidationError
from ..models import Content, Format


class CreateEventForm(Form):
	topic = StringField('Topic', validators=[InputRequired()])
	description = StringField('Description', validators=[InputRequired()])
	speaker = StringField('Speaker', validators=[InputRequired()])
	content = SelectField('Content')
	format = SelectField('Format')
	min_attendance = IntegerField('Minimal attendance', default=10)
	max_attendance = IntegerField('Maximal attendance', default=200)

	def set_options(self):
		contents = db.session.query(Content).all()
		radio_list = list()
		for c in contents:
			tup = (c.name, c.name)
			radio_list.append(tup)
		self.content.choices = radio_list

		formats = db.session.query(Format).all()
		radio_list2 = list()
		for f in formats:
			tup2 = (f.name, f.name)
			radio_list2.append(tup2)
		self.format.choices = radio_list2
