# -*- coding:utf-8 -*-
import os
import sys
import time
import re
import urllib2
import cv2 as cv
import subprocess
from PIL import Image
from multiprocessing import Process, Queue
from functools import wraps
import selenium
from action import Action
from uiBase import UITest
from commandContainer import CommandContainer as CC


class ResultPara(object):
    """定义结果参数
    """
    # 总共测试次数
    totalCount = 0
    # 通过次数
    passCount = 0
    # 失败次数
    failCount = 0
    # 中止次数
    abortCount = 0
    # 异常次数
    exceptionCount = 0
    # 失败详情列表
    failList = []
    # 中止详情列表
    abortList = []
    # 期望详情列表
    exceptionList = []
    # 忽略功能点详情列表
    ingoreFeature = []
    # 忽略模块详情列表
    realIngoreModule = []
    # 正常失败标志位
    realFailTag = 0
    # 设置记录子进程 pid 的队列
    childPQ = Queue()
    # 设置中止子进程标志队列
    childPK = Queue()
    # log 路径名
    logPath = None


def getValidValueFromStr(control):
    """从字串中获取有效值
    """
    reminderValue = None
    for i in ['text', 'desc', 'Id']:
        if i in control:
            reminderValue = control.split('{}='.format(i))[-1].split(',')[0]
            break
    return reminderValue


def getValidValueFromDict(targetDict):
    """从字典中获取有效值
    """
    reminderValue = None
    for i in ['text', 'desc', 'Id']:
        if targetDict.get(i):
            reminderValue = targetDict.get(i)
            break
    return reminderValue


def exceptionHandle(func):
    """错误类型集合
    异常1: 点击时找不到text控件
    异常2: 点击时找不到desc控件
    异常3: 点击时找不到Id控件
    异常4: 文本输入失败
    异常5: 判断失败
    异常6: 点击判等失败
    异常7: 点击判不等失败
    异常8: 等待控件超时
    异常9: 表格中图片数量不等于clickByPic动作数量
    异常10: 目标页面上未找你输入的图片
    """
    @wraps(func)
    def tempFunc(*args, **kwargs):
        try:
            func(*args, **kwargs)
        except AssertionError as e:
            flowTag = e.args[0]
            reminderValue = getValidValueFromStr(args[0])
            if flowTag == 1:
                raise AssertionError(u"找不到你输入的text: {}，请确认!"
                                     .format(reminderValue))
            elif flowTag == 2:
                raise AssertionError(u"找不到你输入的desc: {}，请确认!"
                                     .format(reminderValue))
            elif flowTag == 3:
                raise AssertionError(u"找不到你输入的Id: {}，请确认!"
                                     .format(reminderValue))
            elif flowTag == 4:
                raise AssertionError(u"文本: {} 输入失败，请确认!"
                                     .format(args[1]))
            elif flowTag == 5:
                raise AssertionError('{}_fail'.format(args[1]))
            elif flowTag == 6:
                raise AssertionError(u'点击操作后，此元素 {} 的text值发生改变，fail'.format(
                                        reminderValue))
            elif flowTag == 7:
                raise AssertionError(u'点击操作后，此元素 {} 的text值未发生改变，fail'.format(
                                        reminderValue))
            elif flowTag == 8:
                raise AssertionError(u'规定时间内，仍未找到该元素: {}，fail'.format(
                                        reminderValue))
            elif flowTag == 9:
                raise AssertionError(u'图片资源缺失，请核实! err: {}, fail'.format(
                                                                    e.args[1]))
            elif flowTag == 10:
                raise AssertionError(u'规定时间内，目标页面上未找你输入的图片: {}, fail'.format(
                                                                    e.args[1]))
            elif flowTag == 11:
                raise AssertionError(u'你给定的控件: {} 未被选中, fail'.format(
                                        reminderValue))
            elif flowTag == 12:
                raise AssertionError(u'{}滑动{}步, 控件 {} 共出现{} 次与预期出现次数{} {}，fail'
                                     .format(*(e.args[1])))
            else:
                raise RuntimeError(u'不存在的异常类型')
    return tempFunc


def writeResultToTxt(lineContent, filePath=None, fileName='simpleResult.txt'):
    """将结果写入到指定文件中
    """
    if filePath is None:
        filePath = os.path.join(os.pardir, 'testLOG')
    else:
        filePath = os.path.join(os.pardir, 'testLOG', filePath)
    realPath = os.path.join(filePath, fileName)
    with open(realPath, 'a') as f:
        f.write(lineContent)


def getImgSize(filePath):
    """获取图片像素大小
    """
    reImg = Image.open(filePath)
    return reImg.size


