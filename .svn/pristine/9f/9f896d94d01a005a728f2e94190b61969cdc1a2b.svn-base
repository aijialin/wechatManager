#! /usr/local/bin/python3
# -*- coding: utf-8 -*-
# 

import time, json, sys, os

from utils.funcs import jokeReply
from utils.funcs import busyReply
from utils.funcs import verifyReply
from utils.funcs.banRevoke import recoke
from utils.funcs import hooks

from utils.wechatConfig import *
from utils.wechatLog import *
from utils.wechatRecord import *

import utils.itchat as itchat
from utils.itchat.content import *

lastModifyTime = "" #上一次修改用户配置文件的时间
userConfig = {}


wechatLog.info(json.dumps(sys.argv))
userKey = sys.argv[1]
wechatLog.info("userKey = %s" % userKey)
if userKey == None:
    wechatLog.info('userKey None')
    sys.exit()

#userKey = str(time.time())
initSatatusFile(userKey) #初始化运行日志文件写入{usrKey}
qrcodePath = initQRcodePath(userKey)

def checkAndUpdateConfig():
    global userConfig, lastModifyTime
    userConfigFile = initUserConfigFile()
    testTime = time.ctime(os.path.getmtime(userConfigFile))
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

    if userConfig["verifySwitch"]: verifyReply.response(userConfig["verifyContent"], msg)
    if userConfig["banRevokeSwitch"]: recoke.response(userConfig["revokeMsgToUser"])
    if userConfig["jokeSwitch"]: return jokeReply.response(msg, userName)
    if userConfig["busySwitch"]: return busyReply.response(userConfig["busyContent"], msg, userName)



def qrCallback(uuid, status, qrcode):
    #wechatLog.info("status=%s\tuuid = %s" % (status, uuid))
    if status=='0' and qrcode:    
        wechatLog.info("Please scan the QR code to log in")
        with open(qrcodePath, 'wb') as f:
            f.write(qrcode)
        recordeStatus({"loginStatus":"Please scan the QR code to log in", "uuid":uuid, "qrcode":relativePath(qrcodePath)})
        #itchat.utils.print_qr(qrcodePath)
        return
    if status == '201':
        recordeStatus({"loginStatus":"Please press confirm on your phone"})
        wechatLog.info("confirm on phone")
        return
    if status == '200':
        recordeStatus({"loginStatus":"Loading the contact, this may take a little while"})
        wechatLog.info("load contact")
        return
    if status != '408':
        recordeStatus({"loginStatus":"Log in time out, reloading QR code"})
        wechatLog.info("Log in time out, reloading QR code.")
        return
        

def loginCallback():
    nickName = itchat.originInstance.storageClass.nickName
    userName = itchat.originInstance.storageClass.userName
    recordeStatus({"loginStatus":"Login successfully as %s" % nickName})
    initUserConfigFile(nickName)
    userConfDic = {
            "loginStatus"       : "success",
            "loginTime"         : getCurDate(),
            "friendsCount"      : len(itchat.originInstance.storageClass.memberList),
            "recMsgCount"       : 0,
            "sendMsgCount"      : 0,
            "newFriendsCount"   : 0,
            "busyContent"       : DEFAULTREPLYCONTENT, 
            "verifyContent"     : DEFAULTVERIFYCONTENT,
            "jokeSwitch"        : True,
            "busySwitch"        : False,
            "verifySwitch"      : True,
            "banRevokeSwitch"   : False,
            "revokeMsgToUser"   : "",
            "nickName"          : nickName,
            "userName"          : userName,
            }
    recordUserConfig(userConfDic)
    wechatLog.info("Login successfully as %s" % nickName)

def exitCallback():
    recordeStatus({"loginStatus":"exited"})
    recordUserConfig({"loginStatus":"exited"})
    wechatLog.info("exit successfully")


statusStorageDir = 'wechat.pkl'
itchat.auto_login(qrCallback=qrCallback, loginCallback=loginCallback, 
    exitCallback=exitCallback, hotReload=False, statusStorageDir=statusStorageDir)
itchat.run(debug = True)
