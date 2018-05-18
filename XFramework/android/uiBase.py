# -*- coding:utf-8 -*-
import os, sys, time
import selenium.common.exceptions
from appium.webdriver.common.touch_action import TouchAction as TA
import phoneInfo as pi
import baseOn
from baseOn import BaseOn
from commandContainer import CommandContainer as CC


def setDefaultPara(func):
    '''
    给某些函数添加默认的值
    kwargs参数:
        refresh_time: 刷新时间
        totalTime: 等待总时间
        flowTag: 新旧标志，默认为0，0代表执行不等待直接点击，1代表执行等待点击
    '''
    def tempFunc(*args, **kwargs):
        if 'refresh_time' not in kwargs:
            kwargs['refresh_time'] = 1
        if 'totalTime' not in kwargs:
            kwargs['totalTime'] = 10
        if 'flowTag' not in kwargs:
            kwargs['flowTag'] = '1'
        return func(*args, **kwargs)
    return tempFunc


class UITest(BaseOn, TA):
    """
    ui层基本操作
    """

    def __init__(self, configData=None, driver=None):
        self.configData = configData
        if self.configData is not None:
            self.driver = pi.getDriver(self.configData)
        else:
            self.driver = pi.getDriver()
        TA.__init__(self, driver=self.driver)

    def clickByPos(self, x, y, duration=None):
        """
        通过坐标点击；duration为持续时间，单位ms
        """
        self.driver.tap([(x, y)], duration)
        time.sleep(1)
        self._LOGGER.debug(u'点击坐标结束')

    def swipeByPos(self, start_x, start_y, end_x, end_y, duration=None):
        """
        通过坐标滑动；duration为持续时间，单位ms
        """
        self.driver.swipe(start_x, start_y, end_x, end_y, duration)
        time.sleep(1)
        self._LOGGER.debug(u'滑动结束')

    @setDefaultPara
    def clickByText(self, text, rule='e', *args, **kwargs):
        """
        通过控件的text属性点击；rule默认为e
        """
        if str(kwargs['flowTag']) == '1':
            try:
                self.sleep(kwargs['totalTime'],
                           refresh_time=kwargs['refresh_time'], text=text)
            except AssertionError as e:
                pass
        try:
            self.__select_text_Android(text, rule).click()
            self._LOGGER.debug(u'点击text: ' + text + u'，结束')
        except AttributeError as e:
            raise AssertionError(1)

    @setDefaultPara
    def clickByDesc(self, desc, rule='e', *args, **kwargs):
        """
        通过控件的desc属性点击；rule默认为e
        """
        if str(kwargs['flowTag']) == '1':
            try:
                self.sleep(kwargs['totalTime'],
                           refresh_time=kwargs['refresh_time'], desc=desc)
            except AssertionError as e:
                pass
        try:
            self.__select_desc_Android(desc, rule).click()
            self._LOGGER.debug(u'点击desc: ' + desc + u'，结束')
        except AttributeError as e:
            raise AssertionError(2)

    @setDefaultPara
    def clickById(self, Id, *args, **kwargs):
        """
        通过控件的id属性点击；
        """
        if str(kwargs['flowTag']) == '1':
            try:
                self.sleep(kwargs['totalTime'],
                           refresh_time=kwargs['refresh_time'], Id=Id)
            except AssertionError as e:
                pass
        try:
            self.__select_Id_Android(Id).click()
            self._LOGGER.debug(u'点击Id: ' + Id + u'，结束')
        except AttributeError as e:
            raise AssertionError(3)

    @setDefaultPara
    def clickByTextInstance(self, text, ins, rule='e', *args, **kwargs):
        """
        通过特定控件的text属性点击；ins为索引；rule默认为e
        """
        if str(kwargs['flowTag']) == '1':
            try:
                self.sleep(kwargs['totalTime'],
                           refresh_time=kwargs['refresh_time'], text=text)
            except AssertionError as e:
                pass
        try:
            self.__select_text_ins_Android(text, ins, rule).click()
            self._LOGGER.debug(u'点击text: {}, ins: {}, 结束'.format(text,
                                                                 str(ins)))
        except AttributeError as e:
            raise AssertionError(1)

    @setDefaultPara
    def clickByDescInstance(self, desc, ins, rule='e', *args, **kwargs):
        """
        通过特定控件的desc属性点击；ins为索引；rule默认为e
        """
        if str(kwargs['flowTag']) == '1':
            try:
                self.sleep(kwargs['totalTime'],
                           refresh_time=kwargs['refresh_time'], desc=desc)
            except AssertionError as e:
                pass
        try:
            self.__select_desc_ins_Android(desc, ins, rule).click()
            self._LOGGER.debug(u'点击desc: {}, ins: {}, 结束'.format(desc,
                                                                 str(ins)))
        except AttributeError as e:
            raise AssertionError(2)

    @setDefaultPara
    def clickByIdInstance(self, Id, ins, *args, **kwargs):
        """
        通过控件的id属性点击；ins为索引；
        """
        if str(kwargs['flowTag']) == '1':
            try:
                self.sleep(kwargs['totalTime'],
                           refresh_time=kwargs['refresh_time'], Id=Id)
            except AssertionError as e:
                pass
        try:
            self.__select_Id_ins_Android(Id, ins).click()
            self._LOGGER.debug(u'点击Id: {}, ins: {}, 结束'.format(Id, str(ins)))
        except AttributeError as e:
            raise AssertionError(3)

    @setDefaultPara
    def getTextById(self, Id, ins=None, *args, **kwargs):
        """
        通过Id查找控件，并获取它的text
        """
        if str(kwargs['flowTag']) == '1':
            try:
                self.sleep(kwargs['totalTime'],
                           refresh_time=kwargs['refresh_time'], Id=Id)
            except AssertionError as e:
                pass
        try:
            if ins is None:
                re_text = self.__select_Id_Android(Id).text
            else:
                re_text = self.__select_Id_ins_Android(Id, ins).text

            self._LOGGER.debug(u"获取text: {}, 结束".format(re_text))
            return re_text
        except AttributeError as e:
            raise AssertionError(3)

    @setDefaultPara
    def setValueByText(self, input_text, text, rule='e', *args, **kwargs):
        """
        通过控件的text属性输入文本；rule默认为e;input_text为你想输入文本，支持中英文
        """
        if str(kwargs['flowTag']) == '1':
            try:
                self.sleep(kwargs['totalTime'],
                           refresh_time=kwargs['refresh_time'], text=text)
            except AssertionError as e:
                pass
        try:
            self.__select_text_Android(text, rule).set_text(input_text)
            self._LOGGER.debug(u'T文本: ' + input_text + u'，输入结束')
        except AttributeError as e:
            raise AssertionError(4)

    @setDefaultPara
    def setValueByDesc(self, input_text, desc, rule='e', *args, **kwargs):
        """
        通过控件的desc属性输入文本；rule默认为e;input_text为你想输入文本，支持中英文
        """
        if str(kwargs['flowTag']) == '1':
            try:
                self.sleep(kwargs['totalTime'],
                           refresh_time=kwargs['refresh_time'], desc=desc)
            except AssertionError as e:
                pass
        try:
            self.__select_desc_Android(desc, rule).set_text(input_text)
            self._LOGGER.debug(u'D文本: ' + input_text + u'，输入结束')
        except AttributeError as e:
            raise AssertionError(4)

    @setDefaultPara
    def setValueById(self, input_text, Id, *args, **kwargs):
        """
        通过控件的Id属性输入文本；input_text为你想输入文本，支持中英文
        """
        if str(kwargs['flowTag']) == '1':
            try:
                self.sleep(kwargs['totalTime'],
                           refresh_time=kwargs['refresh_time'], Id=Id)
            except AssertionError as e:
                pass
        try:
            self.__select_Id_Android(Id).set_text(input_text)
            self._LOGGER.debug(u'I文本: ' + input_text + u'，输入结束')
        except AttributeError as e:
            raise AssertionError(4)

    @setDefaultPara
    def isTextInPage(self, text, rule='e', *args, **kwargs):
        """
        判断text元素是否存在，有返回值
        """
        if str(kwargs['flowTag']) == '1':
            try:
                self.sleep(kwargs['totalTime'],
                           refresh_time=kwargs['refresh_time'], text=text)
            except AssertionError as e:
                pass
        if self.__select_text_Android(text, rule):
            return True
        else:
            return False

    @setDefaultPara
    def isDescInPage(self, desc, rule='e', *args, **kwargs):
        """
        判断desc元素是否存在，有返回值
        """
        if str(kwargs['flowTag']) == '1':
            try:
                self.sleep(kwargs['totalTime'],
                           refresh_time=kwargs['refresh_time'], desc=desc)
            except AssertionError as e:
                pass
        if self.__select_desc_Android(desc, rule):
            return True
        else:
            return False

    @setDefaultPara
    def isIdInPage(self, Id, *args, **kwargs):
        """
        判断id元素是否存在，有返回值
        """
        if str(kwargs['flowTag']) == '1':
            try:
                self.sleep(kwargs['totalTime'],
                           refresh_time=kwargs['refresh_time'], Id=Id)
            except AssertionError as e:
                pass
        if self.__select_Id_Android(Id):
            return True
        else:
            return False

    @setDefaultPara
    def isExistByText(self, text, instruction, isIn=0, rule='e', *args, **kwargs):
        """
        通过控件的text属性判断操作是否成功，instruction为此处步骤描述内容；
        """
        # self._LOGGER.debug(instruction)
        if str(kwargs['flowTag']) == '1':
            try:
                self.sleep(kwargs['totalTime'],
                           refresh_time=kwargs['refresh_time'], text=text)
            except AssertionError as e:
                pass
        if int(isIn) == 0:
            if self.__select_text_Android(text, rule):
                pass
            else:
                raise AssertionError
        elif int(isIn) == 1:
            if not self.__select_text_Android(text, rule):
                pass
            else:
                raise AssertionError
        else:
            raise ValueError(u"参数输入有误，请确认后输入参数")

    @setDefaultPara
    def isExistByDesc(self, desc, instruction, isIn=0, rule='e', *args, **kwargs):
        """
        通过控件的desc属性判断操作是否成功，instruction为此处步骤描述内容；
        """
        # self._LOGGER.debug(instruction)
        if str(kwargs['flowTag']) == '1':
            try:
                self.sleep(kwargs['totalTime'],
                           refresh_time=kwargs['refresh_time'], desc=desc)
            except AssertionError as e:
                pass

        if int(isIn) == 0:
            if self.__select_desc_Android(desc, rule):
                pass
            else:
                raise AssertionError
        elif int(isIn) == 1:
            if not self.__select_desc_Android(desc, rule):
                pass
            else:
                raise AssertionError
        else:
            raise ValueError(u"参数输入有误，请确认后输入参数")

    @setDefaultPara
    def isExistById(self, Id, instruction, isIn=0, *args, **kwargs):
        """
        通过控件的id属性判断操作是否成功，instruction为此处步骤描述内容；
        """
        # self._LOGGER.debug(instruction)
        if str(kwargs['flowTag']) == '1':
            try:
                self.sleep(kwargs['totalTime'],
                           refresh_time=kwargs['refresh_time'], Id=Id)
            except AssertionError as e:
                pass
        if int(isIn) == 0:
            if self.__select_Id_Android(Id):
                pass
            else:
                raise AssertionError
        elif int(isIn) == 1:
            if not self.__select_Id_Android(Id):
                pass
            else:
                raise AssertionError
        else:
            raise ValueError(u"参数输入有误，请确认后输入参数")

    def sleep(self, t, *args, **kwargs):
        """
        等待时间，分隐性等待和强制等待，单位s；只有参数t为强制等待，
        有参数refresh_time和el为隐性等待，共等待t，refresh_time为刷新时间
        """
        # 获取调用此函数的脚本名
        backFileName = sys._getframe(1).f_code.co_filename
        if kwargs:
            try:
                timeCount = 0
                while timeCount <= t:
                    # 判断传入的控件类型
                    if 'text' in kwargs:
                        if self.__select_text_Android(kwargs['text'], 'e'):
                            break
                    elif 'desc' in kwargs:
                        if self.__select_desc_Android(kwargs['desc'], 'e'):
                            break
                    elif 'Id' in kwargs:
                        if self.__select_Id_Android(kwargs['Id']):
                            break
                    else:
                        raise ValueError(u'核心参数未给出，或者参数形式有误，请参考文档后，再使用！')
                    time.sleep(kwargs['refresh_time'])
                    timeCount += kwargs['refresh_time']

                if timeCount > t:
                    raise AssertionError(8)
            except KeyError as e:
                raise ValueError(u'参数有问题, 请核对')
        else:
            if args:
                if 'ui_base' in backFileName or 'baseOn' in backFileName:
                    pass
                else:
                    self._LOGGER.warning(u'无效参数，将为你执行默认方法，等待%ss' % t)
            time.sleep(t)

    def scrollByElement(self, *args, **kwargs):
        """
        通过text,desc或者Id滑动，direction为0代表下滑，为1反之；step为步数，默认滑动40下
        """
        # 默认方向为下滑
        if 'direction' not in kwargs:
            kwargs['direction'] = 0

        # 默认下滑步数40
        if 'step' not in kwargs:
            kwargs['step'] = 50

        # 获取滑动指令
        screenX, screenY = self.getScreenSize()
        command = CC.ADB_SWIPE
        if kwargs['direction'] == 0:
            excCommand = (command + ' ' + str(screenX/2) + ' ' +
                          str(screenY*3/4) + ' ' + str(screenX/2) + ' ' +
                          str(screenY/2))
        elif kwargs['direction'] == 1:
            excCommand = (command + ' ' + str(screenX/2) + ' ' +
                          str(screenY/4) + ' ' + str(screenX/2) + ' ' +
                          str(screenY/2))
        else:
            raise ValueError(u'你输入的参数有误')

        stepCount = 0
        while stepCount <= kwargs['step']:
            # 判断传入的控件类型
            if 'text' in kwargs:
                if self.__select_text_Android(kwargs['text'], 'e'):
                    break
            elif 'desc' in kwargs:
                if self.__select_desc_Android(kwargs['desc'], 'e'):
                    break
            elif 'Id' in kwargs:
                if self.__select_Id_Android(kwargs['Id']):
                    break
            else:
                raise ValueError(u'核心参数未给出，或者参数形式有误，请参考文档后，再使用！')
            os.system(excCommand)
            time.sleep(1)
            stepCount += 1
        else:
            if 'text' in kwargs:
                raise AssertionError(1)
            elif 'desc' in kwargs:
                raise AssertionError(2)
            elif 'Id' in kwargs:
                raise AssertionError(3)
            else:
                pass

    # def longPressByElement(self, el, duration=1000):
    #     '''
    #     长按元素
    #     '''
    #     self.long_press()

    def dragByElement(self, rule='e', *args, **kwargs):
        '''
        元素拖动
        '''
        if 'el_start' in kwargs and 'el_end' in kwargs:
            # 得到移动起始位置的元素
            if 'ins_start' not in kwargs:
                el_s = self.__getElement(kwargs['el_start'], rule)
            else:
                el_s = self.__getElement(kwargs['el_start'],
                                         rule,
                                         kwargs['ins_start'])
            # 得到移动结束位置的元素
            if 'ins_end' not in kwargs:
                el_e = self.__getElement(kwargs['el_end'], rule)
            else:
                el_e = self.__getElement(kwargs['el_end'],
                                         rule,
                                         kwargs['ins_end'])
            # 执行移动
            self.long_press(el_s).move_to(el_e).release().perform()
            self._LOGGER.debug(u'拖动已完成')

    def notificationsOn(self):
        """
        打开下拉栏
        """
        self.driver.open_notifications()
        self._LOGGER.debug(u'下拉通知栏完成')

    def clearText(self, *args, **kwargs):
        '''
        清除光标所在输入框的文字
        '''
        self .__select_Id_Android(kwargs['Id']).clear()
        self._LOGGER.debug(u'清除文字，完成')

    def testExit(self):
        """
        退出测试
        """
        self.driver.quit()
        self._LOGGER.debug(u'退出测试')

    def getCurrentTime(self):
        '''
        输出固定格式的时间
        '''
        currenttime = int(time.time())
        timeArray = time.localtime(currenttime)
        formatTime = time.strftime("%Y-%m-%d-%H:%M:%S", timeArray)
        return formatTime

    @baseOn.unifyParaCode
    def __select_text_Android(self, text, rule):
        """
        Android:text匹配规则；ins代表文本索引；rule为匹配规则，e代表全部匹配，p代表部分匹配
        """
        try:
            if rule == "e":
                el = self.driver.find_element_by_android_uiautomator(
                    'new UiSelector().text("{}")'.format(text))
            elif rule == "p":
                el = self.driver.find_element_by_android_uiautomator(
                    'new UiSelector().textContains("{}")'.format(text))
            else:
                raise ValueError(u"这么说吧，你用了一个假的规则选项，请重新阅读规则！")
            return el
        except selenium.common.exceptions.NoSuchElementException as e:
            return False

    @baseOn.unifyParaCode
    def __select_text_ins_Android(self, text, ins, rule):
        """
        Android:特定text匹配规则；ins代表文本索引；rule为匹配规则，e代表全部匹配，p代表部分匹配
        """
        try:
            if rule == "e":
                el = self.driver.find_element_by_android_uiautomator(
                    'new UiSelector().text("{}").instance({})'.format(
                        text, str(ins)))
            elif rule == "p":
                el = self.driver.find_element_by_android_uiautomator(
                    'new UiSelector().textContains("{}").instance({})'.format(
                        text, str(ins)))
            else:
                raise ValueError(u"这么说吧，你用了一个假的规则选项，请重新阅读规则！")

            return el
        except selenium.common.exceptions.NoSuchElementException as e:
            return False

    @baseOn.unifyParaCode
    def __select_desc_Android(self, desc, rule):
        """
        Android:desc匹配规则;rule为匹配规则，e代表全部匹配，p代表部分匹配
        """
        try:
            if rule == "e":
                el = self.driver.find_element_by_android_uiautomator(
                    'new UiSelector().description("{}")'.format(desc))
            elif rule == "p":
                el = self.driver.find_element_by_android_uiautomator(
                    'new UiSelector().descriptionContains("{}")'.format(desc))
            else:
                raise ValueError(u"这么说吧，你用了一个假的规则选项，请重新阅读规则！")

            return el
        except selenium.common.exceptions.NoSuchElementException as e:
            return False

    @baseOn.unifyParaCode
    def __select_desc_ins_Android(self, desc, ins, rule):
        """
        Android:特定desc匹配规则;ins为索引；rule为匹配规则，e代表全部匹配，p代表部分匹配
        """
        try:
            if rule == "e":
                el = self.driver.find_element_by_android_uiautomator(
                    'new UiSelector().description("{}").instance({})'.format(
                        desc, str(ins)))
            elif rule == "p":
                el = self.driver.find_element_by_android_uiautomator(
                    'new UiSelector().descriptionContains("{}").instance({})'
                    .format(desc, str(ins)))
            else:
                raise ValueError(u"这么说吧，你用了一个假的规则选项，请重新阅读规则！")

            return el
        except selenium.common.exceptions.NoSuchElementException as e:
            return False

    def __select_Id_Android(self, Id):
        """
        Android:Id匹配规则;
        """
        try:
            el = self.driver.find_element_by_android_uiautomator(
                'new UiSelector().resourceId("{}")'.format(Id))
            return el
        except selenium.common.exceptions.NoSuchElementException as e:
            return False

    def __select_Id_ins_Android(self, Id, ins):
        """
        Android:特定Id匹配规则;ins为索引；
        """
        try:
            el = self.driver.find_element_by_android_uiautomator(
                'new UiSelector().resourceId("{}").instance({})'.format(
                    Id, str(ins)))
            return el
        except selenium.common.exceptions.NoSuchElementException as e:
            return False

    @baseOn.unifyParaCode
    def __getElement(self, el, rule, ins=None):
        '''
        通过用户传参获取元素
        '''
        el_T = self.__select_text_Android(el, rule)
        el_D = self.__select_desc_Android(el, rule)
        if not ins:
            el_I = self.__select_Id_Android(el)
        else:
            el_I = self.__select_Id_ins_Android(el, ins)

        el_list = [el_T, el_D, el_I]
        el_list_n = self.clearAllAppointEl(el_list, False)
        el = el_list_n[0]
        return el
