#! /usr/local/bin/python3
# -*- coding: utf-8 -*-
import re, time, os
from servers.vendor.itchat.content import *
from servers.vendor.itchat import send
from servers.vendor.itchat import search_friends

from servers.utils.wechatLog import *
from servers.utils.wechatRecord import *


class Revoke():
    timeout = 130.0 #设置最长消息保留时间， 超时将被清理
    msg = None #当前收到消息
    revokeFlag = [u'\u64a4\u56de\u4e86\u4e00\u6761\u6d88\u606f', 'recalled a message'] #撤回了一条消息
    msgLibrayDic = {} #所有消息记录

    def saveMessage(self, msg, userConfig):
        self.msg = msg
        userName = userConfig["userName"]
        if msg['Type'] in [SYSTEM, NOTE]: return #不保存此类消息
        if msg['ToUserName'] == userName: #如果消息接受者是自己
            recordUserConfig({"recMsgCount" : 1}, "count") #接受消息数加一
        elif msg["FromUserName"] == userName: #如果发送消息是自己
            recordUserConfig({"sendMsgCount" : 1}, "count") #发送消息数加一
            return #不保存自己发送的消息
        msgId = msg['MsgId']
        msgFromUserId = msg['FromUserName']
        msgFromNick = search_friends(userName=msgFromUserId)['NickName']
        msgCreateTime = msg['CreateTime']
        msgCreateTime_t = self.timeTodate(msgCreateTime)

        if msg['Type'] in [PICTURE, RECORDING, ATTACHMENT, VIDEO]:
            if not os.path.exists(RECEIVEFILES): os.makedirs(RECEIVEFILES)
            msgContent = RECEIVEFILES + msg.fileName
            msg.download(msgContent)
        elif msg['Type'] in [SHARING]:
            msgContent = msg['Text'] + '\t' + msg['Url']
        elif msg['Type'] in [MAP]:
            x, y, location = re.search("<location x=\"(.*?)\" y=\"(.*?)\".*label=\"(.*?)\".*", msg['OriContent']).group(1,2,3)
            #msg_content = u"纬度->" + str(x) + " 经度->" + str(y) + " " + location
            msgContent = location
        elif msg['Type'] in [CARD]:
            msgContent = msg['RecommendInfo']['NickName'] + u' 的名片'
        else:
            msgContent = msg['Text']

        self.msgLibrayDic.update({
            msgId: {
                "msgFromUserId"     : msgFromUserId,
                "msgFromNick"       : msgFromNick,
                "msgCreateTime"     : msgCreateTime, 
                "msgCreateTime_t"   : msgCreateTime_t, 
                "msgType"           : msg['Type'],
                "msgContent"        : msgContent}
                })
        self.clearTimeoutMsg()

    def isRevokeType(self):
        if self.msg['Type'] != 'Note': return False
        ret = 0
        for i in self.revokeFlag:
            ret += self.msg['Content'].find(i)
        if ret == -2:  return False
        return True

    def response(self, toUserName=None):
        if not self.isRevokeType(): return
        msgId = re.search(r'\<msgid\>(.+?)\<\/msgid\>', self.msg['Content']).group(1)
        msgRecorded = self.msgLibrayDic.get(msgId, None)
        if not msgRecorded: return
        explainInfo = u"%s %s 撤回了一条%s消息" % (msgRecorded["msgCreateTime_t"], msgRecorded["msgFromNick"], msgRecorded["msgType"])
        toUserName = toUserName or msgRecorded['msgFromUserId']
        send(explainInfo, toUserName)
        if msgRecorded['msgType'] in [PICTURE, RECORDING, ATTACHMENT, VIDEO]:
            send('@%s@%s' % 
                ('img' if msgRecorded['msgType'] == 'Picture' else 'fil', msgRecorded['msgContent']), 
                toUserName
                )
            os.remove(msgRecorded['msgContent'])
        elif msgRecorded['msgType'] in [TEXT, MAP, CARD, SHARING]:
            send(msgRecorded['msgContent'], toUserName = toUserName or msgRecorded['msgFromUserId'])

        item = self.msgLibrayDic.pop(msgId)
        wechatLog.debug(u'already return: ' + item['msgContent'])
        self.clearTimeoutMsg()
        return None

    def clearTimeoutMsg(self):
        if not self.msgLibrayDic: return
        #字典在遍历的时候无法修改,RuntimeError: dictionary changed size during iteration
        for msgId in list(self.msgLibrayDic): 
            if time.time() - self.msgLibrayDic[msgId]['msgCreateTime'] > self.timeout: #time out
                item = self.msgLibrayDic.pop(msgId)
                wechatLog.debug(u'time out msg: ' + item['msgContent'])
                if item['msgType'] in [PICTURE, RECORDING, ATTACHMENT, VIDEO]:
                    wechatLog.debug(u'need to delete file: ' + item['msgContent'])
                    os.remove(item['msgContent'])

    def timeTodate(self, timeStamp):
        timeObj = time.localtime(timeStamp)
        readTime = time.strftime("%Y-%m-%d %H:%M:%S", timeObj)
        return readTime



revoke = Revoke()