def getScreenDetail():
    """获取手机屏幕详情
    """
    infoDict = {}
    needList = []
    if re.match('^win', sys.platform):
        command = 'adb shell dumpsys window displays | findstr app='
    else:
        command = CC.GET_SCREEN_DETAIL
    tempData = os.popen(command).read()
    pendingList = tempData.strip().split('\n')
    for each in pendingList:
        if 'cur=' in each:
            needList = each.strip().split(' ')
            break
    for el in needList:
        if '=' in el:
            val = el.strip().split('=')
            infoDict[val[0]] = val[1]
        else:
            if not infoDict.get('density'):
                val = el.strip().split('dpi')
                infoDict['density'] = val[0]
    return infoDict


def adaptiveCoefficient(infoDict, srcImgName):
    """获取当前手机屏幕参数，并转化为标准参数系数
    """
    # 获取图片来源
    imgName = srcImgName.strip().split('.')[0]
    if re.match('^.+_[0-9]+x[0-9]+x[0-9]+$', imgName):
        imgW, imgH, imgD = [int(i) for i in imgName.split('_')[-1].split('x')]
    else:
        imgW, imgH, imgD = (1080, 1920, 480)
    cx, cy = [int(i) for i in infoDict.get('app').split('x')]
    kx1 = float(cx*int(infoDict.get('density')))/(imgW*imgD)
    ky1 = float(cy*int(infoDict.get('density')))/(imgH*imgD)
    return kx1, ky1


def getCorrelationCoefficients(practicalSize, idealSize, acPara):
    """获取截图像素和手机屏幕像素之比
    """
    practicalSizeX, practicalSizeY = practicalSize
    idealSizeX, idealSizeY = idealSize
    kx2 = idealSizeX/float(practicalSizeX/acPara[0])
    ky2 = idealSizeY/float(practicalSizeY/acPara[1])
    return kx2, ky2


def adaptiveImageSize(infoDict, imgDict):
    """图片适配全面屏，将截图裁剪掉多余部分
    """
    cx, cy = [int(i) for i in infoDict.get('app').split('x')]
    ix, iy = [int(i) for i in infoDict.get('cur').split('x')]
    if iy > cy:
        oImg = cv.imread(os.path.join(imgDict['srcImgPath'],
                                      'bg_temp.png'))
        rImg = oImg[0:cy, 0:cx]
        cv.imwrite(os.path.join(imgDict['srcImgPath'],
                                'bg_temp.png'), rImg)


def changeImgSize(filePath, practicalSize, acPara):
    """将手机截图图片大小压缩为指定图片的大小
    """
    im = Image.open(filePath)
    rp = (int(practicalSize[0]/acPara[0]), int(practicalSize[1]/acPara[1]))
    new_im = im.resize(rp, Image.ANTIALIAS)
    new_im.save(filePath)


def getCompareImg(uiObj, imgDict):
    """将手机的当前页面截图，并把尺寸转化为和源图片一致
    """
    uiObj.screencap('bg_temp', CC.PHONE_PIC_COMPARE_PATH)
    uiObj.pullFile('{}/{}'.format(CC.PHONE_PIC_COMPARE_PATH,
                                  'bg_temp.png'),
                   imgDict['srcImgPath'])
    adaptiveImageSize(imgDict.get('screenDetail'), imgDict)
    changeImgSize(os.path.join(imgDict['srcImgPath'],
                               'bg_temp.png'),
                  imgDict['srcImgSize'],
                  imgDict['acPara'])


def getPosOnScreen(originalPos, coefficients):
    """获取屏幕上的坐标点
    """
    realPosX = int(originalPos[0] * coefficients[0])
    realPosY = int(originalPos[1] * coefficients[1])
    return realPosX, realPosY


def transferProperty(target, key, source):
    """动态的向某个类写入属性
    """
    if key in source:
        setattr(target, key, source.get(key))


def detailPrint(detailName, targetList, filePath=None):
    """适配输出测试结果
    """
    if len(targetList) != 0:
        print('{}:'.format(detailName))
        writeResultToTxt('{}:\n'.format(detailName), filePath)
        for i in targetList:
            print('\t{}'.format(i))
            writeResultToTxt('\t{}\n'.format(i), filePath)
        print('='*60)
        writeResultToTxt('{}\n'.format('='*60), filePath)


def setPara(stepEvent, stepAction):
    """步骤事件类写入属性
    """
    transferProperty(stepEvent, 'controlType', stepAction)
    transferProperty(stepEvent, 'inputText', stepAction)
    transferProperty(stepEvent, 'controlAction', stepAction)
    transferProperty(stepEvent, 'expectation', stepAction)
    transferProperty(stepEvent, 'expectationLog', stepAction)
    transferProperty(stepEvent, 'optional', stepAction)


