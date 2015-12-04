from app import db
from flask.ext.wtf import Form
from wtforms import StringField, BooleanField, PasswordField, IntegerField, DateTimeField, DateField, SelectField
from wtforms.validators import InputRequired, Length, Email, EqualTo, ValidationError
from ..models import Content, Format


def unique_title_year(form, field):
	exist_email = db.session.query(Topic).filter(Topic.email == form.email.data).first()
	if exist_email is not None:
		raise ValidationError('Email address already exists')



class CreateTopicForm(Form):
    title = StringField('Topic Title', validators=[InputRequired()])
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
            tup = (c.content_id, c.name)
            radio_list.append(tup)
        self.content.choices = radio_list
        
        formats = db.session.query(Format).all()
        radio_list2 = list()
        for f in formats:
            tup2 = (f.format_id, f.name)
            radio_list2.append(tup2)
        self.format.choices = radio_list2