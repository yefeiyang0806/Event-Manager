import os
from config import ADMINS
from flask import Flask, request, render_template, redirect, url_for,Blueprint,g,current_app,send_from_directory
from werkzeug.utils import secure_filename
from pyexcel_xls import XLBook 
from .forms import UploadForm,SendEmailsForm
from ..models import Topic, User, Format, Content,Role_menu, Menu,Event,EventAttender
from app import db
import xlrd, re,random
from werkzeug.security import generate_password_hash
from ..emails import send_email
from flask.ext.login import login_user, logout_user, current_user, login_required
import urllib
import urllib.request
import requests

upload = Blueprint('upload', __name__)
full_name = ''
status = ''
menu_categories = list()


UPLOAD_FOLDER = 'uploads/'

@upload.route('/upload_file', methods=['GET', 'POST'])
@login_required
def upload_file():
    # full_name = g.user.full_name
    # status = g.user.status
    # menus = menus_of_role()
    form = UploadForm()    
    if form.validate_on_submit():
        filename = secure_filename(form.upload.data.filename)
        fpath = UPLOAD_FOLDER + filename
        form.upload.data.save(fpath) 
        value = form.choice_switcher.data
        if value == 'user':
            input_user_xls(fpath)
        elif filename == 'topic':
            input_topic_xls(fpath)
        message=" import successfully"
    else:
        filename = None
        message=" import failed"
    return render_template('upload/upload.html', form=form, filename=filename,message=message,full_name=full_name, menu_categories=menu_categories, status=status)



@upload.route('/send_emails', methods=['GET', 'POST'])
@login_required
def send_emails():
    # full_name = g.user.full_name
    # status = g.user.status
    user_id = g.user.user_id
    # menus = menus_of_role()
    form = SendEmailsForm() 
    form.set_options()   
    if form.validate_on_submit():
        filename = secure_filename(form.upload.data.filename)
        fpath = UPLOAD_FOLDER + filename
        event_id = form.event_id.data
        event = db.session.query(Event).filter(Event.event_id == event_id).first()
        template = event.email_template
        form.upload.data.save(fpath) 
        send_email_to_user(fpath, template, event_id)  
        message=" import successfully"
    else:
        filename = None
        message=" import failed"
    return render_template('upload/send_emails.html', form=form, filename=filename,message=message,full_name=full_name, menu_categories=menu_categories, status=status)

@upload.route('/template')
@login_required
def download():
    template_id = request.args.get('id')
    file_path = os.path.join(current_app.root_path, '../templatexlsx')
    if template_id == 'users':
        filename = 'users_template.xlsx'
    elif template_id == 'topic':
        filename = 'topic_template.xlsx'
    else:
        filename = 'event_template.xlsx'
    print(filename)
    return send_from_directory(directory=file_path, filename=filename,as_attachment=True,attachment_filename=filename) 



def send_email_to_user(path, template, event_id):
    data = open_excel(path)   
    table=data.sheets()[0] 
    nrows=table.nrows 
    books=[]
    accept = "accept"
    reject = "reject"
    for i in range(nrows):
        ss=table.row_values(i)  
        if i == 0:
            continue
        email = ss[0]
        full_name = ss[1]
        accept_link = basic_url + url_for('upload.user_status') + '?event_id=' + event_id +'&email='+email+'&full_name='+full_name+'&choose=' + accept 
        reject_link = basic_url + url_for('upload.user_status') + '?event_id=' + event_id + '&email='+email+'&full_name='+full_name+'&choose=' + reject
        send_email('Event Manager', ADMINS[0], [email], "Hello just for testing", \
            render_template(template, full_name=full_name, accept_link= accept_link, reject_link= reject_link))


@upload.route('/user_status')
def user_status():
    full_name = request.args.get("full_name")
    event_id = request.args.get("event_id")
    choose = request.args.get("choose")
    email = request.args.get("email")
    event = db.session.query(Event).filter(Event.event_id == event_id).first()
    if event is not None and choose == "accept":
        temp = EventAttender(event_id, full_name ,email)
        db.session.add(temp)
        db.session.commit()
        send_email('Event Manager', ADMINS[0], [email], "reply", \
            render_template("upload/accept_reply.html", full_name=full_name))
        msg = 'Thank you for joining ' + event.name
        result = 'Succeeded'
    else:
        msg = 'Thank you'
        result = 'Failed'
    return render_template('upload/reply_result.html', msg=msg, result=result, full_name= full_name)
    



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



def input_topic_xls(path):
    data = open_excel(path)   
    table=data.sheets()[0]
    nrows=table.nrows  
    books=[]
    for i in range(nrows):
        ss=table.row_values(i)  
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
    global full_name, status, menu_categories
    if hasattr(g.user, 'full_name'):
        full_name = g.user.full_name
    if hasattr(g.user, 'status'):
        status = g.user.status
        menu_categories = menus_of_role()

def generate_active_code():
    pool = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz'
    candidate = random.sample(pool, 4)
    active_code = candidate[0] + candidate[1] + candidate[2] + candidate[3]
    return str(active_code)

def menus_of_role():
    middles = db.session.query(Role_menu).filter(Role_menu.role_id == g.user.role_id).all()
    menu_categories = list()
    cat_grouped_menus = list()
    category_ids = list()
    menu_ids = list()
    for m in middles:
        certain_menu = db.session.query(Menu).filter(Menu.menu_id == m.menu_id).first()
        menu_ids.append(certain_menu.menu_id)
        if certain_menu.category_id not in category_ids:
            category_ids.append(certain_menu.category_id)
            cat_grouped_menus.append(certain_menu)
    for c in cat_grouped_menus:
        c_menus = list()
        cat = dict()
        cat['category_id'] = c.category_id
        cat['category_name'] = c.category_name
        menus = db.session.query(Menu).filter(Menu.category_id == c.category_id).filter().all()
        for m in menus:
            if m.menu_id in menu_ids:
                each_menu = dict()
                each_menu['menu_id'] = m.menu_id
                each_menu['menu_name'] = m.menu_name
                each_menu['url'] = m.url
                c_menus.append(each_menu)
        cat['menus'] = c_menus
        menu_categories.append(cat)

    # print (menu_categories)
    return menu_categories
