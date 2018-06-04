# -*- coding:utf-8 -*-
import time
import urllib2
from functools import wraps
import selenium
from action import Action
from uiBase import UITest
from commandContainer import CommandContainer as CC


def exceptionHandle(func):
    '''
    异常1: 点击时找不到id控件
    异常2: 点击时找不到name控件
    异常3: 点击时找不到xpath控件
    异常4: 文本输入失败
    异常5: 判断失败
    异常6: 点击判等失败
    异常7: 点击判不等失败
    异常8: 等待控件超时
    '''
    @wraps(func)
    def tempFunc(*args, **kwargs):
        '''
        错误类型集合
        '''
        try:
            func(*args, **kwargs)
        except AssertionError as e:
            flowTag = e.args[0]
            if flowTag == 1:
                elType, controlEl = args[0].strip().split('=')
                raise AssertionError(u"找不到你输入的id: {}，请确认!"
                                     .format(controlEl))
            elif flowTag == 2:
                elType, controlEl = args[0].strip().split('=')
                raise AssertionError(u"找不到你输入的name: {}，请确认!"
                                     .format(controlEl))
            elif flowTag == 3:
                elType, controlEl = args[0].strip().split('=')
                raise AssertionError(u"找不到你输入的xpath: {}，请确认!"
                                     .format(controlEl))
            elif flowTag == 4:
                raise AssertionError(u"文本: {} 输入失败，请确认!"
                                     .format(args[1]))
            elif flowTag == 5:
                raise AssertionError('{}_fail'.format(args[1]))
            elif flowTag == 6:
                elType, controlEl = args[0].strip().split('=')
                raise AssertionError('点击操作后，此元素{}的text值发生改变，fail'.format(
                                                                    controlEl))
            elif flowTag == 7:
                elType, controlEl = args[0].strip().split('=')
                raise AssertionError('点击操作后，此元素{}的text值未发生改变，fail'.format(
                                                                    controlEl))
            elif flowTag == 8:
                controlData = control.strip().split('-')
                raise AssertionError('规定时间内，仍未找到该元素: {}，fail'.format(
                                                            controlData[1]))
            else:
                raise RuntimeError('不存在的异常类型')
    return tempFunc


def transferProperty(target, key, source):
    '''
    动态的向某个类写入属性
    target: 类
    key: 属性名
    source: 字典
    '''
    if key in source:
        setattr(target, key, source.get(key))


def detailPrint(detailName, targetList):
    '''
    适配输出测试结果
    '''
    if len(targetList) != 0:
        print('{}:'.format(detailName))
        for i in targetList:
            print('\t{}'.format(i))
        print('='*60)


def setPara(stepEvent, stepAction):
    '''
    步骤事件类写入属性
    '''
    transferProperty(stepEvent, 'controlType', stepAction)
    transferProperty(stepEvent, 'inputText', stepAction)
    transferProperty(stepEvent, 'controlAction', stepAction)
    transferProperty(stepEvent, 'expectation', stepAction)
    transferProperty(stepEvent, 'expectationLog', stepAction)
    transferProperty(stepEvent, 'optional', stepAction)


def creatEvent(stepAction):
    '''
    创建步骤事件
    '''
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
    '''
    前提参数处理
    '''
    preJudgeVal = False
    if '==' in pre:
        preElType, preEl = pre.strip().split('==')
        if preElType == 'Id':
            preJudgeVal = uiObj.isIdInPage(preEl, totalTime=totalTime)
        elif preElType == 'name':
            preJudgeVal = uiObj.isNameInPage(preEl, totalTime=totalTime)
        elif preElType == 'xpath':
            preJudgeVal = uiObj.isXpathInPage(preEl, totalTime=totalTime)
        else:
            raise ValueError('前提参数:{}控件类型不合法,提醒:可能存在空格'.format(pre))
    elif '!=' in pre:
        preElType, preEl = pre.strip().split('!=')
        if preElType == 'Id':
            preJudgeVal = not uiObj.isIdInPage(preEl, totalTime=totalTime)
        elif preElType == 'name':
            preJudgeVal = not uiObj.isNameInPage(preEl, totalTime=totalTime)
        elif preElType == 'xpath':
            preJudgeVal = not uiObj.isXpathInPage(preEl, totalTime=totalTime)
        else:
            raise ValueError('前提参数:{}控件类型不合法,提醒:可能存在空格'.format(pre))
    else:
        raise ValueError('前提参数:{}不合法, 提醒:可能存在中文符号'.format(pre))
    return preJudgeVal


