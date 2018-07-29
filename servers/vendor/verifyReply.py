#! /usr/local/bin/python3
# -*- coding: utf-8 -*-
# 
import time
from servers.vendor.itchat.content import *
from servers.utils.wechatRecord import *


def isVerifyType(msg):
	if msg['Type'] not in [FRIENDS]: 
		return False
	return True

def response(verifyContent, msg):
	if not isVerifyType(msg): return
	verifyContent = verifyContent.split('|')
	msg.user.verify()
	recordUserConfig({"newFriendsCount" : 1}, "count") #接受好友数加一
	recordUserConfig({"friendsCount" : 1}, "count") #总的好友数加一
	for m in verifyContent:
		msg.user.send(m)
		time.sleep(1)
		return