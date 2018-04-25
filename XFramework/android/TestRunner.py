# -*- coding:utf-8 -*-
import time
import selenium
from action import Action
from uiBase import UITest
from commandContainer import CommandContainer as CC


def exceptionHandle(func):
    '''
    异常1：点击时找不到text控件
    异常2：点击时找不到desc控件
    异常3：点击时找不到Id控件
    异常4：文本输入失败
    异常5：判断失败
    异常6：点击判等失败
    异常7：点击判不等失败
    异常8：等待控件超时
    '''
    def tempFunc(*args, **kwargs):
        try:
            func(*args, **kwargs)
        except AssertionError as e:
            flowTag = e.args[0]
            if flowTag == 1:
                elType, controlEl = args[0].strip().split('=')
                raise AssertionError(u"找不到你输入的text：{}，请确认!"
                                     .format(controlEl))
            elif flowTag == 2:
                elType, controlEl = args[0].strip().split('=')
                raise AssertionError(u"找不到你输入的desc：{}，请确认!"
                                     .format(controlEl))
            elif flowTag == 3:
                elType, controlEl = args[0].strip().split('=')
                raise AssertionError(u"找不到你输入的Id：{}，请确认!"
                                     .format(controlEl))
            elif flowTag == 4:
                raise AssertionError(u"文本：{} 输入失败，请确认!"
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


def preconditionHandle(pre, uiObj):
    '''
    前提参数处理
    '''
    if '==' in pre:
        preElType, preEl = pre.strip().split('==')
        if preElType == 'text':
            if not uiObj.isTextInPage(preEl):
                return True
        elif preElType == 'desc':
            if not uiObj.isDescInPage(preEl):
                return True
        elif preElType == 'Id':
            if not uiObj.isIdInPage(preEl):
                return True
    elif '!=' in pre:
        preElType, preEl = pre.strip().split('!=')
        if preElType == 'text':
            if uiObj.isTextInPage(preEl):
                return True
        elif preElType == 'desc':
            if uiObj.isDescInPage(preEl):
                return True
        elif preElType == 'Id':
            if uiObj.isIdInPage(preEl):
                return True
    else:
        raise ValueError('参数:{}不合法, 提醒:可能存在中文符号'.format(pre))


@exceptionHandle
def actionHandle(control, data, realAction, uiObj):
    '''
    动作处理
    '''
    if realAction == 'click':
        if '=' in control:
            elType, controlEl = control.strip().split('=')
            if elType == 'text':
                try:
                    uiObj.clickByText(controlEl, flowTag=1)
                except AssertionError as e:
                    uiObj.clickByText(controlEl, flowTag=1, rule='p')
            elif elType == 'desc':
                uiObj.clickByDesc(controlEl, flowTag=1)
            elif elType == 'Id':
                uiObj.clickById(controlEl, flowTag=1)
            else:
                raise ValueError('参数:{}中的控件类型不合法'.format(control))
        elif '-' in control:
            posList = control.strip().split('-')
            uiObj.clickByPos(posList[0], posList[1])
        else:
            raise ValueError('参数:{}不合法, 提醒:可能存在中文符号'.format(control))
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
                raise ValueError('参数:{}中的控件类型不合法'.format(control))
    elif realAction == 'scroll&&click':
        elType, controlEl = control.strip().split('=')
        if elType == 'text':
            uiObj.scrollByElement(text=controlEl)
        elif elType == 'desc':
            uiObj.scrollByElement(desc=controlEl)
        elif elType == 'Id':
            uiObj.scrollByElement(Id=controlEl)
        else:
            raise ValueError('参数:{}中的控件类型不合法'.format(control))
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
                raise ValueError('参数:{}不合法, 提醒:可能存在中文符号'.format(control))
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
        raise ValueError('不存在的动作类型:{}'.format(realAction))


def getJudgeReturn(paraType, judgeCondition):
    '''
    判断处理
    '''
    judgeVal = False
    totalNum = 10
    while totalNum > 0:
        if paraType == '==':
            if judgeCondition:
                judgeVal = True
                break
            else:
                pass
        elif paraType == '!=':
            if not judgeCondition:
                judgeVal = True
                break
            else:
                pass
        else:
            raise ValueError('不存在的判断类型:{}'.format(paraType))
        time.sleep(1)
        totalNum -= 1
    return judgeVal


def expectTypeHandle(expect, uiObj):
    '''
    期望元素处理
    '''
    expectVal = None
    if '==' in expect:
        expectEl = expect.strip().split('==')[1]
        if 'text' in expect:
            expectVal = getJudgeReturn('==', uiObj.isTextInPage(expectEl))
        elif 'desc' in expect:
            expectVal = getJudgeReturn('==', uiObj.isDescInPage(expectEl))
        elif 'Id' in expect:
            expectVal = getJudgeReturn('==', uiObj.isIdInPage(expectEl))
        else:
            raise ValueError('参数:{}中的控件类型不合法'.format(expect))
    elif '!=' in expect:
        expectEl = expect.strip().split('!=')[1]
        if 'text' in expect:
            expectVal = getJudgeReturn('!=', uiObj.isTextInPage(expectEl))
        elif 'desc' in expect:
            expectVal = getJudgeReturn('!=', uiObj.isDescInPage(expectEl))
        elif 'Id' in expect:
            expectVal = getJudgeReturn('!=', uiObj.isIdInPage(expectEl))
        else:
            raise ValueError('参数:{}中的控件类型不合法'.format(expect))
    else:
        raise ValueError('参数:{}不合法, 提醒:可能存在中文符号'.format(expect))
    return expectVal


@exceptionHandle
def expectHandle(expect, expectInfo, uiObj):
    '''
    期望处理
    '''
    condition = []
    if '&&' in expect:
        for eveExpect in expect.strip().split('&&'):
            tempData = expectTypeHandle(eveExpect, uiObj)
            condition.append(tempData)
        if condition[0] and condition[1]:
            uiObj._LOGGER.info('{}， 结束'.format(expectInfo))
        else:
            raise AssertionError(5)
    elif '||' in expect:
        for eveExpect in expect.strip().split('||'):
            tempData = expectTypeHandle(eveExpect, uiObj)
            condition.append(tempData)
        if condition[0] or condition[1]:
            uiObj._LOGGER.info('{}， 结束'.format(expectInfo))
        else:
            raise AssertionError(5)
    else:
        if expectTypeHandle(expect, uiObj):
            uiObj._LOGGER.info('{}， 结束'.format(expectInfo))
        else:
            raise AssertionError(5)


def executeEvent(stepEventSuit, uiObj):
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
                    if preconditionHandle(pre, uiObj):
                        break
                if realAction != '':
                    actionHandle(control, data, realAction, uiObj)
                if expect != '':
                    uiObj.sleep(2)
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
    totalCount = 0
    passCount = 0
    failCount = 0
    abortCount = 0
    exceptionCount = 0
    failList = []
    abortList = []
    exceptionList = []
    ingoreFeature = []
    for eachTestClass in allTestClass:
        testClassName = eachTestClass['testCaseName']
        testCase = eachTestClass['moduleSuit']
        for eachModule in testCase:
            moduleName = eachModule['moduleName']
            features = eachModule['featureSuite']
            firstEventSuit = []
            pre_firstEventSuit = []
            nor_firstEventSuit = []
            uiObj._LOGGER.info('{}_{} Test Start...'.format(testClassName,
                                                            moduleName))
            for eachFeature in features:
                featureName = eachFeature['featureName']
                steps = eachFeature['featureSteps']
                otherEventSuit = []
                if '#' in featureName:
                    rfeatureName = featureName.strip().split('#')[1]
                    rPath = '{}-{}-{}'.format(testClassName,
                                              moduleName,
                                              rfeatureName)
                    ingoreFeature.append(rPath)
                    continue
                else:
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
                        # stepEventSuit = firstEventSuit + otherEventSuit
                        rName = '{}-{}-{}'.format(testClassName,
                                                  moduleName,
                                                  featureName)
                        try:
                            uiObj.startApp()
                            uiObj.sleep(10)
                            # executeEvent(stepEventSuit, uiObj)
                            numCount = 10
                            while numCount > 0:
                                executeEvent(pre_firstEventSuit, uiObj)
                                uiObj.sleep(1)
                                if uiObj.isTextInPage('首页'):
                                    break
                                else:
                                    numCount -= 1
                            else:
                                uiObj._LOGGER.debug('点击app弹窗失败，请检测app控件名是否正确！')
                            executeEvent(nor_firstEventSuit, uiObj)
                            executeEvent(otherEventSuit, uiObj)
                        except AssertionError as e:
                            uiObj._LOGGER.info('{}: FAIL'.format(rName))
                            uiObj.screencap('{}_fail'.format(rName),
                                            CC.PHONE_PATH)
                            failList.append(rName)
                            failCount += 1
                        except (IndexError, ValueError) as e:
                            uiObj._LOGGER.info(
                                '{}: FAIL(注意：功能点用例中存在不合法的参数！)\n错误详情：{}'
                                .format(rName, e.args[0]))
                            # uiObj._LOGGER.exception('错误详情')
                            abortList.append(rName)
                            abortCount += 1
                        except selenium.common.exceptions.WebDriverException:
                            uiObj._LOGGER.info('{}: FAIL(causeByAppium)'
                                               .format(rName))
                            uiObj.appiumErrorHandle()
                            uiObj = UITest(configData)
                            uiObj.sleep(10)
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
                            uiObj.clearApp()
                            uiObj.sleep(5)
            uiObj._LOGGER.info('{}_{} Test End...'.format(testClassName,
                                                          moduleName))
    uiObj.set_ime()
    print('总共：{}个\n成功：{}个\n失败：{}个\n中止：{}个\n异常：{}个\n'.format(totalCount,
                                                            passCount,
                                                            failCount,
                                                            abortCount,
                                                            exceptionCount))
    detailPrint('失败用例', failList)
    detailPrint('中止用例', abortList)
    detailPrint('异常用例', exceptionList)
    if realIngoreModule != []:
        detailPrint('忽略模块', realIngoreModule)
    if ingoreFeature != []:
        detailPrint('忽略功能点', ingoreFeature)
