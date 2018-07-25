#! /usr/local/bin/python3
# -*- coding: utf-8 -*-
# 
import requests
from ..itchat.content import *
from ..itchat import send
from ..wechatRecord import *

KEY = '60545a559b56449a98280181f505d1fe'
def response(msg, userName):
    if msg['Type'] in [SYSTEM, FRIENDS, NOTE]: return #不回复此类消息
    if msg["FromUserName"] == userName: return #不回复自己发送的消息
    apiUrl = 'http://www.tuling123.com/openapi/api'
    data = {
        'key'    : KEY,
        'info'   : msg["Text"],
        'userid' : 'wechat-robot',
    }
    try:
        r = requests.post(apiUrl, data=data).json()
        send(r.get('text'), msg["FromUserName"])
        recordUserConfig({"sendMsgCount" : 1}, "add") #发送消息数加一
        return
    except:
        return