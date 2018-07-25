#! /usr/local/bin/python3
# -*- coding: utf-8 -*-
import json, time, hashlib, random, threading, subprocess, os, shlex, sys

import traceback
from .utils.wechatConfig import *
from .utils.wechatLog import *
from .utils.wechatRecord import *

def wechat_start(data=None):
    wechatLog.info("wechat_start data=%s" % data)
    ret = {'ret':0, 'msg':'success'}

    userKey = getUserKey() # 生成用户唯一key
    wechatLog.info(userKey)
    #开始启动进程去处理业务 使用跨平台的多进程库subprocess
    PYTHON = sys.executable
    shell_cmd = '%s servers/wechatProcess.py %s' % (PYTHON, userKey)
    cmd = shlex.split(shell_cmd)
    try:
        child = subprocess.Popen(args=cmd, shell=False)
    except:
        wechatLog.info("server error userKey = " + userKey)
        wechatLog.info(traceback.format_exc())
        ret['ret'] = -3;
        ret['msg'] = 'server error'
        return json.dumps(ret)
    statusFile = initSatatusFile(userKey)
    while not os.path.exists(statusFile): 
        #wechatLog.info("%s not found" % statusFile)
        continue
    try:
        with open(statusFile, 'r') as fd:
            retData = fd.read()
            wechatLog.info('read = %s' % retData)
            retList = json.loads(retData)
            retList['ret'] = 0
            retData = json.dumps(retList)
            return retData
    except:
        wechatLog.info("server error userKey = " + userKey)
        wechatLog.info(traceback.format_exc())
        ret['ret'] = -4;
        ret['msg'] = 'server error'
        return json.dumps(ret)


def wechat_checkStatus(userKey=None):
    '''
    desc:检测二维码的状态，是否扫描，是否确认登录，是否超时
    parameter:None
    return {ret:0, state:}
    '''
    ret = {'ret':0, 'msg':'success'}
    if not userKey:
        ret['ret'] = -1
        ret['msg'] = 'userKey is empty'
        return json.dumps(ret)
    if isinstance(userKey, bytes): userKey = userKey.decode('utf-8')
    statusFile = initSatatusFile(userKey)
    try:
        with open(statusFile, 'r') as fd:
            data = fd.read()
            return data
    except:
        print(traceback.format_exc())
        ret['ret'] = -2
        ret['msg'] = 'userKey is wrong'
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
    print(userConfigFile)

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
