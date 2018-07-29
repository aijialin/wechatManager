#! /usr/local/bin/python3
# -*- coding: utf-8 -*-
import json, time, hashlib, random, threading, subprocess, os, shlex, sys

import traceback
from servers.utils.wechatConfig import *
from servers.utils.wechatLog import wechatLog
from servers.utils.wechatRecord import *

def wechat_start(data=None):
    wechatLog.info("wechat_start data=%s" % data)
    ret = {'ret':0, 'msg':'success'}

    userKey = getUserKey() # 生成用户唯一key
    wechatLog.info(userKey)
    #开始启动进程去处理业务 使用跨平台的多进程库subprocess
    PYTHON = sys.executable
    shell_cmd = '"%s" -m servers.wechatProcess %s' % (PYTHON, userKey) #let servers be a package
    wechatLog.debug(shell_cmd)
    cmd = shlex.split(shell_cmd)
    try:
        child = subprocess.Popen(args=cmd, shell=False)
    except:
        wechatLog.info("server error userKey = " + userKey)
        wechatLog.info(traceback.format_exc())
        ret['ret'] = -3;
        ret['msg'] = 'server error'
        return json.dumps(ret)

    ret["loginStatus"] = "Loading the QR code, wait..."
    ret["userKey"] = userKey
    return json.dumps(ret)
    
#牺牲并发性，采用长轮询的方式去获取，hold住请求， 如果有新数据才返回
def wechat_checkStatus_old(userKey=None):
    '''
    desc:检测二维码的状态，是否扫描，是否确认登录，是否超时
    parameter:None
    return {ret:0, state:}
    '''
    ret = {'ret':0, 'msg':'success'}
    if not userKey:
        ret['ret'] = -1
        ret["loginStatus"] = "not init"
        ret['msg'] = 'userKey is empty'
        return json.dumps(ret)
    if isinstance(userKey, bytes): userKey = userKey.decode('utf-8')
    statusFile = initSatatusFile(userKey)
    try:
        with open(statusFile, 'r') as fd:
            data = fd.read()
            return data
    except:
        #wechatLog.info(traceback.format_exc())
        ret['ret'] = -2
        ret["loginStatus"] = "Loading the QR code, wait..."
        ret['msg'] = 'check again'
        return json.dumps(ret)

def wechat_checkStatus(transdata=None):
    '''
    desc:检测二维码的状态，是否扫描，是否确认登录，是否超时
    parameter:None
    return {ret:0, state:}
    {
        1: getting qrcode
        2: scan QRcode
        3: confirm 
        4: load contact
        5: success
        100: 超时
        101: 失败
        负数: 参数错误
    }
    '''
    ret = {'ret':0, 'msg':'success'}
    try:
        transdata = json.loads(transdata)
    except:
        ret['ret'] = -1
        ret["loginStatus"] = "wrong pragma"
        ret['msg'] = 'wrong pragma'
        return json.dumps(ret)

    wechatLog.debug(json.dumps(transdata))
    maxRequestTime = 5 #一次请求最长时间为5秒
    userKey = transdata["userKey"]
    loginCode = transdata["loginCode"] #当前登陆阶段
   
    if not userKey:
        ret['ret'] = -2
        ret["loginStatus"] = "not init"
        ret['msg'] = 'userKey is empty'
        ret['loginCode'] = -1
        return json.dumps(ret)
    if isinstance(userKey, bytes): userKey = userKey.decode('utf-8')
    statusFile = initSatatusFile(userKey)

    while not os.path.exists(statusFile) and maxRequestTime > 0:
        time.sleep(0.2)
        maxRequestTime -= 0.2

    if maxRequestTime <= 0:
        ret['ret'] = 1
        ret["loginStatus"] = "Loading the QR code, wait..."
        ret['msg'] = 'check again'
        ret['loginCode'] = 1
        return json.dumps(ret)

    while maxRequestTime > 0:
        try:
            with open(statusFile, 'r') as fd:
                data = fd.read()
                dataDic = json.loads(data)
                if dataDic["loginCode"] != loginCode:
                    return json.dumps(dataDic)
                else:
                    time.sleep(0.2)
                    maxRequestTime -= 0.2
        except:
            wechatLog.info(traceback.format_exc())
            ret['ret'] = -5
            ret["loginStatus"] = "Please refresh the page..."
            ret['loginCode'] = -1
            ret['msg'] = 'server error'
            return json.dumps(ret)

    #wechatLog.info(traceback.format_exc())
    ret['ret'] = 0
    ret['loginCode'] = loginCode
    ret['msg'] = 'try again'
    return json.dumps(ret)


def getUserKey():
    ran = random.random()
    tim = time.time()
    rankey = (str(ran) + str(tim)).encode('utf-8')
    key = hashlib.md5(rankey)
    return key.hexdigest()


def wechat_getUserConfig(nickeName):
    ret = {'ret':0, 'msg':'success'}
    if nickeName == None:
        ret["ret"] = -1
        ret["msg"] = "nickeName is empty"
        return json.dumps(ret)
    if isinstance(nickeName, bytes): nickeName = nickeName.decode('utf-8')
    userConfigFile = initUserConfigFile(nickeName)
    wechatLog.debug(userConfigFile)

    if not os.path.exists(userConfigFile):
        ret["ret"] = -2
        ret["msg"] = "userConfigFile is undefined"
        return json.dumps(ret)
    try:
        with open(userConfigFile, 'r') as fd:
            data = fd.read()
            return data
    except:
        ret["ret"] = -3
        ret["msg"] = "userConfigFile is error"
        return json.dumps(ret)

def wechat_changeUserConfig(keyValue):
    ret = {'ret':0, 'msg':'success'}
    if keyValue == None:
        ret["ret"] = -2
        ret["msg"] = "keyValue is empty"
        return json.dumps(ret)
    if isinstance(keyValue, bytes): keyValue = keyValue.decode('utf-8')
    confDic = json.loads(keyValue)
    userConfigFile = initUserConfigFile(confDic["nickName"])

    try:
        recordUserConfig(confDic)
        ret["ret"] = 0
        ret["msg"] = "success"
        return json.dumps(ret)
    except:
        wechatLog.info(traceback.format_exc())
        ret["ret"] = -3
        ret["msg"] = "error"
        return json.dumps(ret)



def waitSubProcess(): #linux下需要回收子进程
    while True:
        time.sleep(0.5)
        try:
            os.waitpid(-1, os.WNOHANG) #回收子进程 非阻塞
        except:
            continue

t = threading.Thread(target=waitSubProcess, name='waitSubProcess')
t.start()
