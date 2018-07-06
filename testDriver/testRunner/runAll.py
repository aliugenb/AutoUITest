# -*- coding:utf-8 -*-
import os
import sys
import re
import xlrd
import shutil
import json
import time
from functools import wraps
import common
common.pathGet()
from XFramework.android.baseOn import BaseOn as androidBO
from XFramework.android.uiBase import UITest as androidUT
import XFramework.android.TestRunner as androidTR
# from XFramework.ios.baseOn import BaseOn as iosBO
# from XFramework.ios.uiBase import UITest as iosUT
# import XFramework.ios.TestRunner as iosTR
from XFramework.parseExcel import caseDataTransform as cdt
import XFramework.logger.logger as LG


def getTestPreconditon(casePath):
    fileName = ''
    srcImgName = ''
    targetImgField = ''
    targetImgZip = ''
    targetImgSuit = ''
    files = os.listdir(casePath)
    for eachFile in files:
        suffixType = '.{}'.format(eachFile.split('.')[-1])
        if suffixType in cdt.EXCEL_TYPE and '~$' not in eachFile:
                fileName = eachFile
        if suffixType in cdt.IMG_TYPE and 'bg_temp' not in eachFile:
            srcImgName = eachFile
        if os.path.isdir(os.path.join(casePath, eachFile)):
            targetImgField = eachFile
        if suffixType in cdt.COMPRESSED_FILES_TYPE:
            targetImgZip = eachFile
    targetImgSuit = targetImgField if targetImgField else targetImgZip
    if fileName == '':
        print('当前目录未找到测试用例！')
        raise IOError
    return fileName, srcImgName, targetImgSuit


def getCaseInfo(fileName):
    '''
    只能用于获取父级目录文件
    '''
    casePath = '{}{}{}'.format(os.pardir, os.sep, fileName)
    caseName, srcImgName, targetImgSuit = getTestPreconditon(casePath)
    return casePath, caseName, srcImgName, targetImgSuit


def sheetNotExistwarning(getCaseInfo):
    @wraps(getCaseInfo)
    def outerFunc(func):
        def tempFunc(listPath):
            casePath, caseName, _, _ = getCaseInfo('testCase')
            allTestList = func(listPath)
            data_xls = xlrd.open_workbook(os.path.join(casePath, caseName))
            sheetList = []
            realList = [i for i in allTestList]
            for index, sheet in enumerate(data_xls.sheets()):
                sheetList.append(sheet.name)
            for each in allTestList:
                if each not in sheetList and each != '':
                    print('警告: 你勾选的{}大类，在测试表格中不存在，已经自动帮你过滤。'
                          .format(each))
                    realList.remove(each)
            return realList
        return tempFunc
    return outerFunc


@sheetNotExistwarning(getCaseInfo)
def getTestClass(listPath):
    allTestList = []
    with open(listPath, 'r') as f:
        lines = f.readlines()
        for line in lines:
            allTestList.append(line.strip())
    if allTestList == []:
        print('请确认是否勾选测试类！')
        raise ValueError
    return allTestList


def getRealTestClass(allTestClass):
    """区分主app和广告业务
    """
    if not isinstance(allTestClass, list):
        print('错误的参数：{}，期望的参数类型为列表'.format(allTestClass))
        sys.exit(1)
    tempList = []
    for el in allTestClass:
        if isinstance(el, dict):
            if el.get('testCaseName') == 'ad':
                tempList.append(el)
        else:
            print('列表参数：{}，中所有的元素类型都应该是字典'.format(allTestClass))
            sys.exit(1)
    if len(tempList) == 1:
        return tempList
    elif len(tempList) == 0:
        return allTestClass
    else:
        print('获取测试大类失败, 判断参数为：{}，请确认'.format(tempList))
        sys.exit(1)


def getConfigPara(configPath):
    configDict = {}
    with open(configPath, 'r') as f:
        tempDict = json.load(f)
    if 'Android' in tempDict:
        configDict = tempDict['Android']
    elif 'IOS' in tempDict:
        configDict = tempDict['IOS']
    else:
        raise ValueError('平台参数配置错误，退出测试！')
    if configDict == {}:
        raise ValueError('参数配置错误，退出测试！')
    return configDict


