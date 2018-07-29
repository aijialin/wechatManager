#! /usr/local/bin/python3
# -*- coding: utf-8 -*-
# 
import os, datetime, time, re

from servers.utils.wechatRecord import *

from servers.vendor.itchat import config
from servers.vendor.itchat.components.login import process_login_info
from servers.vendor.itchat.core import Core



def checkLogin(self, uuid=None):
    uuid = uuid or self.uuid
    url = '%s/cgi-bin/mmwebwx-bin/login' % config.BASE_URL
    localTime = int(time.time())
    params = 'loginicon=true&uuid=%s&tip=1&r=%s&_=%s' % (
    uuid, int(-localTime / 1579), localTime)
    headers = { 'User-Agent' : config.USER_AGENT }
    r = self.s.get(url, params=params, headers=headers)
    regx = r'window.code=(\d+)'
    regxForHeadImg = r"window.code=201;window.userAvatar = '(\S+)';"
    data = re.search(regx, r.text)
    if data and data.group(1) == '200':
        if process_login_info(self, r.text):
            return '200'
        else:
            return '400'
    elif data:
        if data.group(1) == '201': #get head img
            headImg = re.search(regxForHeadImg, r.text).group(1)
            recordeStatus({"headImg":headImg})
        return data.group(1)
    else:
        return '400'


Core.check_login = checkLogin #替换掉itchat的check_login
