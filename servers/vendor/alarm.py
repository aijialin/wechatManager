#! /usr/local/bin/python3
# -*- coding: utf-8 -*-
# 
# 
from servers.utils.wechatRecord import *
import threading, time, sys, os

# 开启一个线程，然后去sleep, 睡够时间后去检查登陆状态，如果成功，则什么也不做，若没成功，则设置超时断开
def overtime(t):
	time.sleep(t)
	statusFile = initSatatusFile()
	try:
		with open(statusFile, "r") as f:
			data = f.read()
			dataDic = json.loads(data)
			if dataDic["loginCode"] != 5:
				recordeStatus({"loginStatus": "Please refresh the page ..", "loginCode":101})
				#sys.exit(1) 无法结束整个进程
				os._exit(1)
	except:
		os._exit(1)
	
task = threading.Thread(target=overtime, args=(30, ))
task.setDaemon(True)
task.start()