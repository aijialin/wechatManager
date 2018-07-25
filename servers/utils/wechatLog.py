#! /usr/local/bin/python3
# -*- coding: utf-8 -*-
import logging, json, os
from .wechatConfig import *
'''
    所有的文件都采用本类的实例对象
    打印时间 文件名 函数名 第几行以及自定义等信息
    同时显示在控制台和保存文件中
'''

class LogSystem(object):
    __showOnCmd = True
    __loggingFile = LOGPATH + 'wechat.log'
    __loggingLevel = logging.DEBUG
    __formatter = logging.Formatter('[%(asctime)s] %(pathname)s %(lineno)s %(funcName)s [%(levelname)s] msg:%(message)s %(threadName)s-%(thread)d pid:%(process)d', '%Y-%m-%d %H:%M:%S')
    __str_handle = logging.StreamHandler()
    if not os.path.exists(LOGPATH):
        os.makedirs(LOGPATH)
    __file_handle = logging.FileHandler(filename = __loggingFile, mode='a', encoding=None, delay=False)
    
    def __init__(self):
        self.userKey = None
        self.Logger = logging.getLogger('wechat')
        self.Logger.setLevel(logging.DEBUG)

        self.__str_handle.setFormatter(self.__formatter)
        self.__str_handle.setLevel(logging.DEBUG)
        self.Logger.addHandler(self.__str_handle)

        self.__file_handle.setFormatter(self.__formatter)
        self.__file_handle.setLevel(logging.INFO)
        self.Logger.addHandler(self.__file_handle)

        self.debug = self.Logger.debug
        self.info = self.Logger.info
        self.warning = self.Logger.warning
        self.error = self.Logger.warning

    def set_logging(self, showOnCmd=True, loggingFile=None, loggingLevel=None):
        if showOnCmd != self.__showOnCmd:
            if showOnCmd:
                self.Logger.addHandler(self.__str_handle)
            else:
                self.Logger.removeHandler(self.cmdHandler)
            self.__showOnCmd = showOnCmd

        if loggingFile != None:
            if self.__loggingFile != loggingFile and self.__loggingFile is not None: # clear old fileHandler
                self.Logger.removeHandler(self.__file_handle)
                self.__file_handle.close()

                self.__file_handle = logging.FileHandler(loggingFile)
                self.__file_handle.setFormatter(self.__formatter)
                self.Logger.addHandler(self.__file_handle)
        if loggingLevel != None:      
            if loggingLevel != self.__loggingLevel:
                self.Logger.setLevel(loggingLevel)
                self.__loggingLevel = loggingLevel


wechatLog = LogSystem()
set_logging = wechatLog.set_logging



