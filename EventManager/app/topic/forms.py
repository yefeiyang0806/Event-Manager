from app import db
from flask.ext.wtf import Form
from wtforms import StringField, BooleanField, PasswordField, IntegerField, DateTimeField, DateField, SelectField
from wtforms.validators import InputRequired, Length, Email, EqualTo, ValidationError
from ..models import Content, Format


class CreateTopicForm(Form):
<<<<<<< HEAD
    topic = StringField('Topic Title', validators=[InputRequired()])
    description = StringField('Description', validators=[InputRequired()])
    speaker = StringField('Speaker', validators=[InputRequired()])
    content = SelectField('Content')
    format = SelectField('Format')
    min_attendance = IntegerField('Minimal attendance', default=10)
    max_attendance = IntegerField('Maximal attendance', default=200)
    DateStart = StringField("DateStart", id="start_date")
    day_duration = StringField('Day_Duration', validators=[InputRequired()], default='0')
    hour_duration = StringField('Hour_Duration', validators=[InputRequired()], default='0')
    minute_duration = StringField('Minute_Duration', validators=[InputRequired()], default='15')
    link = StringField("Link")
    jamlink = StringField("JamLink")
    speaker1 = StringField('Speaker1', validators=[InputRequired()])
    speaker2 = StringField('Speaker2')
    speaker3 = StringField('Speaker3')
    location = StringField('Location', validators=[InputRequired()])

    def set_options(self):
        contents = db.session.query(Content).all()
        radio_list = list()
        for c in contents:
            tup = (c.name, c.content_id)
            radio_list.append(tup)
        self.content.choices = radio_list
        
        formats = db.session.query(Format).all()
        radio_list2 = list()
        for f in formats:
            tup2 = (f.name, f.format_id)
            radio_list2.append(tup2)
        self.format.choices = radio_list2
=======
	topic = StringField('Topic Title', validators=[InputRequired()])
	description = StringField('Description', validators=[InputRequired()])
	speaker = StringField('Speaker', validators=[InputRequired()])
	content = SelectField('Content')
	format = SelectField('Format')
	min_attendance = IntegerField('Minimal attendance', default=10)
	max_attendance = IntegerField('Maximal attendance', default=200)
	DateStart = StringField("DateStart", id="start_date")
	day_duration = StringField('Day_Duration', validators=[InputRequired()], default='1')
	hour_duration = StringField('Hour_Duration', validators=[InputRequired()], default='2')
	minute_duration = StringField('Minute_Duration', validators=[InputRequired()], default='15')
	link = StringField("Link", validators=[InputRequired()])
	jamlink = StringField("JamLink", validators=[InputRequired()])
	speaker1 = StringField('Speaker1', validators=[InputRequired()])
	speaker2 = StringField('Speaker2', validators=[InputRequired()])
	speaker3 = StringField('Speaker3', validators=[InputRequired()])
	location = StringField('Location', validators=[InputRequired()])

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


		
		
>>>>>>> 1ed3f83cf0c340fb88945957c3741db4daba23e6
