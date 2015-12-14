import xlrd
from .models import Topic
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
		temp=Topic(ss)
		print("111111111111111111111111111")
		db.session.add(temp)
		# elif:
		for j in range(len(ss)):
			print (ss[j])         #输出一行中各个列的值
			print("++++++++++++++++++++++++++++")




if __name__=='__main__':
	 # tables = excel_table_byindex('static/uploads/test.xlsx')
	 # for row in tables:
	 # 	print("aaaaaaaaaaaaaaaaaaaaaaaaaaaa")
	 # 	print (row)
	 # 	print("bbbbbbbbbbbbbbbbbbbbbbbbbbbbbb")
	 print_xls('static/uploads/test.xlsx')


	