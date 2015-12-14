import os
from flask import Flask, request, render_template, redirect, url_for,Blueprint
from werkzeug.utils import secure_filename
from pyexcel_xls import XLBook 
import  xdrlib ,sys
import xlrd

upload = Blueprint('upload', __name__)


# from flask_wtf.csrf import CsrfProtect

# csrf = CsrfProtect()

# def create_app():
#     app = Flask(__name__)
#     csrf.init_app(app)


UPLOAD_FOLDER = '/static/uploads'
ALLOWED_EXTENSIONS = set(['xlsx'])

@upload.route('/upload_file', methods=['GET', 'POST'])
def upload_file():

    if request.method == 'GET':
        return render_template('upload/upload.html')
    elif request.method == 'POST':
        f = request.files['file']
        if f and allowed_file(f.filename):
            filename = secure_filename(f.filename)
            print(filename.path)
            # f.save(os.path.join(UPLOAD_FOLDER, filename))  
            # return redirect(url_for('uploadtest'))   
            # return ("upload successfully!")


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.',1)[1] in ALLOWED_EXTENSIONS




def open_excel(file):
    try:
        data = xlrd.open_workbook(file)
        return (data)
    except Exception as e:
        print (str(e))




def excel_table_byindex(file ,colnameindex=0, by_index=0):
    data = open_excel(file)
    table = data.sheets()[by_index]
    nrows = table.nrows #
    ncols = table.ncols #
    colnames =  table.row_values(colnameindex) #某一行数据 
    list =[]
    for rownum in range(nrows):
        row = table.row_values(rownum)
        if row:
            app = {}
            for i in range(len(colnames)):
                app[colnames[i]] = row[i] 
                list.append(app)
    return (list)


def uploadtest():
    print("upload successfully")


# def print_xls(path):
#     data=xlrd.open_workbook(path)   #打开excel
#     table=data.sheets()[0] #打开excel的第几个sheet
#     nrows=table.nrows   #捕获到有效数据的行数
#     books=[]
#     for i in range(nrows):
#         ss=table.row_values(i)   #获取一行的所有值，每一列的值以列表项存在
#         #print ss
#         for i in range(len(ss)):
#             print (ss[i])         #输出一行中各个列的值
#             print ('+++++++++++++++++++')

def print_xls(path):
    data = open_excel(path)   #打开excel
    table=data.sheets()[0] #打开excel的第几个sheet
    nrows=table.nrows   #捕获到有效数据的行数
    books=[]
    for i in range(nrows):
        ss=table.row_values(i)   #获取一行的所有值，每一列的值以列表项存在
        #print ss
        if i == 0:
            continue
        temp=Topic(ss)
        print("111111111111111111111111111")
        db.session.add(temp)
        # elif:
        for j in range(len(ss)):
            print (ss[j])         #输出一行中各个列的值
            print("++++++++++++++++++++++++++++")


@upload.route('/test')
def test():
     print_xls('/uploads/test.xlsx')
