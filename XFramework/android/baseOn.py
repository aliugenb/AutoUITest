# -*- coding:utf-8 -*-
import os
import sys
import time
from functools import wraps
import random
import re
import chardet
import types
from commandContainer import CommandContainer as CC


def strDecode(oIter):
    '''
    字串解码为unicode编码, 返回解码后的序列
    参数:
        list, dict
    '''
    if isinstance(oIter, dict):
        for key, value in oIter.items():
            if isinstance(value, str) and not isinstance(value, unicode):
                # 获取value的编码方式
                paraCode = chardet.detect(value)['encoding']
                nv = value.decode(paraCode)
                oIter[key] = nv
        return oIter
    else:
        count = 0
        for i in oIter:
            if isinstance(i, str) and not isinstance(i, unicode):
                paraCode = chardet.detect(i)['encoding']
                j = i.decode(paraCode)
                oIter[count] = j
            count += 1
        return oIter


def unifyParaCode(func):
    '''
    处理函数参数，将参数全部转化为unicode
    '''
    @wraps(func)
    def tempCheck(*args, **kwargs):
        rl = []
        rd = {}
        if args:
            tl = list(args)
            rl = strDecode(tl)
        if kwargs:
            rd = strDecode(kwargs)
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

    def new_floder(self, sdcard_path):
        """
        手机端新建文件夹,sdcard_path(手机路径)
        """
        command = '{} mkdir -p {}'.format(CC.PHONE_SHELL, sdcard_path)
        os.popen(command)

    def screencap(self, pic_name, sdcard_path):
        """
        屏幕截图.sdcard_path(手机路径),pic_name(图片名字)
        截图命名方式: 测试用例名_截图时间戳.png
        """
        command1 = '{} ls {}'.format(CC.PHONE_SHELL, sdcard_path)
        jPath = os.popen(command1).read()
        if jPath == '' or 'No such file or directory' in jPath:
            self.new_floder(sdcard_path)
        expression = re.compile(CC.SPECIAL_CHARACTER_LIST, re.U)
        pic_name = re.sub(expression, '-', pic_name)
        filename = '{}/{}.png'.format(sdcard_path, pic_name)
        command = '{} {}'.format(CC.PHONE_SCREENCAP, filename)
        os.popen(command)

    def get_had_ime(self):
        """
        获取已经安装的输入法的包名,返回包名/list
        """
        command = CC.GET_PHONE_HAD_IME
        r_info = os.popen(command)
        r_list = r_info.read().strip().split('\n')
        r_val = []
        for each in r_list:
            r_val.append(each.split('\r')[0])
        if r_val == ['']:
            self._LOGGER.warning(u'获取已下载的输入法存在问题')
        return r_val

    def get_current_ime(self):
        """
        获取当前输入法包名，返回包名/string
        """
        command = CC.GET_PHONE_CURRENT_IME
        r_info = os.popen(command)
        r_val = r_info.read().strip()
        if r_val == '':
            self._LOGGER.warning(u'获取当前的输入法存在问题')
        return r_val

    def set_ime(self, pkg='com.sohu.inputmethod.sogou.xiaomi/.SogouIME'):
        """
        设置输入法，有默认值
        """
        pkgList = self.get_had_ime()
        command = CC.SET_PHONE_IME
        for eachPkg in pkgList:
            if CC.APPIUM_IME_PKG in eachPkg:
                pkgList.remove(eachPkg)
        if pkg not in pkgList and pkg != CC.APPIUM_IME_PKG:
            command = '{} {}'.format(command, pkgList[0])
            os.popen(command)
        else:
            command = '{} {}'.format(command, pkg)
            os.popen(command)

    def set_input_text(self, text):
        '''
        adb输入法输入，暂时不支持中文
        '''
        command = CC.INPUT_TEXT + ' ' + str(text)
        os.popen(command)

    def getScreenSize(self):
        """
        获取屏幕分辨率，返回横纵坐标
        """
        command = CC.GET_SCREEN_SIZE
        posList = os.popen(command).read()
        if 'x' not in posList:
            self._LOGGER.critical(u'由于经费有限部分机型匹配可能有问题，出现此问题请钉钉联系我！')
            raise RuntimeError
        posList = posList.strip().split(': ')
        posList = posList[1].split('x')
        screenX = int(posList[0])
        screenY = int(posList[1])
        return screenX, screenY

    @classmethod
    def getDeviceName(cls):
        """
        获取手机名字
        """
        command = CC.GET_PHONE_NAME
        dn = os.popen(command).read().strip()
        if dn == '':
            cls._LOGGER.critical(u'获取手机名字失败')
            raise RuntimeError
        return dn

    @classmethod
    def getPlatformVersion(cls):
        """
        获取平台版本
        """
        command = CC.GET_PHONE_VERSION
        pv = os.popen(command).read().strip()
        if pv == '':
            cls._LOGGER.critical(u'获取平台版本失败')
            raise RuntimeError
        return pv

    def searchAppPro(self, pkgName=CC.XIMALAYA_PKG):
        comand = '{} {}'.format(CC.SEARCH_APP_PRO, pkgName)
        return os.popen(comand).read()

    def getProId(self, pkgName=CC.XIMALAYA_PKG):
        """获取某个应用的进程Id
        """
        originalVal = self.searchAppPro(pkgName)
        if originalVal:
            proList = originalVal.strip().split('\n')
            tempList = [i.strip().split(' ') for i in originalVal]
            # 除去嵌套列表中的空值
            [i.remove('') for i in tempList for j in range(i.count(''))]
            return [i[1] for i in tempList]
        else:
            print('警告:你输入的包名:{}，所代表的app没有运行'.format(pkgName))
            return []

    # def killAppPro(self, pkgName=CC.XIMALAYA_PKG):
    #     """
    #     杀掉指定apk进程
    #     """
    #     command = '{} {}'.format(CC.SEARCH_APP_PRO, pkgName)

    def clearApp(self, pkgName=CC.XIMALAYA_PKG, isAD=False):
        '''
        杀掉apk进程，并清理apk数据
        '''
        command1 = '{} {}'.format(CC.FORCE_STOP_APP, pkgName)
        command2 = '{} {}'.format(CC.CLEAR_APP_DATA, pkgName)
        if isAD:
            commands = [command1]
        else:
            commands = [command1, command2]
        map(lambda command: os.popen(command), commands)

    def startApp(self, ActivityName=CC.XIMALAYA_ACTIVITY):
        '''
        启动apk
        '''
        pkgName = ActivityName.split('/')[0]
        command = '{} {}'.format(CC.START_APP, ActivityName)
        if not self.searchAppPro(pkgName):
            os.popen(command)

    def pullFile(self, d_path, c_path):
        """
        把文件从手机推送到电脑,默认推送截图
        """
        command = '{} {} {}'.format(CC.PULLFILE_PHOHE_TO_COMPUTER,
                                    d_path,
                                    c_path)
        try:
            os.popen(command)
        except KeyError as e:
            raise ValueError(u'参数有问题,参数分别为d_path=XXX和c_path=XXX，请核对')

    def pressBack(self):
        """
        返回键
        """
        command = '{} 4'.format(CC.PHONE_KEYEVENT)
        os.popen(command)
        time.sleep(1)

    def pressMenu(self):
        '''
        菜单键
        '''
        command = '{} 82'.format(CC.PHONE_KEYEVENT)
        os.popen(command)
        time.sleep(1)

    def pressHome(self):
        """
        回主界面
        """
        command = '{} 3'.format(CC.PHONE_KEYEVENT)
        os.popen(command)
        time.sleep(1)

    def getRandomNum(self):
        '''
        默认获取一个两位数的随机数
        '''
        randomNum = random.randint(0, 99)
        if len(str(randomNum)) == 1:
            randomNum = '0' + str(randomNum)
        elif len(str(randomNum)) == 2:
            randomNum = str(randomNum)
        else:
            print(u'随机数长度不符合要求')
        return randomNum

    def get_file_list(self, file_name):
        """
        读取文件，返回列表
        """
        try:
            with open(file_name, 'r') as m:
                lines = m.readlines()
                r_lines = []
                for line in lines:
                    r_lines.append(line.strip())
        except IOError as e:
            self._LOGGER.critical(u'File error: {}'.format(str()))
        return r_lines

    def clearAllAppointEl(self, pendingList, el):
        '''
        删除列表中所有指定的元素
        '''
        if not isinstance(pendingList, list):
            self._LOGGER.critical(u'错误: 输入参数不为列表')
            raise TypeError
        list_copy = pendingList
        for i in pendingList:
            if i == el:
                list_copy.remove(i)
        return list_copy

    def isOrNotEqual(self, valueLeft, valueRight):
        '''
        判断传入的两个字串是否相等
        '''
        valueLeft = str(valueLeft)
        valueRight = str(valueRight)
        if valueLeft == valueRight:
            self._LOGGER.debug(u'两个值相等，两个值分别为: {}, {}'.format(valueLeft,
                                                              valueRight))
        else:
            self._LOGGER.debug(u'两个值不等，两个值分别为: {}, {}'.format(valueLeft,
                                                              valueRight))

    def appiumErrorHandle(self):
        command1 = CC.KILL_ADB
        command2 = CC.START_ADB
        os.popen(command1)
        time.sleep(1)
        os.popen(command2)
        time.sleep(5)

    def getScreenDetail(self):
        command = CC.GET_SCREEN_DETAIL
        tempData = os.popen(command).read()
        pendingList = tempData.strip().split('\n')
        infoDict = {}
        needList = []
        for each in pendingList:
            if 'app=' in each:
                needList = each.strip().split(' ')
        for el in needList:
            if '=' in el:
                val = el.strip().split('=')
                infoDict[val[0]] = val[1]
            else:
                val = el.strip().split('dpi')
                infoDict['density'] = val[0]
        return infoDict

    # def getScriptInfo(self):
    #     '''
    #     获取调用
    #     '''
