import xlrd
from app.models import Topic
from app import db


def open_excel(file):
    try:
        data = xlrd.open_workbook(file)
        return (data)
    except Exception as e:
        print (str(e))




def excel_table_byindex(file ,colnameindex=0, by_index=0):

	data = open_excel(file)
	table = data.sheets()[by_index]
	nrows = table.nrows #行数
	ncols = table.ncols #列数
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
		print("++++***********************++++++")
		startdata = ss[7].split('-')
		print("++**************************+++")
		print(startdata)
		print("++++***********************++++++")
		year_start = startdata[0]
		print("++**************************+++")
		print(year_start)
		print("++++***********************++++++")
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

			# print (ss[j])         #输出一行中各个列的值
			# print("++++++++++++++++++++++++++++")
     	# print("++++++++++++++++++++++++++++")
     	# print(year_start)
     	# print("++++++++++++++++++++++++++++")
		temp=Topic(title, description, min_attendance, max_attendance, speaker1, speaker2, speaker3,\
			year_start, month_start, day_start,day_duration,hour_duration,minute_duration, create_by,\
			content, format, location, link, jamlink )
		db.session.add(temp)
		db.session.commit()
		print("111111111111111111111111111111111111111111111111111")
		# elif:
		# for j in range(len(ss)):
		# 	print (ss[j])         #输出一行中各个列的值
		# 	print("++++++++++++++++++++++++++++")



# def print_xls(path):
# 	data = open_excel(path)   #打开excel
# 	table=data.sheets()[0] #打开excel的第几个sheet
# 	nrows=table.nrows   #捕获到有效数据的行数
# 	books=[]
# 	for i in range(nrows):
# 		ss=table.row_values(i)   #获取一行的所有值，每一列的值以列表项存在
# 		for j in range(len(ss)):
# 			print (ss[j])         #输出一行中各个列的值
# 			print("++++++++++++++++++++++++++++")



if __name__=='__main__':
	 # tables = excel_table_byindex('static/uploads/test.xlsx')
	 # for row in tables:
	 # 	print("aaaaaaaaaaaaaaaaaaaaaaaaaaaa")
	 # 	print (row)
	 # 	print("bbbbbbbbbbbbbbbbbbbbbbbbbbbbbb")
	 print_xls('uploads/topic.xlsx')


	