@exceptionHandle
def actionHandle(control, data, realAction, uiObj):
    '''
    动作处理
    '''
    if realAction == 'click':
        paraList = []
        paraDict = {}
        if ',' in control:
            paraList = control.strip().split(',')
        elif ',' not in control and '=' in control:
            paraList.append(control)
        elif '-' in control:
            posList = control.strip().split('-')
            uiObj.clickByPos(posList[0], posList[1])
        else:
            raise ValueError('动作参数:{}不合法, 提醒:可能存在中文符号'.format(control))
        if paraList:
            for eachPara in paraList:
                if '=' in eachPara:
                    paraKey, paraValue = eachPara.strip().split('=')
                    paraDict[paraKey] = paraValue
                else:
                    raise ValueError('动作参数:{}不合法，提醒:肯存在中文符号'.format(eachPara))
            if 'Id' in paraDict:
                if 'rule' in paraDict and 'ins' not in paraDict:
                    uiObj.clickByText(text=paraDict['Id'],
                                      rule=paraDict['rule'])
                elif 'rule' in paraDict and 'ins' in paraDict:
                    uiObj.clickByTextInstance(text=paraDict['Id'],
                                              rule=paraDict['rule'],
                                              ins=paraDict['ins'])
                elif 'rule' not in paraDict and 'ins' in paraDict:
                    uiObj.clickByTextInstance(text=paraDict['Id'],
                                              ins=paraDict['ins'])
                else:
                    uiObj.clickByText(text=paraDict['text'])
            elif 'name' in paraDict:
                if 'rule' in paraDict and 'ins' not in paraDict:
                    uiObj.clickByDesc(desc=paraDict['name'],
                                      rule=paraDict['rule'])
                elif 'rule' in paraDict and 'ins' in paraDict:
                    uiObj.clickByDescInstance(desc=paraDict['name'],
                                              rule=paraDict['rule'],
                                              ins=paraDict['ins'])
                elif 'rule' not in paraDict and 'ins' in paraDict:
                    uiObj.clickByDescInstance(desc=paraDict['name'],
                                              ins=paraDict['ins'])
                else:
                    uiObj.clickByDesc(desc=paraDict['name'])
            elif 'xpath' in paraDict:
                if 'ins' in paraDict:
                    uiObj.clickByIdInstance(Id=paraDict['xpath'],
                                            ins=paraDict['ins'])
                else:
                    uiObj.clickById(Id=paraDict['xpath'])
            else:
                raise ValueError('动作参数:{}中的控件类型不合法,提醒:可能存在空格'.format(control))
    elif realAction == 'swipe':
        posList = control.strip().split('-')
        uiObj.swipeByPos(posList[0], posList[1], posList[2], posList[3])
    elif realAction == 'drag':
        d_start, d_end = control.strip().split('&&')
        el_start = d_start.split('=')[1]
        el_end = d_end.split('=')[1]
        uiObj.dragByElement(el_start=el_start, el_end=el_end)
    elif realAction == 'typewrite':
        if control == '':
            uiObj.set_input_text(data)
        else:
            elType, controlEl = control.strip().split('=')
            if elType == 'text':
                uiObj.setValueByText(data, controlEl)
            elif elType == 'desc':
                uiObj.setValueByDesc(data, controlEl)
            elif elType == 'Id':
                uiObj.setValueById(data, controlEl)
            else:
                raise ValueError('动作参数:{}中的控件类型不合法,提醒:可能存在空格'.format(control))
    elif realAction == 'scroll':
        elType, controlEl = control.strip().split('=')
        if elType == 'Id':
            uiObj.scrollByElement(text=controlEl)
        elif elType == 'name':
            uiObj.scrollByElement(desc=controlEl)
        elif elType == 'xpath':
            uiObj.scrollByElement(Id=controlEl)
        else:
            raise ValueError('动作参数:{}中的控件类型不合法,提醒:可能存在空格'.format(control))
    elif realAction == 'scroll&&click':
        elType, controlEl = control.strip().split('=')
        if elType == 'Id':
            uiObj.scrollByElement(Id=controlEl)
            uiObj.clickByText(controlEl)
        elif elType == 'name':
            uiObj.scrollByElement(name=controlEl)
            uiObj.clickByDesc(controlEl)
        elif elType == 'xpath':
            uiObj.scrollByElement(xpath=controlEl)
            uiObj.clickById(controlEl)
        else:
            raise ValueError('动作参数:{}中的控件类型不合法,提醒:可能存在空格'.format(control))
    elif realAction == 'sleep':
        if '-' in control:
            controlData = control.strip().split('-')
            if len(controlData) == 2:
                t, el = controlData
                uiObj.sleep(t, el=el)
            elif len(controlData) == 3:
                t, el, refreshTime = controlData
                uiObj.sleep(t, el=el, refresh_time=refreshTime)
            else:
                raise ValueError('动作参数:{}不合法, 提醒:可能存在中文符号'.format(control))
        else:
            uiObj.sleep(int(control))
    elif realAction == 'click&&equal':
        elType, controlEl = control.strip().split('=')
        textBefore = uiObj.getTextById(controlEl)
        uiObj.clickById(controlEl)
        textAfter = uiObj.getTextById(controlEl)
        if textBefore == textAfter:
            pass
        else:
            raise AssertionError(6)
    elif realAction == 'click&&unequal':
        elType, controlEl = control.strip().split('=')
        textBefore = uiObj.getTextById(controlEl)
        uiObj.clickById(controlEl)
        textAfter = uiObj.getTextById(controlEl)
        if textBefore != textAfter:
            pass
        else:
            raise AssertionError(7)
    elif realAction == 'back':
        uiObj.pressBack()
    else:
        raise ValueError('不存在的动作类型:{},提醒:可能存在空格'.format(realAction))


