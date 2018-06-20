# -*- coding:utf-8 -*-
import os
import sys
import xlrd
import json
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
        if suffixType in cdt.EXCEL_TYPE:
            if '~$' not in eachFile:
                fileName = eachFile
        if suffixType in cdt.IMG_TYPE:
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


if __name__ == '__main__':
    # 获取手机参数信息
    configData = getConfigPara('config.json')
    # 获取需要测试的大类集合
    allTestList = getTestClass('testList.txt')
    # 获取用例路径以及源图片名字
    casePath, caseName, srcImgName, targetImgSuit = getCaseInfo('testCase')
    # 获取所有测试用例
    allTestClass, realIngoreModule = cdt.getTestCaseSuit(os.path.join(
                                                                    casePath,
                                                                    caseName),
                                                         allTestList)
    realAllTestClass = getRealTestClass(allTestClass)
    # 测试驱动
    if configData['platformName'] == 'Android':
        p = androidUT(configData)
        imgDict = {}
        if srcImgName != '' and targetImgSuit != '':
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
            # 获取图片比例相关系数
            kx, ky = androidTR.getCorrelationCoefficients(srcImgSize,
                                                          p.getScreenSize())
            # 图片所需参数集合
            imgDict = {'testImgPath': testImgPath,
                       'testImgPathName': testImgPathName,
                       'srcImgSize': srcImgSize,
                       'coefficients': (kx, ky),
                       'srcImgName': cdt.getFileNameWithoutSuffix(srcImgName),
                       'realSrcImgName': srcImgName,
                       'srcImgPath': casePath}
        else:
            print("警告: 测试图片压缩文件和源图片未同时存在于上传文件中，默认你未使用图片点击功能！")
        # 获取log文件生成路径
        logPath = LG.setLogPath()
        # 为driver动态添加logger
        androidBO._LOGGER = LG.logCreater(logPath)
        try:
            androidTR.testRunAllTest(realAllTestClass, realIngoreModule,
                                     configData, p, imgDict)
        except Exception as e:
            p._LOGGER.info('Test End...')
            p._LOGGER.exception(e)
        finally:
            # 防止主程序意外退出，杀掉其下所有子进程
            while not androidTR.childPQ.empty():
                childPid = androidTR.childPQ.get()
                os.popen('kill -9 {}'.format(childPid))
            sys.exit(0)
    # elif configData['platformName'] == 'iOS':
    #     iosBO._LOGGER = LG.logCreater(logPath)
    #     p = iosUT(configData)
    #     iosTR.testRunAllTest(realAllTestClass, realIngoreModule,
    #                          configData, p)
    else:
        print('移动平台参数设置错误，退出测试！')
        sys.exit(1)
