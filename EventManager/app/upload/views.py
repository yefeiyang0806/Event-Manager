import os
from config import ADMINS
from flask import Flask, request, render_template, redirect, url_for,Blueprint,g
from werkzeug.utils import secure_filename
from pyexcel_xls import XLBook 
from .forms import UploadForm,SendEmailsForm
from ..models import Topic, User, Format, Content,Role_menu, Menu
from app import db
import xlrd, re,random
from werkzeug.security import generate_password_hash
from ..emails import send_email
from flask.ext.login import login_user, logout_user, current_user, login_required

upload = Blueprint('upload', __name__)



UPLOAD_FOLDER = 'uploads/'

@upload.route('/upload_file', methods=['GET', 'POST'])
@login_required
def upload_file():
    full_name = g.user.full_name
    status = g.user.status
    menus = menus_of_role()
    form = UploadForm()    
    if form.validate_on_submit():
        filename = secure_filename(form.upload.data.filename)
        fpath = UPLOAD_FOLDER + filename
        form.upload.data.save(fpath) 
        if filename == 'users.xlsx':
            input_user_xls(fpath)
        elif filename == 'topic.xlsx':
            input_topic_xls(fpath)
        message=" import successfully"
    else:
        filename = None
        message=" import failed"
    return render_template('upload/upload.html', form=form, filename=filename,message=message,full_name=full_name, menus=menus, status=status)



@upload.route('/send_emails', methods=['GET', 'POST'])
@login_required
def send_emails():
    full_name = g.user.full_name
    status = g.user.status
    user_id = g.user.user_id
    menus = menus_of_role()
    form = SendEmailsForm() 
    # form.set_options()   
    if form.validate_on_submit():
        filename = secure_filename(form.upload.data.filename)
        fpath = UPLOAD_FOLDER + filename
        form.upload.data.save(fpath) 
        send_email_to_user(fpath)  
        message=" import successfully"
    else:
        filename = None
        message=" import failed"
    return render_template('upload/send_emails.html', form=form, filename=filename,message=message,full_name=full_name, menus=menus, status=status)

def send_email_to_user(path):
    data = open_excel(path)   
    table=data.sheets()[0] 
    nrows=table.nrows 
    books=[]
    for i in range(nrows):
        ss=table.row_values(i)  
        if i == 0:
            continue
        email = ss[0]
        full_name = ss[1]
        print("^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^6")
        print(email)
        print(full_name)
        print("^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^6")
        send_email('Event Manager', ADMINS[0], [email], "Hello just for testing", \
            render_template('upload/email/D-com.html', full_name=full_name))







def open_excel(path):
    try:
        data = xlrd.open_workbook(path)
        return (data)
    except Exception as e:
        print (str(e))


def input_user_xls(path):
    data = open_excel(path)   
    table=data.sheets()[0] 
    nrows=table.nrows 
    books=[]
    for i in range(nrows):
        ss=table.row_values(i)  
        if i == 0:
            continue
        # result = []
        index = 0;
        tempss = []
        for s in ss:
            tempss.append(s)
            index = index + 1            
            if index == 9:
                speaker_id = tempss[0]
                rolename = tempss[1]
                last_name = tempss[2]
                first_name = tempss[3]
                job = tempss[4]
                department = tempss[5]
                country = tempss[6]
                email = tempss[7]
                s1 = tempss[8]
                user_id = ifcomma(s1)
                title = ''
                password = hash_password = generate_password_hash("init123")
                if job == 'Mr.' or job == 'Ms.':
                    title = job
                    job = ''
                active_code = generate_active_code()             
                usertemp = db.session.query(User).filter(User.user_id == user_id).first()
                if usertemp is not None or user_id == '' or user_id is None:
                    print('user'+user_id+' already exists')
                else:           
                    temp=User(user_id, email, password, first_name, last_name, department,active_code,title, job, country, rolename, speaker_id)
                    db.session.add(temp)
                    db.session.commit()
                tempss = []
                index = 0
        print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")
        print(i)
        print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")



def input_topic_xls(path):
    data = open_excel(path)   #打开excel
    table=data.sheets()[0] #打开excel的第几个sheet
    nrows=table.nrows   #捕获到有效数据的行数
    books=[]
    for i in range(nrows):
        ss=table.row_values(i)   #获取一行的所有值，每一列的值以列表项存在
        if i == 0:
            continue
        topic_id = ss[0]
        statustemp = ss[1]
        format = ss[2]
        content = ss[3]
        title = ss[4]
        description = ss[5]
        memo = ss[6]
        speaker1 = ifcomma(ss[7])
        speaker2 = ifcomma(ss[8])
        speaker3 = ifcomma(ss[9])
        speaker4 = ifcomma(ss[10])
        speaker5 = ifcomma(ss[11])
        create_by = ifcomma(ss[12])    
        if statustemp == 'Accepted':
            status = 'AP' 
        elif statustemp == 'Rejected':
            status = 'RJ' 
        min_attendance = 0
        max_attendance = 0
        day_duration = '0'
        hour_duration = '0'
        minute_duration = '20'
        year_start = '2016'
        month_start = ''
        day_start = ''
        location = ''
        link = ''
        jamlink = ''
        topictemp = db.session.query(Topic).filter(Topic.topic_id == topic_id).first()
        if topictemp is not None or topic_id == '' or topic_id is None:
            print(topic_id+'Topic already exists')
        else:           
            temp=Topic(topic_id,title, description, min_attendance, max_attendance, speaker1, speaker2, speaker3, speaker4, speaker5, \
              year_start, month_start, day_start,day_duration, hour_duration, minute_duration ,create_by,\
              content, format, location, link, jamlink, memo, status)
            db.session.add(temp)
            db.session.commit()
        print("^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^")
        print(i)
        print("^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^")


def ifcomma(data):    
    an = re.search(',', data)
    if an:
        s1 = data.split(',')
        user_id = s1[0]
    else:
        user_id = data
    return user_id



def uploadtest():
    print("upload successfully")



@upload.route('/test')
def test():
     input_user_xls('uploads/test2.xlsx')

#Refresh the global variable before every request
@upload.before_request
def before_request():
    g.user = current_user

def generate_active_code():
    pool = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz'
    candidate = random.sample(pool, 4)
    active_code = candidate[0] + candidate[1] + candidate[2] + candidate[3]
    return str(active_code)

def menus_of_role():
    middles = db.session.query(Role_menu).filter(Role_menu.role_id == g.user.role_id).all()
    menus = list()
    for m in middles:
        menu = db.session.query(Menu).filter(Menu.menu_id == m.menu_id).first()
        menus.append(menu)
    print (menus)
    return menus