def creatEvent(stepAction):
    """创建步骤事件
    """
    stepEvent = Action()
    stepEventList = []
    transferProperty(stepEvent, 'precondition', stepAction)
    if stepEvent.precondition != '':
        stepEventList.append(stepEvent)
        multiSteps = stepAction['multiSteps']
        for step in multiSteps:
            eachEvent = Action()
            setPara(eachEvent, step)
            stepEventList.append(eachEvent)
    else:
        setPara(stepEvent, stepAction)
        stepEventList.append(stepEvent)
    return stepEventList


def preconditionHandle(pre, uiObj, totalTime):
    """前提参数处理
    """
    preJudgeVal = False
    if '==' in pre:
        preElType, preEl = pre.strip().split('==')
        if preElType == 'text':
            preJudgeVal = uiObj.isTextInPage(preEl, totalTime=totalTime)
        elif preElType == 'desc':
            preJudgeVal = uiObj.isDescInPage(preEl, totalTime=totalTime)
        elif preElType == 'Id':
            preJudgeVal = uiObj.isIdInPage(preEl, totalTime=totalTime)
        else:
            raise ValueError(u'前提参数: {} 控件类型不合法,提醒:可能存在空格'.format(pre))
    elif '!=' in pre:
        preElType, preEl = pre.strip().split('!=')
        if preElType == 'text':
            preJudgeVal = not uiObj.isTextInPage(preEl, totalTime=totalTime)
        elif preElType == 'desc':
            preJudgeVal = not uiObj.isDescInPage(preEl, totalTime=totalTime)
        elif preElType == 'Id':
            preJudgeVal = not uiObj.isIdInPage(preEl, totalTime=totalTime)
        else:
            raise ValueError(u'前提参数: {} 控件类型不合法,提醒:可能存在空格'.format(pre))
    else:
        raise ValueError(u'前提参数: {} 不合法, 提醒:可能存在中文符号'.format(pre))
    return preJudgeVal


def getDecompressPath(control, imgDict):
    """获取解压缩文件所在位置
    """
    targetImgName = os.path.join(imgDict['testImgPath'],
                                 '{}.png'.format(control))
    # 防止压缩策略问题
    if not os.path.exists(targetImgName):
        fields = os.listdir(imgDict['testImgPath'])
        targetPath = [field for field in fields
                      if '__' not in field and '.' not in field]
        targetImgName = os.path.join(imgDict['testImgPath'],
                                     targetPath[0],
                                     '{}.png'.format(control))
    return targetImgName


def getPosOfPic(targetImgName, imgDict, uiObj):
    """获取测试图片所在位置
    """
    # 点击总次数
    totalTime = 10
    # 实际已点次数
    countTime = 0
    # 10s内刷新匹配图片
    while countTime < totalTime:
        getCompareImg(uiObj, imgDict)
        reInfo = uiObj.getTargetImgPos(os.path.join(
                                            imgDict['srcImgPath'],
                                            'bg_temp.png'),
                                       targetImgName)
        if reInfo is not None:
            break
        time.sleep(1)
        countTime += 1
    return reInfo


def paraParse(control):
    """控件类型列，参数解析
    """
    allParaList = control.strip().split(',')
    paraList = []
    paraDict = {}
    for eachPara in allParaList:
        if '=' in eachPara:
            paraKey, paraValue = eachPara.strip().split('=')
            paraDict[paraKey] = paraValue
        else:
            paraList.append(eachPara)
    return paraList, paraDict


def click(paraList, paraDict, control, uiObj):
    """点击实现
    """
    if 'text' in paraDict:
        if paraDict.get('ins'):
            uiObj.clickByTextInstance(**paraDict)
        else:
            uiObj.clickByText(**paraDict)
    elif 'desc' in paraDict:
        if paraDict.get('ins'):
            uiObj.clickByDescInstance(**paraDict)
        else:
            uiObj.clickByDesc(**paraDict)
    elif 'Id' in paraDict:
        if paraDict.get('ins'):
            uiObj.clickByIdInstance(**paraDict)
        else:
            uiObj.clickById(**paraDict)
    elif len(paraList) == 1 and '-' in paraList[0]:
        uiObj.clickByPos(*(paraList[0].split('-')))
        uiObj._LOGGER.debug(u'点击坐标: {}-{} 结束'
                            .format(*(paraList[0].split('-'))))
    elif len(paraList) == 2:
        uiObj.clickByPos(*(paraList))
        uiObj._LOGGER.debug(u'点击坐标: {},{} 结束'.format(*(paraList)))
    else:
        raise ValueError(u'表格参数: {} 不合法,提醒:可能存在空格或中文符号'.format(control))


