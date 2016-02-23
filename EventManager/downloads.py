# import urllib 
# import urllib2 
# import requests
# print ("downloading with urllib")
# url = 'http://www.pythontab.com/test/demo.zip'  
# print ("downloading with urllib")
# urllib.urlretrieve(url, "demo.zip")
import urllib.request
resp=urllib.request.urlopen('uploads/users_template.xlsx')
html=resp.read()
print(html)