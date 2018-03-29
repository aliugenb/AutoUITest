# -*- coding:utf-8 -*-
import caseDataTransform as cdt
import TestRunner as TR
import common
common.pathGet()
from XFramework.base_on import BaseOn
from XFramework.ui_base import UITest
import XFramework.logger as LG


if __name__ == '__main__':
    filePath = LG.setLogPath()
    BaseOn._LOGGER = LG.logCreater(filePath)
    p = UITest()
    p.clearApp()
    allTestList = []
    with open('testList.txt', 'r') as f:
        lines = f.readlines()
        for line in lines:
            allTestList.append(line.strip())
    allTestClass = cdt.getTestCaseSuit('testCase.xlsx', allTestList)
    TR.test_run_all_test(allTestClass, p)
