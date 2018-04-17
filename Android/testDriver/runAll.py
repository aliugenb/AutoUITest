# -*- coding:utf-8 -*-
import os
import xlrd
import caseDataTransform as cdt
import TestRunner as tr
import common
common.pathGet()
from XFramework.base_on import BaseOn
from XFramework.ui_base import UITest
import XFramework.logger as LG


def getTestExcel(filePath):
    fileName = ''
    for path, dirs, files in os.walk(filePath):
        for eachFile in files:
            if '.xlsx' in eachFile or '.xls' in eachFile:
                if '~$' not in eachFile:
                    fileName = eachFile
        if fileName == '':
            print('当前目录未找到测试用例！')
            raise IOError
    return fileName


def sheetNotExistwarning(getTestExcel):
    def outerFunc(func):
        def tempFunc(filePath):
            fileName = getTestExcel('.')
            allTestList = func(filePath)
            data_xls = xlrd.open_workbook(fileName)
            sheetList = []
            realList = [i for i in allTestList]
            for index, sheet in enumerate(data_xls.sheets()):
                sheetList.append(sheet.name)
            for each in allTestList:
                print each
                if each not in sheetList:
                    print('警告：你勾选的{}大类，在测试表格中不存在，已经自动帮你过滤。'
                          .format(each))
                    realList.remove(each)
            return realList
        return tempFunc
    return outerFunc


@sheetNotExistwarning(getTestExcel)
def getTestClass(filePath):
    allTestList = []
    with open('testList.txt', 'r') as f:
        lines = f.readlines()
        for line in lines:
            allTestList.append(line.strip())
    if allTestList == []:
        print('请确认是否勾选测试类！')
        raise ValueError
    return allTestList


if __name__ == '__main__':
    filePath = LG.setLogPath()
    BaseOn._LOGGER = LG.logCreater(filePath)
    p = UITest()
    p.clearApp()
    fileName = getTestExcel('.')
    allTestList = getTestClass('testList.txt')
    allTestClass, realIngoreModule = cdt.getTestCaseSuit(fileName,
                                                         allTestList)
    tr.test_run_all_test(allTestClass, realIngoreModule, p)
