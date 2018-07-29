#! /usr/local/bin/python3
# -*- coding: utf-8 -*-
# 
import time
from servers.vendor.itchat import send
from servers.vendor.itchat.content import *
from servers.utils.wechatRecord import *


#当用户打开文件传输助手时响应这个函数
#


class Assistant():

	def __init__(self):
		self.tipsInfo = u'''回复序号即可快速操作
			11. 【关闭自动闲聊】
			12. 【开启自动闲聊】
			21. 【禁止撤回消息，将用户撤回的消息发送给ta自己】
			22. 【禁止撤回消息，将用户撤回的消息发送给文件传输助手】
			23. 【关闭禁止撤回消息】
			31. 【开启好友自动验证】
			32. 【关闭自动好友验证】
			41. 【开启忙碌状态】
			42. 【关闭忙碌状态】
		'''
		self.operatorStrDic = {
			"11": "自动闲聊已关闭",
			"12": "自动闲聊已开启",
			"21": "已禁止撤回消息，将用户撤回的消息发送给ta自己",
			"22": "已禁止撤回消息，将用户撤回的消息发送给文件传输助手",
			"23": "禁止撤回消息已关闭",
			"31": "好友自动验证已开启",
			"32": "好友自动验证已关闭",
			"41": "忙碌状态已开启",
			"42": "忙碌状态已关闭",
		}
		self.operatorDic = {
			"11": {"jokeSwitch":False},
			"12": {"jokeSwitch":True},
			"21": {"banRevokeSwitch":True, "revokeMsgToUser":""},
			"22": {"banRevokeSwitch":True, "revokeMsgToUser":"filehelper"},
			"23": {"banRevokeSwitch":False},
			"31": {"verifySwitch":True},
			"32": {"verifySwitch":False},
			"41": {"busySwitch":True},
			"42": {"busySwitch":False},
		}
	def operator(self, msg, userName):
		if msg["ToUserName"] != "filehelper": return
		if msg["Type"] in [SYSTEM]: self.printTips()
		elif msg["Type"] in [TEXT]: self.changeConfig(msg["Text"])


	def printTips(self):
		send(self.tipsInfo, "filehelper")


	def changeConfig(self, cmd):
		if cmd not in self.operatorDic: return
		recordUserConfig(self.operatorDic[cmd])
		send(self.operatorStrDic[cmd], "filehelper")


assistant = Assistant()