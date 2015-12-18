import os
from flask import Flask, request, render_template, redirect, url_for,Blueprint
from werkzeug.utils import secure_filename
from pyexcel_xls import XLBook 
from .forms import UploadForm
from ..models import Topic
from app import db
import xlrd

upload = Blueprint('upload', __name__)


# from flask_wtf.csrf import CsrfProtect

# csrf = CsrfProtect()

# def create_app():
#     app = Flask(__name__)
#     csrf.init_app(app)


UPLOAD_FOLDER = '/static/uploads'

@upload.route('/upload_file', methods=['GET', 'POST'])
def upload_file():    
    form = UploadForm()    
    if form.validate_on_submit():
        filename = secure_filename(form.upload.data.filename)
        print(filename)
        fpath = 'uploads/' + filename
        form.upload.data.save(fpath)  
        print_xls(fpath)
        message=" import successfully"
    else:
        filename = None
        message=" import failed"
    return render_template('upload/upload.html', form=form, filename=filename,message=message)

def open_excel(path):
    try:
        data = xlrd.open_workbook(path)
        return (data)
    except Exception as e:
        print (str(e))



def print_xls(path):
    data = open_excel(path)   #打开excel
    table=data.sheets()[0] #打开excel的第几个sheet
    nrows=table.nrows   #捕获到有效数据的行数
    books=[]
    for i in range(nrows):
        ss=table.row_values(i)   #获取一行的所有值，每一列的值以列表项存在
        if i == 0:
            continue
        title = ss[0]
        description = ss[1]
        min_attendance = ss[2]
        max_attendance = ss[3]
        speaker1 = ss[4]
        speaker2 = ss[5]
        speaker3 = ss[6]
        startdata = ss[7].split('-')
        print(startdata)
        year_start = startdata[0]
        print(year_start)
        month_start = startdata[1]
        day_start = startdata[2]
        day_duration = ss[8]
        hour_duration = ss[9]
        minute_duration = ss[10]
        create_by = ss[11]
        content = ss[12]
        format = ss[13]
        print(format)
        location = ss[14]
        link = ss[15]
        jamlink  = ss[16]
        temp=Topic(title, description, min_attendance, max_attendance, speaker1, speaker2, speaker3,\
            year_start, month_start, day_start,day_duration,hour_duration,minute_duration, create_by,\
            content, format, location, link, jamlink )
        db.session.add(temp)
        db.session.commit()
       





def uploadtest():
    print("upload successfully")



@upload.route('/test')
def test():
     print_xls('uploads/test2.xlsx')