def clickByPic(control, imgDict, uiObj):
    """图片点击实现
    """
    if imgDict == {}:
        raise AssertionError(9, u'上传文件中图片资源缺失！')
    try:
        # 获取测试图片位置
        targetImgName = getDecompressPath(control, imgDict)
        # 获取测试图片在当前界面所处位置
        reInfo = getPosOfPic(targetImgName, imgDict, uiObj)
    except IOError as e:
        raise AssertionError(9, e)
    if reInfo is not None:
        realPos = getPosOnScreen(reInfo, imgDict['ccPara'])
        uiObj.clickByPos(realPos[0], realPos[1])
        uiObj._LOGGER.debug(u'点击图片: {} ，结束'.format(control))
    else:
        raise AssertionError(10, control)


def swipe(paraList, control, uiObj):
    """滑动实现
    """
    if len(paraList) == 1 and '-' in paraList[0]:
        uiObj.swipeByPos(*(paraList[0].split('-')))
        uiObj._LOGGER.debug(u'滑动: {}-{}-{}-{} 结束'.format(
                                                    *(paraList[0].split('-'))))
    elif len(paraList) == 4:
        uiObj.swipeByPos(*(paraList))
        uiObj._LOGGER.debug(u'滑动: {},{},{},{} 结束'.format(*(paraList)))
    else:
        raise ValueError(u'表格参数: {} 不合法,提醒:可能存在空格或中文符号'.format(control))


def drag(paraList, paraDict, control, uiObj):
    """拖动实现
    """
    if paraList == []:
        uiObj.dragByElement(**paraDict)
    else:
        raise ValueError(u'表格参数: {} 不合法,提醒:可能存在空格或中文符号'.format(control))


def typewrite(paraDict, control, data, uiObj):
    """输入实现
    """
    if control == '':
        uiObj.set_input_text(data)
    else:
        paraDict['input_text'] = data
        if 'text' in paraDict:
            uiObj.setValueByText(**paraDict)
        elif 'desc' in paraDict:
            uiObj.setValueByDesc(**paraDict)
        elif 'Id' in paraDict:
            uiObj.setValueById(**paraDict)
        else:
            raise ValueError(u'表格参数: {} 不合法,提醒:可能存在空格或中文符号'.format(control))


def scroll(paraDict, control, uiObj):
    """滚动实现
    """
    if 'text' in paraDict or 'desc' in paraDict or 'Id' in paraDict:
        uiObj.scrollByElement(**paraDict)
    else:
        raise ValueError(u'表格参数: {} 不合法,提醒:可能存在空格或中文符号'.format(control))


def scrollAndClick(paraDict, control, uiObj):
    """滚动点击实现
    """
    if 'text' in paraDict:
        uiObj.scrollByElement(**paraDict)
        uiObj.clickByText(**paraDict)
    elif 'desc' in paraDict:
        uiObj.scrollByElement(**paraDict)
        uiObj.clickByDesc(**paraDict)
    elif 'Id' in paraDict:
        uiObj.scrollByElement(**paraDict)
        uiObj.clickById(**paraDict)
    else:
        raise ValueError(u'表格参数: {} 不合法,提醒:可能存在空格或中文符号'.format(control))


def sleep(paraList, paraDict, control, uiObj):
    """等待实现
    """
    if len(paraList) == 1 and paraDict == {}:
        uiObj.sleep(int(control))
    elif len(paraList) == 1 and paraDict != {}:
        uiObj.sleep(int(paraList[0]), **paraDict)
    else:
        raise ValueError(u'表格参数: {} 不合法,提醒:可能存在空格或中文符号'.format(control))


def clickAndEqual(paraList, paraDict, control, uiObj):
    """点击并判断相等实现
    """
    if paraList == []:
        textBefore = uiObj.getTextById(**paraDict)
        uiObj.clickById(**paraDict)
        textAfter = uiObj.getTextById(**paraDict)
        if textBefore == textAfter:
            pass
        else:
            raise AssertionError(6)
    else:
        raise ValueError(u'表格参数: {} 不合法,提醒:可能存在空格或中文符号'.format(control))


def clickAndUnequal(paraList, paraDict, control, uiObj):
    """点击并判断不相等实现
    """
    if paraList == []:
        textBefore = uiObj.getTextById(**paraDict)
        uiObj.clickById(**paraDict)
        textAfter = uiObj.getTextById(**paraDict)
        if textBefore != textAfter:
            pass
        else:
            raise AssertionError(7)
    else:
        raise ValueError(u'表格参数: {} 不合法,提醒:可能存在空格或中文符号'.format(control))


def back(uiObj):
    """返回实现
    """
    uiObj.pressBack()