def getImgDict(casePath, targetImgSuit, srcImgName):
    """获取图片参数集合
    """
    imgDict = {}
    if srcImgName != '' and targetImgSuit != '':
        # 获取手机屏幕详情
        infoDict = androidTR.getScreenDetail()
        rx, ry = [int(i) for i in infoDict.get('app').split('x')]
        # 解压测试图片所属压缩文件
        if '.' in targetImgSuit:
            cdt.unzipFile(casePath, targetImgSuit)
            # 获取解压后的测试图片文件目录
            testImgPathName = cdt.getFileNameWithoutSuffix(targetImgSuit)
        else:
            testImgPathName = targetImgSuit
        testImgPath = os.path.join(casePath, testImgPathName)
        # 获取源图片尺寸
        srcImgSize = androidTR.getImgSize(os.path.join(casePath,
                                                       srcImgName))
        # 获取自适配系数
        kx1, ky1 = androidTR.adaptiveCoefficient(infoDict, srcImgName)
        # 获取图片比例相关系数
        kx2, ky2 = androidTR.getCorrelationCoefficients(srcImgSize,
                                                        (rx, ry),
                                                        (kx1, ky1))
        # 图片所需参数集合
        imgDict = {'testImgPath': testImgPath,
                   'testImgPathName': testImgPathName,
                   'srcImgSize': srcImgSize,
                   'srcImgName': srcImgName,
                   'acPara': (kx1, ky1),
                   'ccPara': (kx2, ky2),
                   'realSrcImgName': cdt.getFileNameWithoutSuffix(srcImgName),
                   'srcImgPath': casePath,
                   'screenDetail': infoDict}
    else:
        print("警告: 测试图片压缩文件和源图片未同时存在于上传文件中，默认你未使用图片点击功能！")
    return imgDict


def envInit():
    """清除手机中上次测试遗留的内容
    """
    os.popen('adb shell rm -rf sdcard/AutoTest/screencap')
    os.popen('adb shell rm -rf sdcard/AutoTest/screenrecord')
    if re.match('^win', sys.platform):
        os.popen('rd /q {}'.format(os.path.join(os.pardir,
                                                'testLOG',
                                                'androidLog')))
        os.popen('del /q {}'.format(os.path.join(os.pardir,
                                                 'testLOG',
                                                 'simpleResult.txt')))
        os.popen('del /q {}'.format(os.path.join(os.pardir,
                                                 'testLOG',
                                                 'total_log.txt')))
    else:
        os.popen('rm -rf {}'.format(os.path.join(os.pardir,
                                                 'testLOG',
                                                 'androidLog')))
        os.popen('rm -rf {}'.format(os.path.join(os.pardir,
                                                 'testLOG',
                                                 'simpleResult.txt')))
        os.popen('rm -rf {}'.format(os.path.join(os.pardir,
                                                 'testLOG',
                                                 'total_log.txt')))


def logHandle(filePath):
    """处理log信息
    """
    os.popen('adb pull sdcard/AutoTest/screencap {}'
             .format(os.path.join(os.pardir, 'testResult', filePath)))
    os.popen('adb pull sdcard/AutoTest/screenrecord {}'
             .format(os.path.join(os.pardir, 'testResult', filePath)))
    shutil.copytree(os.path.join(os.pardir, 'testLOG', 'androidLog'),
                    os.path.join(os.pardir, 'testResult',
                                 filePath, 'androidLog'))
    shutil.copyfile(os.path.join(os.pardir, 'testLOG', 'simpleResult.txt'),
                    os.path.join(os.pardir, 'testResult',
                                 filePath, 'simpleResult.txt'))
    shutil.copyfile(os.path.join(os.pardir, 'testLOG', 'total_log.txt'),
                    os.path.join(os.pardir, 'testResult',
                                 filePath, 'total_log.txt'))
    if os.path.exists(os.path.join(os.pardir, 'testCase', 'bg_temp.png')):
        os.remove(os.path.join(os.pardir, 'testCase', 'bg_temp.png'))


if __name__ == '__main__':
    # 判读是否是服务器
    # isServer = os.path.exists(os.path.join(os.pardir), '')
    # 获取手机参数信息
    configData = getConfigPara('config.json')
    # 获取需要测试的大类集合
    allTestList = getTestClass('testList.txt')
    # 获取用例路径以及源图片名字
    casePath, caseName, srcImgName, targetImgSuit = getCaseInfo('testCase')
    # 创建结果参数类实例
    rp = androidTR.ResultPara()
    # 获取所有测试用例
    allTestClass, rp.realIngoreModule = cdt.getTestCaseSuit(os.path.join(
                                                                    casePath,
                                                                    caseName),
                                                            allTestList)
    realAllTestClass = getRealTestClass(allTestClass)
    # 删除遗留文件
    envInit()
    # 获取log文件生成路径
    rp.logPath = time.strftime("%Y.%m.%d-%H.%M.%S", time.localtime())
    os.mkdir(os.path.join(os.pardir, 'testResult', rp.logPath))
    logPath = LG.setLogPath()
    # 为driver动态添加logger
    androidBO._LOGGER = LG.logCreater(logPath)
    # 创建 driver 实例
    p = androidUT(configData)
    # 图片所需参数集合
    imgDict = getImgDict(casePath, targetImgSuit, srcImgName)
    # 开始测试
    try:
        androidTR.testRunAllTest(realAllTestClass,
                                 configData, imgDict, p, rp)
    except (Exception, KeyboardInterrupt, SystemExit) as e:
        p._LOGGER.exception(e)
        p._LOGGER.info(u'Test End...')
    finally:
        # 防止主程序意外退出，杀掉其下所有子进程
        while not rp.childPQ.empty():
            childPid = rp.childPQ.get_nowait()
            os.popen('kill -9 {}'.format(childPid))
        # 处理 log 信息
        logHandle(rp.logPath)
        sys.exit(0)
