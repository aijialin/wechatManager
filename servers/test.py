#! /usr/local/bin/python3
# -*- coding: utf-8 -*-
# 
from utils.wechatRecord import *
import random, hashlib, json, os
import time, traceback
from utils.wechatConfig import *
from utils.wechatLog import *


import datetime, sys
def get_date():
    now = datetime.datetime.now()
    print(now)
    return now.strftime('%Y-%m-%d %H:%M:%S')

def timeTodate(timeStamp):
	timeObj = time.localtime(timeStamp)
	readTime = time.strftime("%Y-%m-%d %H:%M:%S", timeObj)
	return readTime

print(timeTodate(1532500288))

try:
	userKey = sys.argv[1]
except:
	userKey = 8000

print(sys.argv[0])

