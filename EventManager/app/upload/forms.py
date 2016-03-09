from app import db
from flask_wtf import Form
from flask_wtf.file import FileField, FileAllowed, FileRequired
from wtforms import SelectField, RadioField
from ..models import Event

class UploadForm(Form):
    upload = FileField('', validators=[
        FileRequired(),
        FileAllowed(['xlsx', 'xls'], 'excel only!')    
    ])

    choice_switcher = RadioField('choice', choices=[('user', 'user'), ('topic', 'topic')], default='user'
    )

class SendEmailsForm(Form):
    upload = FileField('', validators=[
        FileRequired(),
        FileAllowed(['xlsx', 'xls'], 'excel only!')
	])
    event_id = SelectField('Event')     

    def set_options(self):
        events = db.session.query(Event).all()
        radio_list = list()
        for e in events:
            tup = (e.event_id, e.name)
            radio_list.append(tup)
        self.event_id.choices = radio_list
