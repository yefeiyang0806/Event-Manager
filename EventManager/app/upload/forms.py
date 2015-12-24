from app import db
from flask_wtf import Form
from flask_wtf.file import FileField, FileAllowed, FileRequired
from wtforms import SelectField
from ..models import Event

class UploadForm(Form):
    upload = FileField('', validators=[
        FileRequired(),
        FileAllowed(['xlsx', 'xls'], 'excel only!')
    ])

class SendEmailsForm(Form):
    upload = FileField('', validators=[
        FileRequired(),
        FileAllowed(['xlsx', 'xls'], 'excel only!')
<<<<<<< HEAD
	])
    event = SelectField('Event') 


=======
        ])
    event = SelectField('Event')
>>>>>>> 32f03a8c789b4b0073a061fceb3bccabf058998e
    

    def set_options(self):
        events = db.session.query(Event).all()
        radio_list = list()
        for e in events:
            tup = (e.event_id, e.name)
            radio_list.append(tup)
        self.event.choices = radio_list