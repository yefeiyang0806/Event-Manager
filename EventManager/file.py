import xlrd
from flask import Flask, request, render_template, redirect
from werkzeug.utils import secure_filename
from app.models import Topic
from app import db


# ALLOWED_EXTENSIONS = set(['xlsx','xls'])

# @app.route('/import', methods=['GET', 'POST'])
# def import_xlsx():

#     if request.method == 'GET':
#         return render_template('upload/upload.html')
#     elif request.method == 'POST':
#         f = request.files['file']
#         if f and allowed_file(f.filename):
#             filename = secure_filename(f.filename)
#             f.save(os.path.join(UPLOAD_FOLDER, filename))  
#             return redirect(url_for('uploadtest'))   
#             # return ("upload successfully!")


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.',1)[1] in ALLOWED_EXTENSIONS


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
		#print ss
		if i == 0:
			continue
		# for j in range(len(ss)):
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
		print("111111111111111111111111111111111111111111111111111")



if __name__=='__main__':
	print('******************************************8')
	print_xls(r+'C:\Users\i325391\Desktop\topic2.xlsx')


	