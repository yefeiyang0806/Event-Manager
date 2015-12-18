
from flask_wtf import Form
from flask_wtf.file import FileField, FileAllowed, FileRequired



class UploadForm(Form):
    upload = FileField('', validators=[
        FileRequired(),
        FileAllowed(['xlsx', 'xls'], 'excel only!')
    ])