def wSwipeAndAssert(paraList, paraDict, control, uiObj):
    """横向滑动，并判断某个元素出现次数实现
    """
    if paraList == []:
        res, iCount, pCount = uiObj.wSwipeAndAssert(**paraDict)
        if res:
            uiObj._LOGGER.debug(u'横向滑动{} 步，控件 {} 共出现 {} 次，与预期出现次数 {} 相符，滑动判断结束'
                                .format(paraDict.get('step', 9),
                                        getValidValueFromDict(paraDict),
                                        iCount, pCount))
        else:
            raise AssertionError(12, ('横向', paraDict.get('step', 9),
                                      getValidValueFromDict(paraDict),
                                      iCount, pCount, '不相符'))
    else:
        raise ValueError(u'表格参数: {} 不合法,提醒:可能存在空格或中文符号'.format(control))


def hSwipeAndAssert(paraList, paraDict, control, uiObj):
    """纵向滑动，并判断某个元素出现次数实现
    """
    if paraList == []:
        res, iCount, pCount = uiObj.hSwipeAndAssert(**paraDict)
        if res:
            uiObj._LOGGER.debug(u'纵向滑动{} 步，控件 {} 共出现 {} 次，与预期出现次数 {} 相符，滑动判断结束'
                                .format(paraDict.get('step', 9),
                                        getValidValueFromDict(paraDict),
                                        iCount, pCount))
        else:
            raise AssertionError(12, ('纵向', paraDict.get('step', 9),
                                      getValidValueFromDict(paraDict),
                                      iCount, pCount, '不相符'))
    else:
        raise ValueError(u'表格参数: {} 不合法,提醒:可能存在空格或中文符号'.format(control))


def isChecked(paraDict, control, uiObj):
    """判断元素是否被选中实现
    """
    el = uiObj.getElementFromControl(**paraDict)
    if el:
        if el.get_attribute('checked') == 'true':
            uiObj._LOGGER.debug(u'判断控件 {} 被选中，结束'.format(
                getValidValueFromDict(paraDict)))
        else:
            raise AssertionError(11)
    else:
        raise ValueError(u'表格参数: {} 不合法,提醒:可能存在空格或中文符号'.format(control))


@exceptionHandle
def actionHandle(control, data, realAction, uiObj, imgDict):
    """动作处理
    """
    paraList, paraDict = paraParse(control)
    if realAction == 'click':
        click(paraList, paraDict, control, uiObj)
    elif realAction == 'clickByPic':
        clickByPic(control, imgDict, uiObj)
    elif realAction == 'swipe':
        swipe(paraList, control, uiObj)
    elif realAction == 'drag':
        drag(paraList, paraDict, control, uiObj)
    elif realAction == 'typewrite':
        typewrite(paraDict, control, data, uiObj)
    elif realAction == 'scroll':
        scroll(paraDict, control, uiObj)
    elif realAction == 'scroll&&click':
        scrollAndClick(paraDict, control, uiObj)
    elif realAction == 'sleep':
        sleep(paraList, paraDict, control, uiObj)
    elif realAction == 'isChecked':
        isChecked(paraDict, control, uiObj)
    elif realAction == 'click&&equal':
        clickAndEqual(paraList, paraDict, control, uiObj)
    elif realAction == 'click&&unequal':
        clickAndUnequal(paraList, paraDict, control, uiObj)
    elif realAction == 'back':
        back(uiObj)
    elif realAction == 'wSwipe&&Assert':
        wSwipeAndAssert(paraList, paraDict, control, uiObj)
    elif realAction == 'hSwipe&&Assert':
        hSwipeAndAssert(paraList, paraDict, control, uiObj)
    else:
        raise ValueError(u'不存在的动作类型: {}'.format(realAction))


def expectTypeHandle(paraDict, expect, uiObj):
    """期望元素处理
    """
    expectVal = False
    try:
        if 'text' in paraDict:
            uiObj.isExistByText(**paraDict)
        elif 'desc' in paraDict:
            uiObj.isExistByDesc(**paraDict)
        elif 'Id' in paraDict:
            uiObj.isExistById(**paraDict)
        else:
            raise ValueError(u'期望参数: {} 中的控件类型不合法'.format(expect))
        expectVal = True
    except AssertionError as e:
        pass
    return expectVal


def expectParaParse(expectPara, expect):
    """期望类型列，参数解析
    """
    allParaList = expectPara.strip().split(',')
    paraDict = {}
    for eachPara in allParaList:
        if '==' in eachPara:
            paraKey, paraValue = eachPara.strip().split('==')
        elif '!=' in eachPara:
            paraKey, paraValue = eachPara.strip().split('!=')
            paraDict['isIn'] = 1
        elif '=' in eachPara:
            paraKey, paraValue = eachPara.strip().split('=')
        else:
            raise ValueError(u'表格参数: {} 不合法,提醒:可能存在空格或中文符号'.format(expect))
        paraDict[paraKey] = paraValue
    return paraDict


