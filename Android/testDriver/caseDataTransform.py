# _*_ coding: utf-8 _*_
import pandas as pd
import xlrd


def getSheetName(filePath, allTestList):
    data_xls = xlrd.open_workbook(filePath)
    sheetList = []
    for index, sheet in enumerate(data_xls.sheets()):
        if sheet.name in allTestList:
            sheetList.append((index, sheet.name))
    return sheetList


def getModleGroup(dataFrame):
    startList = []
    endList = []
    modleDict = {}
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
                modleDict[startList[index][1]] = \
                    '{}-{}'.format(startList[index][0], endList[index][0])
    return modleDict


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
    modleSuit = []
    modleDict = getModleGroup(dataFrame)
    for key, value in modleDict.items():
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
        modleUnit = {"moduleName": key, 'featureSuite': featuresList}
        featuresList = []
        modleSuit.append(modleUnit)
        modleUnit = {}
    testCaseUnit = {'testCaseName': sheetName, 'modleSuit': modleSuit}
    return testCaseUnit


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
        testCaseUnit = getTestCaseUnit(dataFrame, sheet[1])
        testCaseSuit.append(testCaseUnit)
    return testCaseSuit
