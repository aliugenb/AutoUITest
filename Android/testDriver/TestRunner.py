# -*- coding:utf-8 -*-
import selenium
from action import Action
import common
common.pathGet()
from XFramework.ui_base import UITest
from XFramework.command_container import CommandContainer as CC


def transferProperty(target, key, source):
    if key in source:
        setattr(target, key, source.get(key))


def detailPrint(detailName, targetList):
    if len(targetList) != 0:
        print('{}:'.format(detailName))
        for i in targetList:
            print('\t{}'.format(i))
        print('='*60)


def setPara(stepEvent, stepAction):
    transferProperty(stepEvent, 'controlType', stepAction)
    transferProperty(stepEvent, 'inputText', stepAction)
    transferProperty(stepEvent, 'controlAction', stepAction)
    transferProperty(stepEvent, 'expectation', stepAction)
    transferProperty(stepEvent, 'expectationLog', stepAction)
    transferProperty(stepEvent, 'optional', stepAction)


def creatEvent(stepAction):
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
        raise ValueError


def actionHandle(control, data, realAction, uiObj):
    if realAction == 'click':
        if '=' in control:
            elType, controlEl = control.strip().split('=')
            if elType == 'text':
                try:
                    uiObj.clickByText(controlEl, flowTag=1)
                except AssertionError as e:
                    try:
                        uiObj.clickByText(controlEl, flowTag=1, rule='p')
                    except AssertionError as e:
                        # uiObj._LOGGER.error(u"此页面找不到你输入的text：{}，请确认!"
                        #                     .format(controlEl))
                        raise AssertionError(u"此页面找不到你输入的text：{}，请确认!"
                                             .format(controlEl))
            elif elType == 'desc':
                uiObj.clickByDesc(controlEl, flowTag=1)
            elif elType == 'Id':
                uiObj.clickById(controlEl, flowTag=1)
            else:
                raise ValueError
        elif '-' in control:
            posList = control.strip().split('-')
            uiObj.clickByPos(posList[0], posList[1])
        else:
            raise ValueError
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
                raise ValueError
    elif realAction == 'scroll&&click':
        elType, controlEl = control.strip().split('=')
        if elType == 'text':
            uiObj.scrollByElement(text=controlEl)
        elif elType == 'desc':
            uiObj.scrollByElement(desc=controlEl)
        elif elType == 'Id':
            uiObj.scrollByElement(Id=controlEl)
        else:
            raise ValueError
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
                raise ValueError
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
            # uiObj._LOGGER.error('点击操作后，此元素{}的text值发生改变，fail'.format(
            #                                                         controlEl))
            Id_pic = controlEl.split('/')[1]
            raise AssertionError('点击操作后，此元素{}的text值发生改变，fail'.format(
                                                                    controlEl))
    elif realAction == 'click&&unequal':
        elType, controlEl = control.strip().split('=')
        textBefore = uiObj.getTextById(controlEl)
        uiObj.clickById(controlEl)
        textAfter = uiObj.getTextById(controlEl)
        if textBefore != textAfter:
            pass
        else:
            # uiObj._LOGGER.error('点击操作后，此元素{}的text值未发生改变，fail'.format(
            #                                                         controlEl))
            raise AssertionError('点击操作后，此元素{}的text值未发生改变，fail'.format(
                                                                    controlEl))
    elif realAction == 'back':
        uiObj.pressBack()
    else:
        raise ValueError


def getJudgeReturn(paraType, judgeCondition):
    if paraType == '==':
        if judgeCondition:
            return True
        else:
            return False
    elif paraType == '!=':
        if not judgeCondition:
            return True
        else:
            return False
    else:
        raise ValueError


def expectTypeHandle(expect, uiObj):
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
            raise ValueError
    elif '!=' in expect:
        expectEl = expect.strip().split('!=')[1]
        if 'text' in expect:
            expectVal = getJudgeReturn('!=', uiObj.isTextInPage(expectEl))
        elif 'desc' in expect:
            expectVal = getJudgeReturn('!=', uiObj.isDescInPage(expectEl))
        elif 'Id' in expect:
            expectVal = getJudgeReturn('!=', uiObj.isIdInPage(expectEl))
        else:
            raise ValueError
    else:
        raise ValueError
    if expectVal is None:
        raise ValueError
    else:
        return expectVal


def expectHandle(expect, expectInfo, uiObj):
    condition = []
    if '&&' in expect:
        for eveExpect in expect.strip().split('&&'):
            tempData = expectTypeHandle(eveExpect, uiObj)
            condition.append(tempData)
        if condition[0] and condition[1]:
            pass
        else:
            # uiObj._LOGGER.error('{}_fail'.format(expectInfo))
            raise AssertionError('{}_fail'.format(expectInfo))
    elif '||' in expect:
        for eveExpect in expect.strip().split('||'):
            tempData = expectTypeHandle(eveExpect, uiObj)
            condition.append(tempData)
        if condition[0] or condition[1]:
            pass
        else:
            # uiObj._LOGGER.error('{}_fail'.format(expectInfo))
            raise AssertionError('{}_fail'.format(expectInfo))
    else:
        if expectTypeHandle(expect, uiObj):
            pass
        else:
            # uiObj._LOGGER.error('{}_fail'.format(expectInfo))
            raise AssertionError('{}_fail'.format(expectInfo))


def executeEvent(stepEventSuit, uiObj):
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


def test_run_all_test(allTestClass, realIngoreModule, uiObj):
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
                    else:
                        for eachStep in steps:
                            otherEventSuit.append(creatEvent(eachStep))
                        stepEventSuit = firstEventSuit + otherEventSuit
                        rName = '{}-{}-{}'.format(testClassName,
                                                  moduleName,
                                                  featureName)
                        try:
                            uiObj.startApp()
                            uiObj.sleep(10)
                            executeEvent(stepEventSuit, uiObj)
                        except AssertionError as e:
                            uiObj._LOGGER.info('{}: FAIL'.format(rName))
                            uiObj.screencap('{}_fail'.format(rName),
                                            CC.PHONE_PATH)
                            failList.append(rName)
                            failCount += 1
                        except (IndexError, ValueError):
                            uiObj._LOGGER.info(u'{}: FAIL(注意：功能点用例中存在不合法的参数！)'
                                               .format(rName))
                            abortList.append(rName)
                            abortCount += 1
                        except selenium.common.exceptions.WebDriverException:
                            uiObj._LOGGER.info('{}: FAIL(causeByAppium)'
                                               .format(rName))
                            uiObj.appiumErrorHandle()
                            uiObj = UITest()
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