def expectTypeHandle(expect, expectInfo, uiObj):
    '''
    期望元素处理
    '''
    expectVal = False
    if '==' in expect:
        expectEl = expect.strip().split('==')[1]
        try:
            if 'Id' in expect:
                uiObj.isExistById(expectEl, expectInfo)
            elif 'name' in expect:
                uiObj.isExistByName(expectEl, expectInfo)
            elif 'xpath' in expect:
                uiObj.isExistByXpath(expectEl, expectInfo)
            else:
                raise ValueError('期望参数:{}中的控件类型不合法'.format(expect))
            expectVal = True
        except AssertionError as e:
            pass
    elif '!=' in expect:
        expectEl = expect.strip().split('!=')[1]
        try:
            if 'Id' in expect:
                uiObj.isExistById(expectEl, expectInfo, isIn=1)
            elif 'name' in expect:
                uiObj.isExistByName(expectEl, expectInfo, isIn=1)
            elif 'xpath' in expect:
                uiObj.isExistByXpath(expectEl, expectInfo, isIn=1)
            else:
                raise ValueError('期望参数:{}中的控件类型不合法'.format(expect))
            expectVal = True
        except AssertionError as e:
            pass
    else:
        raise ValueError('期望参数:{}不合法, 提醒:可能存在中文符号'.format(expect))
    return expectVal


@exceptionHandle
def expectHandle(expect, expectInfo, uiObj):
    '''
    期望处理
    '''
    condition = []
    if '&&' in expect:
        for eveExpect in expect.strip().split('&&'):
            tempData = expectTypeHandle(eveExpect, expectInfo, uiObj)
            condition.append(tempData)
        if condition[0] and condition[1]:
            uiObj._LOGGER.debug('{}， 结束'.format(expectInfo))
        else:
            raise AssertionError(5)
    elif '||' in expect:
        for eveExpect in expect.strip().split('||'):
            tempData = expectTypeHandle(eveExpect, expectInfo, uiObj)
            condition.append(tempData)
        if condition[0] or condition[1]:
            uiObj._LOGGER.debug('{}， 结束'.format(expectInfo))
        else:
            raise AssertionError(5)
    else:
        if expectTypeHandle(expect, expectInfo, uiObj):
            uiObj._LOGGER.debug('{}， 结束'.format(expectInfo))
        else:
            raise AssertionError(5)


def executeEvent(stepEventSuit, uiObj, totalTime=0):
    '''
    执行动作事件
    '''
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
                    actionHandle(control, data, realAction.strip(), uiObj)
                if expect != '':
                    expectHandle(expect, expectInfo, uiObj)
            except AssertionError as e:
                if isOptional == '1.0':
                    pass
                else:
                    uiObj._LOGGER.error(e)
                    raise


