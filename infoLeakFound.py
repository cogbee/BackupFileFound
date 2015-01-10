#!/usr/bin/env python
#encoding=utf-8

'''
function:it tests whether some bak files is exists. 
for example:if http://www.test.com/1.php is a right url,I will test http://www.test.com/11.php(12.php,2.php,1.php.bak)
author:jaffer
time:2015-01-10
version:1.0
构架：爬虫系统，url分析系统，保存url系统
需要改进的地方：1、程序速度，多线程？2、链接如果断了，该如何保持一段时间重连？3、代理爬虫？
'''

import pdb
import re
import httplib2
import urllib2
import urllib
from sys import argv
from os import makedirs,unlink,sep
from os.path import dirname,exists,isdir,splitext
from string import replace,find,lower
from htmllib import HTMLParser
from urllib import urlretrieve
from urllib import urlopen
from urlparse import urlparse,urljoin
from formatter import DumbWriter,AbstractFormatter
from cStringIO import StringIO
import sys 

pdb.set_trace()

reload(sys) 
sys.setdefaultencoding('utf8')

#url分析系统
class url_parse(object):
	def __init__(self,url):
		self.url = url
		self.url_test = []
		
		#判断是否是http://www.ssss.com/1.php的形式。同时增加判断，url大于512字节认为不可靠，过滤掉,
		#对带参数的一些url进行过滤。比如http://www.ssss.com/1.php?user=hi。
	def isValidUrl(self):
		if self.url.find('?') == -1:
			return 1
		else:
			return 0
		#判断是否有无法解析的url，比如一些doc文档。
	def isGoodUrl(self):
		if len(self.url) >= 512:
			return 1
		pat=re.compile(r'[0-9a-zA-Z._\-/\?:=&@]*\.(jpg|log|sql|md5|sh|swf|gif|cer|png|doc|xls|ppt|pptx|docs|rar|zip|pdf|chm|gz|gzip|apk|db|wmv|avi|ts|mp3|mp4|rmvb|tar)')
		match = pat.match(self.url)
		if match:
			return 1
		else:
			return 0
	def createUrl(self):
		#create .bak
		#print self.url+'-----'
		#http://www.ccc.cn 这样的url不处理，http://www.ccc.cn/../ 含有这样的.. 也不处理
		url_test_path = urlparse(self.url)
		if url_test_path.path == '' or url_test_path.path.find('./') != -1:
			return self.url_test
		self.url_test.append(self.url + '.bak')
		#create **1.php,**2.html
		url_len = len(self.url) - 1
		i = url_len
		flag = 0
		while i > 0:
			if self.url[i] == '.':
				flag = 1
				break
			if self.url[i] == '/':
				break
			i = i - 1
		#http://www.cccc.com/test
		if flag == 0:
			self.url_test.append(self.url + '1')
		else:
			#http://www.cccc.com/test.php
			self.url_test.append(self.url[0:i] + '1' + self.url[i:url_len+1])
			#http://www.cccc.com/test3.php
			isNum = re.search(r'[0-9]',self.url[i-1])
			if isNum:
				self.url_test.append(self.url)
				n = int(self.url[i-1])
				n = n + 1
				self.url_test.append(self.url[0:i-1]+ str(n) + self.url[i:url_len+1])
		return self.url_test

#url 变异引擎
class Exp(object):
	def __init__(self,url,file,cookie):
		self.url = url
		self.file = file
		self.cookie = cookie
		#self.result = []
	def getTest(self):
		try:
			h = httplib2.Http(timeout=0.1)
			headers = {}
			if self.cookie != '':
				headers = {'Cookie':self.cookie}
			for i in range(len(self.url)):
				#self.result.append(0)
				#print self.url[i] + '---++++++++------'
				res,con = h.request(self.url[i],'GET',headers = headers)
			#没有找到才存下来
				try:
					if res.status != 404:
						self.file.write(self.url[i]+'\n')
				finally:
					pass
		#处理超时的。将所有错误都捕获，然后忽略
		except Exception,e:
			pass
		#return self.result


#爬虫系统
class Retriever(object):
	def __init__(self,url):
		self.url = url


	#parse HTML ,save links
	def parseAndGetLinks(self):
		#print self.url
		list = []
		if self.url.find('./') != -1:
			return list
		try:
			self.parser = HTMLParser(AbstractFormatter(DumbWriter(StringIO())))
			#self.parser.getConnection().setConnectionTimeout(500)
			self.parser.feed(urlopen(self.url).read())
			self.parser.close()
		except Exception,e:
			return list
		return self.parser.anchorlist


#manage entire crawler
class Crawler(object):
	count = 0
	def __init__(self,url,cookie):
		self.q = [url]
		self.cookie = cookie
		self.seen = []
		self.dom = urlparse(url)[1]
		self.first = 0

	def getMyDom(self):
		dom_len = len(self.dom) - 1
		i = 0
		while( i < dom_len):
			if(self.dom[i] == '.'):
				break
			i = i + 1
		self.dom = self.dom[i+1:dom_len+1]


	def getPage(self,url):
		#gurl = url_parse(url)
		r = Retriever(url)
		#重新定义我们的域
		if self.first == 0:
			self.getMyDom()
			self.first = 1
		Crawler.count += 1
		self.seen.append(url)
		#if gurl.isGoodUrl() == 0:
		links = r.parseAndGetLinks()
		#else:
		#	links = []
		for eachLink in links:
			if eachLink in links:
				if eachLink[:4] != 'http' and find(eachLink,'://') == -1:
					eachLink = urljoin(url,eachLink)
				if find(lower(eachLink),'mailto:') != -1:
					continue
			if eachLink not in self.seen:
				if find(eachLink,self.dom) == -1:
					pass
				else:
					if eachLink not in self.q:
						self.q.append(eachLink)
					else:
						pass
			else:
				pass
		fp = open('url','a+')
		for i in range(len(links)):
			fp.write(links[i]+'\n')
		fp.close()
		

	def go(self):
		first = 0
		count = 0
		try:
			result = open('bak','a+')
		except IOError:
			print 'file open failed.'
			return
		while self.q:
			url = self.q.pop()
			count = count + 1
			print url
			#调用url分析系统--->调用sql注入引擎---->保存url
			self.getPage(url)
			goodurl = url_parse(url)
			#同时，对这个url进行判断。是否能够解析，是否是http://www.ssss/index.apk的类似形式
			if goodurl.isGoodUrl() == 1:
				continue
			#是否是http://www.ssss/?id=11的类似形式
			if goodurl.isValidUrl() == 1:
				url_list = goodurl.createUrl()
				#url 变异引擎
				sql = Exp(url_list,result,self.cookie)
				sql.getTest()
		print 'the all url we crawl is %d\n' % count
		result.close()


def main():
	if len(argv) > 1:
		url = argv[1]
	else:
		try:
			url = raw_input('Enter starting URL:')
		except (KeyboardInterrupt,EOFError):
			url = ''
		if not url:
			return
	cookie = raw_input('please input your cookie.if you do not have one,just go:\n')
	robot = Crawler(url,cookie)
	robot.go()


if __name__ == '__main__':
	main()
	print '\nover \n the reuslt is in the file result.please input enter to quit'
	raw_input()
