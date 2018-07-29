#! /usr/bin/python3
# -*- coding: utf-8 -*-
# 从wsgiref模块导入:
from flup.server.fcgi import WSGIServer
import os, sys, traceback
from imp import reload
from servers import wechatInterface
from servers.utils.wechatLog import wechatLog

def retFormat(ret):
	'''
		change ret to list and encode with utf-8
	'''
	if not ret: return None
	if isinstance(ret, list):
		if isinstance(ret[0], bytes): return ret
		else:
			ret = map(lambda m:m.encode('utf-8'), ret)
			return ret
	elif isinstance(ret, bytes):
		return [ret]
	else: return [ret.encode('utf-8')]

def contentType(suffix):
	dic = {
		'.html'	:	('Content-Type', '%s' % 'text/html'),
		'.jpg'	:	('Content-Type', '%s' % 'image/jpeg'),
		'.png'	:	('Content-Type', '%s' % 'image/jpeg'),
		'.css'	:	('Content-Type', '%s' % 'text/css'),
		'.js'	:	('Content-Type', '%s' % 'application/javascript'),
	}
	if suffix not in dic:
		return ('Content-Type', 'text/html')
	return dic[suffix]

def parsePathInfo(pathInfo):
	try:
		filepath, lastfilename = os.path.split(pathInfo)
		shotname, extension = os.path.splitext(lastfilename)
		return shotname, extension
	except:
		return None, None

def importModule(module):
	glob = {}
	loc = {}
	try:
		exec(module, glob, loc)
		for item in loc:
			return loc[item]
	except:
		wechatLog.debug(traceback.format_exc())
		return False

def hotUpdate():
	reload(wechatInterface)

def application(environ, start_response):
	#hotUpdate()
	content = "OK!"
	filepath = environ['PATH_INFO'][1:] #去掉开头的/

	#wechatLog.debug("filepath = ", filepath)
	funcName, suffix = parsePathInfo(filepath)
	if suffix in ['.js', '.css', '.png', '.jpg']:
		try:
			with open(filepath, 'rb') as f:
				start_response('200 OK', [contentType(suffix)])
				return retFormat(f.read())
		except:
			start_response('404 NOT FOUND', [contentType(suffix)])
			return retFormat('404 NOT FOUND')
		
	if suffix in ['.html'] or not funcName: #访问首页
		start_response('200 OK', [('Content-Type', 'text/html')])
		location = "html/%s" % (filepath or "login.html")
		#wechatLog.debug("location = ", location)
		with open(location, 'rb') as f:
			return retFormat(f.read())
	
	if suffix not in ['.request']:
		start_response('404 OK', [('Content-Type', 'text/html')])
		with open("html/404.html", 'rb') as f:
			return retFormat(f.read())
		
	importFunc = "from servers.wechatInterface import %s as execfunc" % (funcName)
	#wechatLog.debug(importFunc)
	execfunc = importModule(importFunc)

	if not execfunc:
		start_response('403 Forbidden', [('Content-Type', 'text/html')])
		return retFormat("403 Forbidden")

	requestBodySize = environ.get('CONTENT_LENGTH', 0)
	if not requestBodySize: requestBodySize = 0
	else: requestBodySize = int(requestBodySize)

	requestBody = environ["wsgi.input"].read(requestBodySize)
	if not requestBody: ret = execfunc()
	else: ret = execfunc(requestBody)
	
	start_response('200 OK', [('Content-Type', 'text/plain')])
	return retFormat(ret) or retFormat(content)

'''
# 创建一个服务器，IP地址为空，端口是8000，处理函数是application:
try:
	PORT = int(sys.argv[1])
except:
	PORT = 8000
httpd = make_server('', PORT, application)
wechatLog.debug('Serving HTTP on port %d...' % PORT)

# 开始监听HTTP请求:
httpd.serve_forever()
'''
if __name__  == '__main__':
	WSGIServer(application).run()
