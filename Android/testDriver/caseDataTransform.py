# _*_ coding: utf-8 _*_
import pandas as pd
import xlrd


def getSheetName(filePath, allTestList):
    data_xls = xlrd.open_workbook(filePath)
    sheetList = []
    for index, sheet in enumerate(data_xls.sheets()):
        if sheet.name in allTestList:
            sheetList.append((index, sheet.name))
    if sheetList == []:
        print('你上传的表格sheet名与你勾选的不一致, 请核实！')
        raise ValueError
    return sheetList


def getModuleGroup(dataFrame):
    startList = []
    endList = []
    moduleDict = {}
    ingoreModule = []
    for index, name in enumerate(dataFrame.loc[:, 'moduleName']):
        if name != 'isNaN':
            if '>>>>' in name:
                endList.append((index, name))
            else:
                startList.append((index, name))
    if len(startList) != len(endList):
        print(u'注意检查模块名的起始和结束是否闭合')
    else:
        for index in range(len(startList)):
            if '#' not in startList[index][1]:
                moduleDict[startList[index][1]] = \
                    '{}-{}'.format(startList[index][0], endList[index][0])
            else:
                moduleName = startList[index][1].strip().split('#')[1]
                ingoreModule.append(moduleName)
    return moduleDict, ingoreModule


def getStepUnit(dataFrame, rowIndex):
    stepUnit = {}
    for eachColumn in dataFrame.columns[3:dataFrame.shape[1]]:
        if dataFrame.loc[rowIndex, [eachColumn]][0] != 'isNaN':
            if eachColumn == 'optional':
                stepUnit[eachColumn] =\
                 str(dataFrame.loc[rowIndex, [eachColumn]][0])
            else:
                stepUnit[eachColumn] = dataFrame.loc[rowIndex, [eachColumn]][0]
    return stepUnit


def getTestCaseUnit(dataFrame, sheetName):
    precondition = 'isNaN'
    featuresList = []
    stepSuit = []
    multiSteps = []
    featureUnit = {}
    multiStepUnit = {}
    moduleSuit = []
    moduleDict, ingoreModule = getModuleGroup(dataFrame)
    for key, value in moduleDict.items():
        rowIndex, rowsNum = [int(i) for i in value.split('-')]
        while rowIndex <= rowsNum-1:
            if dataFrame.loc[rowIndex, ['featureName']][0] != 'isNaN':
                featureName = dataFrame.loc[rowIndex, ['featureName']][0]
                featureUnit['featureName'] = featureName
            stepDesc = dataFrame.loc[rowIndex, ['stepDesc']][0]
            if dataFrame.loc[rowIndex, ['precondition']][0] != 'isNaN':
                if precondition != 'isNaN' and \
                 precondition != dataFrame.loc[rowIndex, ['precondition']][0]:
                    multiStepUnit['multiSteps'] = multiSteps
                    stepSuit.append(multiStepUnit)
                    multiSteps = []
                    multiStepUnit = {}
                precondition = dataFrame.loc[rowIndex, ['precondition']][0]
                multiStepUnit['precondition'] = precondition
            else:
                if '>>' in stepDesc:
                    stepUnit = getStepUnit(dataFrame, rowIndex)
                    multiSteps.append(stepUnit)
                    rowIndex += 1
                    continue
                elif '>>' not in stepDesc and precondition != 'isNaN':
                    multiStepUnit['multiSteps'] = multiSteps
                    stepSuit.append(multiStepUnit)
                    precondition = 'isNaN'
                    multiSteps = []
                    multiStepUnit = {}
                else:
                    pass
                if rowIndex == rowsNum-1:
                    stepUnit = getStepUnit(dataFrame, rowIndex)
                    stepSuit.append(stepUnit)
                    featureUnit['featureSteps'] = stepSuit
                    featuresList.append(featureUnit)
                    stepSuit = []
                    featureUnit = {}
                else:
                    if stepDesc != 'isNaN':
                        stepUnit = getStepUnit(dataFrame, rowIndex)
                        stepSuit.append(stepUnit)
                    else:
                        featureUnit['featureSteps'] = stepSuit
                        featuresList.append(featureUnit)
                        stepSuit = []
                        featureUnit = {}
            rowIndex += 1
        moduleUnit = {"moduleName": key, 'featureSuite': featuresList}
        featuresList = []
        moduleSuit.append(moduleUnit)
        moduleUnit = {}
    testCaseUnit = {'testCaseName': sheetName, 'moduleSuit': moduleSuit}
    realIngoreModule = []
    if ingoreModule != []:
        for module in ingoreModule:
            modulePath = '{}-{}'.format(sheetName, module)
            realIngoreModule.append(modulePath)
    return testCaseUnit, realIngoreModule


def getTestCaseSuit(filePath, allTestList):
    testCaseSuit = []
    sheetList = getSheetName(filePath, allTestList)
    for sheet in sheetList:
        data_xls = pd.read_excel(filePath, sheet_name=sheet[0], index_col=0)
        csvPath = '{}.csv'.format(filePath.split('.')[0])
        data_xls.to_csv(csvPath, mode='w', encoding='utf-8')
        dataFrame = pd.read_csv(csvPath)
        # 填充空值
        dataFrame = dataFrame.fillna('isNaN')
        testCaseUnit, realIngoreModule = getTestCaseUnit(dataFrame, sheet[1])
        testCaseSuit.append(testCaseUnit)
    return testCaseSuit, realIngoreModule