def getExpectList(expectParaList, expect, expectInfo, uiObj):
    """获取期望列表
    """
    condition = []
    for eachPara in expectParaList:
        paraDict = expectParaParse(eachPara, expect)
        paraDict['instruction'] = expectInfo
        tempData = expectTypeHandle(paraDict, expect, uiObj)
        condition.append(tempData)
    return condition


def getExpectResult(condition, judgeTag, expectInfo, uiObj):
    """等到期望结果
    """
    if judgeTag == 0:
        for i in condition:
            if not i:
                raise AssertionError(5)
        else:
            uiObj._LOGGER.debug(u'{}， 结束'.format(expectInfo))
    elif judgeTag == 1:
        for i in condition:
            if i:
                uiObj._LOGGER.debug(u'{}， 结束'.format(expectInfo))
                break
        else:
            raise AssertionError(5)
    else:
        if condition[0]:
            uiObj._LOGGER.debug(u'{}， 结束'.format(expectInfo))
        else:
            raise AssertionError(5)


@exceptionHandle
def expectHandle(expect, expectInfo, uiObj):
    """期望处理
    """
    judgeTag = None
    if '&&' in expect:
        expectParaList = expect.strip().split('&&')
        judgeTag = 0
    elif '||' in expect:
        expectParaList = expect.strip().split('||')
        judgeTag = 1
    else:
        expectParaList = [expect.strip()]
    condition = getExpectList(expectParaList, expect, expectInfo, uiObj)
    getExpectResult(condition, judgeTag, expectInfo, uiObj)


def executeEvent(stepEventSuit, uiObj, totalTime, imgDict):
    """执行动作事件
    """
    for stepEventUnit in stepEventSuit:
        for stepEvent in stepEventUnit:
            pre = stepEvent.precondition
            control = stepEvent.controlType
            data = stepEvent.inputText
            realAction = stepEvent.controlAction
            expect = stepEvent.expectation
            expectInfo = stepEvent.expectationLog
            isOptional = stepEvent.optional
            try:
                if pre != '':
                    preJudgeRet = not preconditionHandle(pre, uiObj, totalTime)
                    if preJudgeRet:
                        break
                if realAction != '':
                    actionHandle(control, data,
                                 realAction.strip(), uiObj, imgDict)
                if expect != '':
                    expectHandle(expect, expectInfo, uiObj)
            except AssertionError as e:
                if isOptional == '1.0':
                    pass
                else:
                    uiObj._LOGGER.error(e)
                    raise


def replaceIllegalCharacter(targrtString):
    """检测传入字符是否含非法字符，并用 - 代替非法字符
    """
    expression = re.compile(CC.SPECIAL_CHARACTER_LIST, re.U)
    return re.sub(expression, '-', targrtString)


def getRecordCommandIter(sdcardPath):
    """返回录屏命令生成器
    """
    recordCommandIter = (['adb', 'shell', 'screenrecord', '--time-limit',
                          '180', r'{}/{}.mp4'.format(sdcardPath, i)]
                         for i in range(1, 100))
    return recordCommandIter


def emptyQueue(queue):
    """清空一个队列
    """
    while not queue.empty():
        queue.get_nowait()


def screenRecordForFeature(rName, uiObj, rpObj):
    """为每个功能点录屏
    """
    # 获取子进程 pid
    rpObj.childPQ.put_nowait(os.getpid())
    # 定义子进程的子进程
    grandchildP = None
    # 检测是否有非法字符，并用 - 代替非法字符
    record_field = replaceIllegalCharacter(rName)
    sdcardPath = 'sdcard/AutoTest/screenrecord/{}'.format(record_field)
    # 创建手机中 sdcardPath 的目录
    uiObj.new_floder(sdcardPath)
    # 获取录屏命令
    rcIter = getRecordCommandIter(sdcardPath)
    command = 'adb devices'
    while True:
        # 检测是否有子进程在录屏，没有则fork
        if grandchildP is None or grandchildP.poll() is not None:
            grandchildP = subprocess.Popen(rcIter.next())
        # 标志队列为空，则结束循环
        if not rpObj.childPK.empty():
            break
        # 检测是否有手机，没有则结束循环
        f = os.popen(command).read().strip()
        fl = f.split('\n')
        if len(fl) == 1:
            break
    if grandchildP is not None:
        grandchildP.kill()
        grandchildP.wait()


