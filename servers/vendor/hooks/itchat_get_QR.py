#! /usr/local/bin/python3
# -*- coding: utf-8 -*-
# 
import requests, io

from servers.utils.wechatLog import *

from servers.vendor.itchat import config
from servers.vendor.itchat.core import Core
from servers.vendor.itchat import utils


def get_qrcode(uuid=None):
    url = '%s/qrcode/%s' % (config.BASE_URL, uuid)
    headers = { 'User-Agent' : config.USER_AGENT }
    try:
        r = requests.Session().get(url, stream=True, headers=headers)
    except:
        wechatLog.info('get_qrcode error')
        return None
    qrStorage = io.BytesIO(r.content)
    return qrStorage

def get_QR(self, uuid=None, enableCmdQR=False, picDir=None, qrCallback=None):
    uuid = uuid or self.uuid
    picDir = picDir or config.DEFAULT_QR
    '''
    qrStorage = io.BytesIO()
    qrCode = QRCode('https://login.weixin.qq.com/l/' + uuid)
    qrCode.png(qrStorage, scale=10)
    '''
    qrStorage = get_qrcode(uuid)

    if hasattr(qrCallback, '__call__'):
        qrCallback(uuid=uuid, status='0', qrcode=qrStorage.getvalue())
    else:
        with open(picDir, 'wb') as f:
            f.write(qrStorage.getvalue())
        if enableCmdQR:
            utils.print_cmd_qr(qrCode.text(1), enableCmdQR=enableCmdQR)
        else:
            utils.print_qr(picDir)
    return qrStorage


Core.get_QR = get_QR #替换掉itchat的check_login