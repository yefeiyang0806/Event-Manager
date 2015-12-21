import os
from flask import Flask, request, render_template, redirect, url_for,Blueprint
from werkzeug.utils import secure_filename
from pyexcel_xls import XLBook 
from .forms import UploadForm
from ..models import Topic, User
from app import db
import xlrd, re,random
from werkzeug.security import generate_password_hash

upload = Blueprint('upload', __name__)



UPLOAD_FOLDER = '/static/uploads'

@upload.route('/upload_file', methods=['GET', 'POST'])
def upload_file():    
    form = UploadForm()    
    if form.validate_on_submit():
        filename = secure_filename(form.upload.data.filename)
        print(filename)
        fpath = 'uploads/' + filename
        form.upload.data.save(fpath) 

        # input_user_xls(fpath)
        # input_createuser_xls(path)
        input_topic_xls(fpath)
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


def input_user_xls(path):
    data = open_excel(path)   #打开excel
    table=data.sheets()[0] #打开excel的第几个sheet
    nrows=table.nrows   #捕获到有效数据的行数
    books=[]
    for i in range(nrows):
        ss=table.row_values(i)   #获取一行的所有值，每一列的值以列表项存在
        if i == 0:
            continue
        # result = []
        index = 0;
        tempss = []
        for s in ss:
            tempss.append(s)
            index = index + 1            
            if index == 8:
                rolename = tempss[0]
                last_name = tempss[1]
                first_name = tempss[2]
                # full_name= last_name + first_name
                job = tempss[3]
                department = tempss[4]
                country = tempss[5]
                email = tempss[6]
                s1 = tempss[7]
                user_id = ifcomma(s1)
                title = ''
                password = hash_password = generate_password_hash("init123")
                if job == 'Mr.' or job == 'Ms.':
                    title = job
                    job = ''

                active_code = generate_active_code()
             
                usertemp = db.session.query(User).filter(User.user_id == user_id).first()
                print(usertemp)

                if usertemp is not None or user_id == '' or user_id is None:
                    print('user address already exists')
                else:  
                    print("*****************************************")              
                    temp=User(user_id, email, password, first_name, last_name, department,active_code,title, job, country, rolename)
                    db.session.add(temp)
                    db.session.commit()

                # result.append(tempss)
                print(tempss)
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
        temp=Topic(topic_id,title, description, speaker1, speaker2, speaker3, speaker4, speaker5, \
            create_by, status, memo, content, format)
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

def generate_active_code():
    pool = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz'
    candidate = random.sample(pool, 4)
    active_code = candidate[0] + candidate[1] + candidate[2] + candidate[3]
    return str(active_code)