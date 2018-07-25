#! /usr/local/bin/python3
# -*- coding: utf-8 -*-
from .wechatConfig import *
import os, json, datetime, time


class Recorde():
    def __init__(self):
        pass

    def initSatatusFile(self, userKey=None):
        if not userKey: return self.statusFile
        self.userKey = userKey
        if not os.path.exists(STATUSDIR): os.makedirs(STATUSDIR)
        self.statusFile = STATUSDIR + '%s.json' % userKey
        return self.statusFile

    def initUserConfigFile(self, userName=None):
        if not userName: return self.userConfigFile
        self.userName = userName
        if not os.path.exists(USERCONFIG): os.makedirs(USERCONFIG)
        self.userConfigFile = USERCONFIG + '%s.json' % userName
        return self.userConfigFile


    def initQRcodePath(self, userKey):
        if not userKey: return None
        if not os.path.exists(QRPATH): os.makedirs(QRPATH)
        self.qrcodePath = QRPATH + '%s.png' % userKey
        return self.qrcodePath


    def recordUserConfig(self, keyValue, mothod="replace"):
        filename = self.userConfigFile
        if not isinstance(keyValue, dict): return None
        try:
            with open(filename, 'r+') as f: 
                old_dic = json.loads(f.read())
                for key, value in keyValue.items():
                    if mothod == "add":
                        old_dic[key] += value
                    else:
                        old_dic[key] = value
                f.seek(0)
                f.truncate()
                f.write(json.dumps(old_dic))
        except: #第一次记录文件
            with open(filename, 'w') as f:
                f.write(json.dumps(keyValue))


    def recordeStatus(self, keyValue):
        filename = self.statusFile
        if not isinstance(keyValue, dict): return None
        try:
            with open(filename, 'r+') as f: 
                old_dic = json.loads(f.read())
                for key, value in keyValue.items():
                    old_dic[key] = value
                f.seek(0)
                f.truncate()
                f.write(json.dumps(old_dic))
        except: #第一次记录文件
            with open(filename, 'w') as f:
                if "userKey" not in keyValue:
                    keyValue["userKey"] = self.userKey
                f.write(json.dumps(keyValue))

    def getUserConfig(self):
        filename = self.userConfigFile
        with open(filename, 'r+') as f: 
            userConfigDic = json.loads(f.read())
            return userConfigDic

    def relativePath(self, path, relate=ROOT):
        index = 0
        for i in path:
            if index > len(relate)-1: return path[index+1:]
            if i == relate[index]:
                index += 1
        return None
    def getCurDate(self):
        now = datetime.datetime.now()
        return now.strftime('%Y-%m-%d %H:%M:%S')
        
r = Recorde()
initSatatusFile = r.initSatatusFile
recordeStatus = r.recordeStatus
recordUserConfig = r.recordUserConfig
initQRcodePath = r.initQRcodePath
initUserConfigFile = r.initUserConfigFile
getUserConfig = r.getUserConfig
relativePath = r.relativePath
getCurDate = r.getCurDate