def test_run_all_test(allTestClass, realIngoreModule, configData, uiObj):
    '''
    执行所有用例
    '''
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
    # 忽略详情列表
    ingoreFeature = []
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
            # 出去忽略模块实际要跑的功能点集合
            realFeatures = []
            # 此模块下忽略的功能点
            tempIngoreFeature = []
            # 此模块下忽略功能点数目
            ingoreFeaturesNum = 0
            firstEventSuit = []
            # 首次启动app中的步骤分割
            pre_firstEventSuit = []
            nor_firstEventSuit = []
            # 检测模块中的功能点是否被全部忽略
            for tempFeature in features:
                if '#' in tempFeature['featureName']:
                    rfeatureName = featureName.strip().split('#')[1]
                    rPath = '{}-{}-{}'.format(testClassName,
                                              moduleName,
                                              rfeatureName)
                    tempIngoreFeature.append(rPath)
                    ingoreFeaturesNum += 1
                else:
                    realFeatures.append(tempFeature)
            # 主app和广告业务逻辑不同
            if testClassName == 'ad':
                if len(features) == ingoreFeaturesNum:
                    print('警告: 模块:{}的所有功能点都被你忽略，默认你忽略了此模块。'
                          .format(moduleName))
                    realIngoreModule.append('{}-{}'.format(testClassName,
                                                           moduleName))
                    continue
                else:
                    ingoreFeature.extend(tempIngoreFeature)
            else:
                if len(features) == ingoreFeaturesNum+1:
                    print('警告: 模块:{}的所有功能点都被你忽略，默认你忽略了此模块。'
                          .format(moduleName))
                    realIngoreModule.append('{}-{}'.format(testClassName,
                                                           moduleName))
                    continue
                else:
                    ingoreFeature.extend(tempIngoreFeature)
            uiObj._LOGGER.info('{}_{} Test Start...'.format(testClassName,
                                                            moduleName))
            # 处理功能点
            for eachFeature in realFeatures:
                # 获取每个测试大类下测试模块有效测试功能点名称
                featureName = eachFeature['featureName']
                steps = eachFeature['featureSteps']
                otherEventSuit = []
                if featureName == '首次启动app':
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
                else:
                    for eachStep in steps:
                        otherEventSuit.append(creatEvent(eachStep))
                    rName = '{}-{}-{}'.format(testClassName,
                                              moduleName,
                                              featureName)
                    # 开始测试
                    try:
                        if testClassName == 'ad':
                            uiObj.startApp()
                            executeEvent(otherEventSuit, uiObj, 3)
                        else:
                            uiObj.startApp()
                            time.sleep(10)
                            # 循环点击权限弹窗
                            numCount = 10
                            while numCount > 0:
                                executeEvent(pre_firstEventSuit, uiObj)
                                time.sleep(1)
                                if uiObj.isTextInPage('首页'):
                                    break
                                else:
                                    numCount -= 1
                            else:
                                uiObj._LOGGER.debug('点击app弹窗失败，请检测app控件名是否正确！')
                            executeEvent(nor_firstEventSuit, uiObj, 3)
                            executeEvent(otherEventSuit, uiObj, 3)
                    except AssertionError as e:
                        uiObj._LOGGER.info('{}: FAIL'.format(rName))
                        uiObj.screencap('{}_fail'.format(rName),
                                        CC.PHONE_PATH)
                        failList.append(rName)
                        failCount += 1
                    except (IndexError, ValueError) as e:
                        uiObj._LOGGER.info(
                            '{}: FAIL(注意: 功能点用例中存在不合法的参数！)\n错误详情: {}'
                            .format(rName, e.args[0]))
                        # uiObj._LOGGER.exception('错误详情')
                        abortList.append(rName)
                        abortCount += 1
                    except (selenium.common.exceptions.WebDriverException,
                            URLError) as e:
                        uiObj._LOGGER.info('{}:FAIL(causeByAppium).错误详情:{}'
                                           .format(rName, str(e).strip()))
                        uiObj.testExit()
                        uiObj.appiumErrorHandle()
                        uiObj = UITest(configData)
                        time.sleep(10)
                        exceptionList.append(rName)
                        exceptionCount += 1
                    else:
                        uiObj._LOGGER.info('{}-{}-{}: PASS'.format(
                                                        testClassName,
                                                        moduleName,
                                                        featureName))
                        passCount += 1
                    finally:
                        totalCount += 1
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
    print('总共: {}个\n成功: {}个\n失败: {}个\n中止: {}个\n异常: {}个\n'.format(totalCount,
                                                                 passCount,
                                                                 failCount,
                                                                 abortCount,
                                                                 exceptionCount
                                                                 ))
    detailPrint('失败用例', failList)
    detailPrint('中止用例', abortList)
    detailPrint('异常用例', exceptionList)
    if realIngoreModule != []:
        detailPrint('忽略模块', realIngoreModule)
    if ingoreFeature != []:
        detailPrint('忽略功能点', ingoreFeature)
