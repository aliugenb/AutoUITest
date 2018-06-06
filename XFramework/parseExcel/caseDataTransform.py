# _*_ coding: utf-8 _*_
import os
import sys
import pandas as pd
import xlrd
import zipfile

IMG_TYPE = ['png', 'jpg', 'jpeg', 'bmg']


def getSheetName(filePath, allTestList):
    data_xls = xlrd.open_workbook(filePath)
    sheetList = []
    for index, sheet in enumerate(data_xls.sheets()):
        if sheet.name in allTestList:
            sheetList.append((index, sheet.name))
    if sheetList == []:
        raise ValueError('你上传的表格sheet名与你勾选的不一致, 请核实！')
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
                startList.append((index, name.strip()))
    if len(startList) != len(endList):
        raise ValueError(u'注意检查模块名的起始和结束是否闭合')
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
                featureUnit['featureName'] = featureName.strip()
            stepDesc = dataFrame.loc[rowIndex, ['stepDesc']][0]
            if rowIndex == rowsNum-1:
                if dataFrame.loc[rowIndex, ['precondition']][0] != 'isNaN':
                    if precondition != 'isNaN' and \
                     precondition != dataFrame.loc[rowIndex,
                                                   ['precondition']][0]:
                        raise ValueError('功能点的最后一行不能只是一个判断，请修改用例！')
                else:
                    if '>>' in stepDesc:
                        stepUnit = getStepUnit(dataFrame, rowIndex)
                        multiSteps.append(stepUnit)
                        multiStepUnit['multiSteps'] = multiSteps
                        stepSuit.append(multiStepUnit)
                        featureUnit['featureSteps'] = stepSuit
                        featuresList.append(featureUnit)
                        multiSteps = []
                        multiStepUnit = {}
                        stepSuit = []
                        featureUnit = {}
                    else:
                        stepUnit = getStepUnit(dataFrame, rowIndex)
                        stepSuit.append(stepUnit)
                        featureUnit['featureSteps'] = stepSuit
                        featuresList.append(featureUnit)
                        stepSuit = []
                        featureUnit = {}
            else:
                if dataFrame.loc[rowIndex, ['precondition']][0] != 'isNaN':
                    if precondition != 'isNaN' and \
                       precondition != dataFrame.loc[rowIndex,
                                                     ['precondition']][0]:
                        if multiSteps:
                            multiStepUnit['multiSteps'] = multiSteps
                        if multiStepUnit:
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
                    else:
                        if multiSteps:
                            multiStepUnit['multiSteps'] = multiSteps
                        if multiStepUnit:
                            stepSuit.append(multiStepUnit)
                        multiSteps = []
                        multiStepUnit = {}
                    # else:
                    #     raise ValueError('表单:{}中的第{}行中的参数里有无法识别'
                    #                      .format(sheetName,
                    #                              rowIndex+2))
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


def getFileNameWithoutSuffix(file_name):
    """返回裁取掉后缀的文件名
    """
    file_type = '.{}'.format(file_name.split('.')[-1])
    dir_name = file_name.replace(file_type, '')
    if dir_name != '':
        return dir_name
    else:
        print('The file name you gived is wrong! err: {}'.format(file_name))
        sys.exit(1)


def changeFileType(file_path, file_name, target_type='.zip'):
    """将指定目录中的excel文件类型改为压缩文件
    """
    original_path = os.path.join(file_path, file_name)
    # 判断如果文件不存在，提示用户并退出解释器
    if not os.path.exists(original_path):
        print('No such File! err: {}'.format(original_path))
        sys.exit(1)
    target_name = '{}{}'.format(file_name.split('.')[0], target_type)
    target_path = os.path.join(file_path, target_name)
    # 假如zip文件存在，将其删除
    if os.path.exists(target_path):
        os.remove(target_path)
    os.rename(original_path, target_path)
    return target_name


def unzipFile(file_path, file_name):
    """将指定目录下的Zip文件解压缩到当前文件
    """
    real_path = os.path.join(file_path, file_name)
    # 判断文件是否为压缩文件
    if zipfile.is_zipfile(real_path):
        z = zipfile.ZipFile(real_path, 'r')
        # 判断文件是否损坏
        test_result = z.testzip()
        if test_result is not None:
            print('file is damaged! errFlie: {}'.format(test_result))
            sys.exit(1)
        dir_name = getFileNameWithoutSuffix(file_name)
        dir_path = os.path.join(file_path, dir_name)
        # 检测是否有同名文件夹，存在则删除
        if os.path.exists(dir_path):
            os.popen('rm -rf {}'.format(dir_path))
        # 解压到指定文件目录
        z.extractall(dir_path)
        z.close()
    else:
        print('No compressed file! err: {}'.format(real_path))
        sys.exit(1)


def getImg(file_path, file_name):
    """解压缩的excel目录下获取图片并用PIL读取，存储
    """
    img_dir = 'xl{}media'.format(os.sep)
    dir_name = getFileNameWithoutSuffix(file_name)
    img_path = os.path.join(file_path, dir_name, img_dir)
    if not os.path.exists(img_path):
        print ('No such directory! err: {}'.format(img_path))
        sys.exit(1)
    # 读取指定目录的图片，存储到生成器中
    file_list = os.listdir(img_path)
    try:
        im_path_iter = (os.path.join(img_path, eachImg)
                        for eachImg in file_list
                        if eachImg.split('.')[-1] in IMG_TYPE)
        return im_path_iter
    except IOError as e:
        print('No images! err: {}'.format(img_path))
        sys.exit(1)


def getImgFromExcel(file_path, file_name):
    """获取excel中的所有图片，返回一个存储图片的生成器
    """
    # 改变文件类型为压缩文件
    target_name = changeFileType(file_path, file_name)
    # 解压目标文件
    unzipFile(file_path, target_name)
    # 复原原文件
    changeFileType(file_path, target_name, target_type='.xlsx')
    return getImg(file_path, file_name)
