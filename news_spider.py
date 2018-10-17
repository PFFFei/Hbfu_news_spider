# -*- coding:UTF-8 -*-
from bs4 import BeautifulSoup
import requests
import pymongo
 
def spider(url):
	server = 'http://www.ysu.edu.cn/info/2178/'
	req = requests.get(url)
	global number				#gobal引用全局变量
	global title_list
	global content_list
	html = req.content.decode('utf-8')#解码
	div_bf = BeautifulSoup(html,'html.parser')#html解析器
	news_content = div_bf.find_all('div',class_='content')#find_all返回的是列表
	news_title = div_bf.select('form > div > div > h3')#select是BeautifulSoup的函数
	for item in news_content:#循环遍历列表
		if item.text not in title_list:#写入列表，如果不存在则写入
			content_list.append(item.text)
	for title in news_title:
		if title.text not in title_list:
	 		title_list.append(title.text)
	news_content = div_bf.select('form > div > div > a')
	try:
		if number == 1 :
			next_url = server + news_content[0].get('href')#第一页的下一条新闻地址
			number = number + 1
		else:
			next_url = server + news_content[1].get('href')#下一条新闻地址
			number = number + 1	
		print(number)
		if number < 160:
			return spider(next_url)
	except Exception as e:#捕捉异常 最后一页没有下一条
		print('新闻爬虫完毕！')
def database():
	global title_list
	global content_list
	client = pymongo.MongoClient("localhost:27017")#连接数据库
	db = client.test#获取数据库名称
	users = db.users#获取集合
	db.users.remove()#清空数据库信息
	for i in range(len(title_list)-3):
		db.users.insert({'title': title_list[i], 'content':content_list[i]})#json数据
	try:
		while True:
			search = input('请输入查询内容:\n')
			u = db.users.find_one({"title":search})#查询一条数据，使用循环查询
			print(u.get('content'))
	except Exception as e:
		print('新闻查询结束！')
	
if __name__ == '__main__':
	number = 1
	title_list = []
	content_list = []
	url = 'http://www.ysu.edu.cn/info/2178/4041.htm'
	spider(url)
	print('新闻标题列表如下：')
	for each in title_list:
		print(each)
	database()
