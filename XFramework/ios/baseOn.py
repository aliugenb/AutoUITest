# -*- coding:utf-8 -*-
import os
import sys
import time
import random
import re
import chardet
import types
from commandContainer import CommandContainer as CC


def getStrEncode(oStr):
    '''
    获取字串编码方式, 返回编码方式
    参数:
        str
    '''
    codeMode = chardet.detect(oStr)['encoding']
    return codeMode


def strDecode(oIter):
    '''
    字串解码为unicode编码, 返回解码后的序列
    参数:
        list, dict
    '''
    if isinstance(oIter, dict):
        for key, value in oIter.items():
            if isinstance(value, str) and not isinstance(value, unicode):
                paraCode = getStrEncode(value)
                nv = value.decode(paraCode)
                oIter[key] = nv
        return oIter
    else:
        count = 0
        for i in oIter:
            if isinstance(i, str) and not isinstance(i, unicode):
                paraCode = getStrEncode(i)
                j = i.decode(paraCode)
                oIter[count] = j
            count += 1
        return oIter


def unifyParaCode(func):
    '''
    处理函数参数，将参数全部转化为unicode
    '''
    def tempCheck(*args, **kwargs):
        rl = []
        rd = {}
        if args:
            tl = list(args)
            rl = strDecode(tl)
        if kwargs:
            rd = strDecode(kwargs)
        # print('%s is begin' % func.__name__)
        if rl and not rd:
            return func(*rl)
        elif not rl and rd:
            return func(**rd)
        elif rl and rd:
            return func(*rl, **rd)
        else:
            return func()
    return tempCheck


class BaseOn(object):
    """
    基本操作方法
    """

  
    def getPhoneUdid():
        cmd = CC.PHONE_UDID
        phoneUdid = os.popen(cmd).read().strip()
        #print len(phoneUdid)
        return phoneUdid

    def getPlatformVersionIos():
        cmd = CC.PLATFORM_VERSION
        platformVersion = os.popen(cmd).read().strip()
        return  platformVersion

    def getPhoneNameIos():
        cmd = CC.PHONE_NAME
        phoneName = os.popen(cmd).read().strip()
        return phoneName

   
    
    '''
    def clearApp(self, pkgName=CC.XIMALAYA_PKG, isAD=False):
       # 杀掉apk进程，并清理apk数据
        command1 = '{} {}'.format(CC.FORCE_STOP_APP, pkgName)
        command2 = '{} {}'.format(CC.CLEAR_APP_DATA, pkgName)
        if isAD:
            commands = [command1]
        else:
            commands = [command1, command2]
        map(lambda command: os.popen(command), commands)
    '''
    
    def startApp(self, pkgName=CC.XIMALAYA_PKG):
        '''
        启动apk
        '''
        cmd =  'idevicedebug run '+ CC.PHONE_NAME        
        os.popen(cmd).read().strip()
        
'''
    def clearAllAppointEl(self, pendingList, el):
        # 删除列表中所有指定的元素
        if not isinstance(pendingList, list):
            self._LOGGER.critical(u'错误: 输入参数不为列表')
            raise TypeError
        list_copy = pendingList
        for i in pendingList:
            if i == el:
                list_copy.remove(i)
        return list_copy
    
    def appiumErrorHandle(self):        
          # 模拟手工插拔设备               
        command1 = CC.KILL_ADB
        command2 = CC.START_ADB
        os.popen(command1)
        time.sleep(1)
        os.popen(command2)
        time.sleep(5)   
    '''