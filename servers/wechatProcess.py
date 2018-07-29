#! /usr/local/bin/python3
# -*- coding: utf-8 -*-
# 

import time, json, sys, os, base64
from servers.utils.wechatConfig import *
from servers.utils.wechatLog import wechatLog
from servers.utils.wechatRecord import *


import servers.vendor.itchat as itchat
from servers.vendor.itchat.content import *

from servers.vendor import alarm  #一个线程， 如果超时未登录成功，则结束这个进程
from servers.vendor import jokeReply
from servers.vendor import busyReply
from servers.vendor import verifyReply
from servers.vendor.operateAssistant import assistant
from servers.vendor.banRevoke import recoke

from servers.vendor.hooks import itchat_check_login
from servers.vendor.hooks import itchat_get_QR



lastModifyTime = 0.0 #上一次修改用户配置文件的时间
userConfig = {} #用户配置文件
maxRetryTimes = 1 #最大允许超时重新获取二维码次数


wechatLog.info(json.dumps(sys.argv))
userKey = sys.argv[1]
wechatLog.info("userKey = %s" % userKey)
if userKey == None:
    wechatLog.info('userKey None')
    sys.exit()

#userKey = str(time.time())
initSatatusFile(userKey) #初始化运行日志文件写入{usrKey}

def checkAndUpdateConfig():
    global userConfig, lastModifyTime
    userConfigFile = initUserConfigFile()
    testTime = os.path.getmtime(userConfigFile)
    if testTime != lastModifyTime:
        lastModifyTime = testTime
        userConfig = getUserConfig()


@itchat.msg_register(INCOME_MSG)
def wechat(msg):
    checkAndUpdateConfig()
    userName = userConfig["userName"]
    if msg["FromUserName"] in ["newsapp"]: return #过滤掉腾讯新闻的消息
    wechatLog.info(msg)
    recoke.saveMessage(msg, userConfig) #为了随时撤回，每一条消息都要及时保存
    assistant.operator(msg, userName) #当用户打开文件助手时，打印操作消息
    if userConfig["verifySwitch"]: verifyReply.response(userConfig["verifyContent"], msg)
    if userConfig["banRevokeSwitch"]: recoke.response(userConfig["revokeMsgToUser"])
    if userConfig["jokeSwitch"]: return jokeReply.response(msg, userName)
    if userConfig["busySwitch"]: return busyReply.response(userConfig["busyContent"], msg, userName)



def qrCallback(uuid, status, qrcode):
    global maxRetryTimes
    wechatLog.info("status=%s\tuuid = %s" % (status, uuid))
    if status=='0' and qrcode:
        #wechatLog.info("Please scan the QR code to log in")
        recordeStatus({"loginStatus":"Please scan the QR code to log in", "uuid":uuid, "qrcode":"data:image/png;base64," + base64.b64encode(qrcode).decode('utf-8'), "loginCode":2})
        return
    if status == '201':
        recordeStatus({"loginStatus":"Please press confirm on your phone", "loginCode":3})
        #wechatLog.info("confirm on phone")
        return
    if status == '200':
        recordeStatus({"loginStatus":"Loading the contact, this may take a little while", "loginCode":4})
        wechatLog.info("load contact")
        return
    if status != '408':
        if maxRetryTimes <= 0: 
            recordeStatus({"loginStatus": "Please refresh the page", "loginCode":101})
            sys.exit(1)
        maxRetryTimes -= 1
        recordeStatus({"loginStatus":"Log in time out, reloading QR code %d" % maxRetryTimes, "loginCode":100})
        #wechatLog.info("Log in time out, reloading QR code.")
        return
        

def loginCallback():
    nickName = itchat.originInstance.storageClass.nickName
    userName = itchat.originInstance.storageClass.userName
    recordeStatus({"loginStatus":"Login successfully as %s" % nickName, "loginCode":5, "nickName":nickName})
    initUserConfigFile(nickName)
    userConfDic1 = {
            "busyContent"       : DEFAULTREPLYCONTENT, 
            "verifyContent"     : DEFAULTVERIFYCONTENT,
            "jokeSwitch"        : True,
            "busySwitch"        : False,
            "verifySwitch"      : True,
            "banRevokeSwitch"   : False,
            "revokeMsgToUser"   : "",
            }
    recordUserConfig(userConfDic1, "checkkey") # 设置默认值 如果没有就添加，有就放弃
    userConfDic2 = {
            "loginStatus"       : "success",
            "loginTime"         : getCurDate(),
            "friendsCount"      : len(itchat.originInstance.storageClass.memberList),
            "recMsgCount"       : 0,
            "sendMsgCount"      : 0,
            "newFriendsCount"   : 0,
            "nickName"          : nickName,
            "userName"          : userName,
            }
    recordUserConfig(userConfDic2, "replace") # 强制更新的选项
    wechatLog.info("Login successfully as %s" % nickName)

def exitCallback():
    recordeStatus({"loginStatus":"exited"})
    recordUserConfig({"loginStatus":"exited"})
    wechatLog.info("exit successfully")


statusStorageDir = 'wechat.pkl'
itchat.auto_login(qrCallback=qrCallback, loginCallback=loginCallback, 
    exitCallback=exitCallback, hotReload=False, statusStorageDir=statusStorageDir)
itchat.run(debug = True)