def showReport(rpObj):
    """展示报告
    """
    totalResult = u'总共: {}个\n成功: {}个\n失败: {}个\n中止: {}个\n异常: {}个\n'\
                  .format(rpObj.totalCount,
                          rpObj.passCount,
                          rpObj.failCount,
                          rpObj.abortCount,
                          rpObj.exceptionCount
                          )
    print(totalResult)
    writeResultToTxt('{}\n'.format(totalResult), rpObj.logPath)
    detailPrint(u'失败用例', rpObj.failList, rpObj.logPath)
    detailPrint(u'中止用例', rpObj.abortList, rpObj.logPath)
    detailPrint(u'异常用例', rpObj.exceptionList, rpObj.logPath)
    if rpObj.realIngoreModule != []:
        detailPrint(u'忽略模块', rpObj.realIngoreModule, rpObj.logPath)
    if rpObj.ingoreFeature != []:
        detailPrint(u'忽略功能点', rpObj.ingoreFeature, rpObj.logPath)


def popOutHandle(pre_firstEventSuit, uiObj, imgDict):
    """处理首次启动的弹窗
    """
    numCount = 10
    while numCount > 0:
        executeEvent(pre_firstEventSuit, uiObj, 0, imgDict)
        if uiObj.isIdInPage('com.ximalaya.ting.android:id/main_count_down_text'):
            uiObj.clickById('com.ximalaya.ting.android:id/main_count_down_text')
        time.sleep(1)
        if uiObj.isTextInPage('首页')\
           and (not uiObj.isIdInPage('com.ximalaya.ting.android.main.application:id/main_btn_skip')
                or not uiObj.isIdInPage('com.ximalaya.ting.android:id/main_btn_skip')):
            break
        else:
            numCount -= 1
    else:
        uiObj._LOGGER.debug(u'点击app弹窗失败，请检测app控件名是否正确！')


def firstStartHandle(steps):
    """首次启动事件处理
    """
    firstEventSuit = []
    pre_firstEventSuit = []
    nor_firstEventSuit = []
    for eachStep in steps:
        firstEventSuit.append(creatEvent(eachStep))
    # 处理初始化
    for i in firstEventSuit:
        if len(i) >= 2:
            if i[0].precondition != '' and\
             i[1].optional != '':
                pre_firstEventSuit.append(i)
            else:
                nor_firstEventSuit.append(i)
        elif len(i) == 1:
            nor_firstEventSuit.append(i)
        else:
            pass
    return pre_firstEventSuit, nor_firstEventSuit


def ingorePartFilter(features, testClassName, moduleName):
    """过滤忽略功能点
    """
    realFeatures = []
    # 此模块下忽略的功能点
    tempIngoreFeature = []
    # 此模块下忽略功能点数目
    ingoreFeaturesNum = 0
    # 检测模块中的功能点是否被全部忽略
    for tempFeature in features:
        if '#' in tempFeature['featureName']:
            rfeatureName = tempFeature['featureName'].strip()\
                                                     .split('#')[-1]
            rPath = '{}-{}-{}'.format(testClassName,
                                      moduleName,
                                      rfeatureName)
            tempIngoreFeature.append(rPath)
            ingoreFeaturesNum += 1
        else:
            realFeatures.append(tempFeature)
    return realFeatures, tempIngoreFeature, ingoreFeaturesNum


