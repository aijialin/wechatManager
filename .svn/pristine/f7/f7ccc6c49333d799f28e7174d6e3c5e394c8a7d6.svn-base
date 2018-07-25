#! /usr/local/bin/python3
# -*- coding: utf-8 -*-
# 
import time
from ..itchat.content import *
from ..wechatRecord import *


def isVerifyType(msg):
	if msg['Type'] not in [FRIENDS]: 
		return False
	return True

def response(verifyContent, msg):
	if not isVerifyType(msg): return
	verifyContent = verifyContent.split('|')
	msg.user.verify()
	recordUserConfig({"newFriendsCount" : 1}, "add") #接受好友数加一
	recordUserConfig({"friendsCount" : 1}, "add") #总的好友数加一
	for m in verifyContent:
		msg.user.send(m)
		time.sleep(1)
		return