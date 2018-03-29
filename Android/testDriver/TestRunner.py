# -*- coding:utf-8 -*-
import selenium
from action import Action


def transferProperty(target, key, source):
    if key in source:
        setattr(target, key, source.get(key))


# def parseCaseSuit(allTestClass):
#     if not isinstance(allTestClass, list):

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
        pass


def actionHandle(control, data, realAction, uiObj):
    if realAction == 'click':
        if '=' in control:
            elType, controlEl = control.strip().split('=')
            if elType == 'text':
                uiObj.clickByText(controlEl, flowTag=1)
            elif elType == 'desc':
                uiObj.clickByDesc(controlEl, flowTag=1)
            elif elType == 'Id':
                uiObj.clickById(controlEl, flowTag=1)
            else:
                pass
        elif '-' in control:
            posList = control.strip().split('-')
            uiObj.clickByPos(posList[0], posList[1])
        else:
            pass
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
                pass
    elif realAction == 'scroll&&click':
        elType, controlEl = control.strip().split('=')
        if elType == 'text':
            uiObj.scrollByElement(text=controlEl)
        elif elType == 'desc':
            uiObj.scrollByElement(desc=controlEl)
        elif elType == 'Id':
            uiObj.scrollByElement(Id=controlEl)
        else:
            pass
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
                pass
        else:
            uiObj.sleep(int(control))
    elif realAction == 'back':
        uiObj.pressBack()
    else:
        pass


def expectTypeHandle(expect, expectInfo, uiObj):
    if '==' in expect:
        expectEl = expect.strip().split('==')[1]
        if 'text' in expect:
            uiObj.isExistByText(expectEl, expectInfo, 0)
        elif 'desc' in expect:
            uiObj.isExistByDesc(expectEl, expectInfo, 0)
        elif 'Id' in expect:
            uiObj.isExistById(expectEl, expectInfo, 0)
    elif '!=' in expect:
        expectEl = expect.strip().split('!=')[1]
        if 'text' in expect:
            uiObj.isExistByText(expectEl, expectInfo, 1)
        elif 'desc' in expect:
            uiObj.isExistByDesc(expectEl, expectInfo, 1)
        elif 'Id' in expect:
            uiObj.isExistById(expectEl, expectInfo, 1)
    else:
        pass


def expectHandle(expect, expectInfo, uiObj):
    condition = []
    if '&&' in expect:
        for eveExpect in expect.strip().split('&&'):
            try:
                expectTypeHandle(eveExpect, expectInfo, uiObj)
            except AssertionError as e:
                condition.append(False)
            else:
                condition.append(True)
        if condition[0] and condition[1]:
            pass
        else:
            raise AssertionError
    elif '||' in expect:
        for eveExpect in expect.strip().split('||'):
            try:
                expectTypeHandle(eveExpect, expectInfo, uiObj)
            except AssertionError as e:
                condition.append(False)
            else:
                condition.append(True)
        if condition[0] or condition[1]:
            pass
        else:
            raise AssertionError
    else:
        expectTypeHandle(expect, expectInfo, uiObj)


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
                    raise


def test_run_all_test(allTestClass, uiObj):
    totalCount = 0
    passCount = 0
    failCount = 0
    abortCount = 0
    exceptionCount = 0
    failList = []
    abortList = []
    exceptionList = []
    for eachTestClass in allTestClass:
        testClassName = eachTestClass['testCaseName']
        testCase = eachTestClass['modleSuit']
        for eachModle in testCase:
            moduleName = eachModle['moduleName']
            features = eachModle['featureSuite']
            firstEventSuit = []
            for eachFeature in features:
                featureName = eachFeature['featureName']
                steps = eachFeature['featureSteps']
                otherEventSuit = []
                if '#' in featureName:
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
                            print('{}: FAIL'.format(rName))
                            failList.append(rName)
                            failCount += 1
                            continue
                        except (IndexError, ValueError):
                            print(u'这个功能点用例中可能存在不合法的参数，请核查！\n{}: FAIL'
                                  .format(rName))
                            abortList.append(rName)
                            abortCount += 1
                        except selenium.common.exceptions.WebDriverException:
                            print('{}: FAIL(causeByAppium)'.format(rName))
                            uiObj.appiumErrorHandle()
                            exceptionList.append(rName)
                            exceptionCount += 1
                            continue
                        else:
                            print('{}-{}-{}: PASS'.format(testClassName,
                                                          moduleName,
                                                          featureName))
                            passCount += 1
                        finally:
                            totalCount += 1
                            uiObj.clearApp()
                            uiObj.sleep(5)
    uiObj.set_ime()
    print('总共：{}个\n成功：{}个\n失败：{}个\n中止：{}个\n异常：{}个\n'.format(totalCount,
                                                            passCount,
                                                            failCount,
                                                            abortCount,
                                                            exceptionCount))
    detailPrint('失败用例', failList)
    detailPrint('中止用例', abortList)
    detailPrint('异常用例', exceptionList)