def testRunAllTest(allTestClass, configData, imgDict, uiObj, rpObj):
    """执行所有用例
    """
    # 获取手机厂商
    df = os.popen(CC.GET_PHONE_PRODUCER).read().upper()
    # 定义子进程
    childP = None
    # 安卓测试机本身 log 存放地址
    androidLogField = os.path.join(os.pardir, 'testLOG',
                                   rpObj.logPath, 'androidLog')
    os.mkdir(androidLogField)
    # 处理大类
    for eachTestClass in allTestClass:
        # 获取每个测试大类名称
        testClassName = eachTestClass['testCaseName']
        testCase = eachTestClass['moduleSuit']
        if testClassName == 'ad':
            uiObj.clearApp(isAD=True)
            uiObj.pressHome()
        else:
            uiObj.clearApp()
        # 处理模块
        for eachModule in testCase:
            # 获取每个测试大类下测试模块名称
            moduleName = eachModule['moduleName']
            features = eachModule['featureSuite']
            # 除去忽略模块实际要跑的功能点集合
            realFeatures, tempIngoreFeature, ingoreFeaturesNum =\
                ingorePartFilter(features, testClassName, moduleName)
            # 主app和广告业务逻辑不同
            if testClassName == 'ad':
                if len(features) == ingoreFeaturesNum:
                    print(u'警告: 模块: {} 的所有功能点都被你忽略，默认你忽略了此模块。'
                          .format(moduleName))
                    rpObj.realIngoreModule.append('{}-{}'.format(testClassName,
                                                                 moduleName))
                    continue
                else:
                    ingoreFeature.extend(tempIngoreFeature)
            else:
                if len(features) == ingoreFeaturesNum+1:
                    print(u'警告: 模块: {} 的所有功能点都被你忽略，默认你忽略了此模块。'
                          .format(moduleName))
                    rpObj.realIngoreModule.append('{}-{}'.format(testClassName,
                                                                 moduleName))
                    continue
                else:
                    rpObj.ingoreFeature.extend(tempIngoreFeature)
            uiObj._LOGGER.info('{}_{} Test Start...'.format(testClassName,
                                                            moduleName))
            # 处理功能点
            for eachFeature in realFeatures:
                # 获取每个测试大类下测试模块有效测试功能点名称
                featureName = eachFeature['featureName']
                steps = eachFeature['featureSteps']
                otherEventSuit = []
                if featureName == '首次启动app':
                    # 首次启动事件分割
                    pre_firstEventSuit, nor_firstEventSuit = firstStartHandle(steps)
                else:
                    for eachStep in steps:
                        otherEventSuit.append(creatEvent(eachStep))
                    # 用例拼接名
                    rName = '{}-{}-{}'.format(testClassName,
                                              moduleName,
                                              featureName)
                    # 转换非法字符
                    tName = replaceIllegalCharacter(rName)
                    # 开始测试
                    try:
                        # 清理安卓机的 log
                        os.popen('{} -c'.format(CC.ANDROIDLOG))

                        # 启动子进程为case录制视频，华为手机无此功能
                        if 'HONOR' not in df and 'HUAWEI' not in df:
                            childP = Process(target=screenRecordForFeature,
                                             args=(rName, uiObj, rpObj,))
                            childP.start()
                        if testClassName == 'ad':
                            uiObj.startApp()
                            executeEvent(otherEventSuit, uiObj,
                                         3, imgDict)
                        else:
                            uiObj.startApp()
                            time.sleep(10)
                            # 循环点击权限弹窗
                            popOutHandle(pre_firstEventSuit, uiObj, imgDict)
                            executeEvent(nor_firstEventSuit, uiObj,
                                         3, imgDict)
                            executeEvent(otherEventSuit, uiObj,
                                         3, imgDict)
                    except AssertionError as e:
                        uiObj._LOGGER.info('{}: FAIL'.format(rName))
                        rpObj.realFailTag = 1
                        rpObj.failList.append(rName)
                        rpObj.failCount += 1
                    except (IndexError, ValueError) as e:
                        uiObj._LOGGER.info(
                            u'{}: FAIL(注意: 功能点用例中存在不合法的参数！) 错误详情: {}'
                            .format(rName, e.args[0]))
                        rpObj.abortList.append(rName)
                        rpObj.abortCount += 1
                    except (selenium.common.exceptions.WebDriverException,
                            urllib2.URLError) as e:
                        uiObj._LOGGER.info(u'{}:FAIL(causeByAppium).错误详情:{}'
                                           .format(rName, str(e).strip()))
                        uiObj.appiumErrorHandle()
                        uiObj = UITest(configData)
                        time.sleep(10)
                        rpObj.exceptionList.append(rName)
                        rpObj.exceptionCount += 1
                    else:
                        uiObj._LOGGER.info(u'{}-{}-{}: PASS'.format(
                                                        testClassName,
                                                        moduleName,
                                                        featureName))
                        rpObj.passCount += 1
                    finally:
                        # 结束录屏
                        if childP is not None:
                            rpObj.childPK.put_nowait('1')
                            childP.join(3)
                            if childP.is_alive():
                                childP.terminate()
                            emptyQueue(rpObj.childPQ)
                            emptyQueue(rpObj.childPK)
                        # 检测是否为正常失败
                        if rpObj.realFailTag == 1:
                            # 截图
                            uiObj.screencap('{}_fail'.format(rName),
                                            CC.PHONE_PATH)
                            # 输出本次测试安卓产生的 log 到指定文件中
                            os.popen('{} -d > {}'.format(CC.ANDROIDLOG,
                                                         os.path.join(
                                                          androidLogField,
                                                          '{}.txt'.format(tName))))
                            rpObj.realFailTag = 0
                        else:
                            # 其他情况，删除录屏文件夹
                            os.popen('{} rm -rf sdcard/AutoTest/screenrecord/{}'
                                     .format(CC.PHONE_SHELL, tName))
                        rpObj.totalCount += 1
                        if testClassName == 'ad':
                            uiObj.clearApp(isAD=True)
                            uiObj.pressHome()
                        else:
                            uiObj.clearApp()
                        time.sleep(5)
            uiObj._LOGGER.info('{}_{} Test End...'.format(testClassName,
                                                          moduleName))
    uiObj.set_ime()
    # 打印报告
    showReport(rpObj)
