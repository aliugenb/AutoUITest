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
from XFramework.ios.baseOn import BaseOn as iosBO
from XFramework.ios.uiBase import UITest as iosUT
import XFramework.ios.TestRunner as iosTR
from XFramework.parseExcel import caseDataTransform as cdt
import XFramework.logger.logger as LG


def getTestExcel(casePath):
    fileName = ''
    for path, dirs, files in os.walk(casePath):
        for eachFile in files:
            if '.xlsx' in eachFile or '.xls' in eachFile:
                if '~$' not in eachFile:
                    fileName = eachFile
        if fileName == '':
            print('当前目录未找到测试用例！')
            raise IOError
    return fileName


def getCaseInfo(fileName):
    '''
    只能用于获取父级目录文件
    '''
    casePath = '{}{}{}'.format(os.pardir, os.sep, fileName)
    caseName = getTestExcel(casePath)
    realCasePath = '{}{}{}'.format(casePath, os.sep, caseName)
    return casePath, caseName, realCasePath


def sheetNotExistwarning(getCaseInfo):
    @wraps(getCaseInfo)
    def outerFunc(func):
        def tempFunc(listPath):
            _, _, realCasePath = getCaseInfo('testCase')
            allTestList = func(listPath)
            data_xls = xlrd.open_workbook(realCasePath)
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
    # 获取log文件生成路径
    logPath = LG.setLogPath()
    # 获取手机参数信息
    configData = getConfigPara('config.json')
    # 获取需要测试的大类集合
    allTestList = getTestClass('testList.txt')
    # 获取用例路径
    casePath, caseName, realCasePath = getCaseInfo('testCase')
    # 获取所有测试用例
    allTestClass, realIngoreModule = cdt.getTestCaseSuit(realCasePath,
                                                         allTestList)
    realAllTestClass = getRealTestClass(allTestClass)
    # 获取excel中的所有图片
    #imgs = cdt.getImgFromExcel(casePath, caseName)
    # 测试驱动
    if configData['platformName'] == 'iOS':
        iosBO._LOGGER = LG.logCreater(logPath)
        p = iosUT(configData)
        iosTR.test_run_all_test(realAllTestClass, realIngoreModule,
                                configData, p)
    else:
        print('移动平台参数设置错误，退出测试！')
        sys.exit(1)
