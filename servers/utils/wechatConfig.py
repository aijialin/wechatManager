#! /usr/local/bin/python3
# -*- coding: utf-8 -*-
import os

ROOT			= os.getcwd() 
STATUSDIR		= ROOT + '/status/'
LOGPATH			= ROOT + '/logs/'
MYFIFO			= ROOT + '/myfifo'
DOWNLOAD		= ROOT + '/download/'
RECEIVEFILES	= DOWNLOAD + 'receiveFiles/'
QRPATH			= DOWNLOAD + 'QR/'
USERCONFIG		= ROOT + '/config/'
RELOAD			= ROOT + '/'


DEFAULTREPLYCONTENT = u"您好|我现在有事不在，一会再和您联系。"
DEFAULTVERIFYCONTENT = u"您好|感谢添加好友"




