# -*- coding:utf-8 -*-
import os, sys, time
from functools import wraps
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
    @wraps(func)
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
    def __init__(self, configData, driver=None):
        self.configData = configData
        self.driver = pi.getDriver(self.configData)
        TA.__init__(self, driver=self.driver)
        
    def clearApp(self):
        '''
        启动apk
        '''
        self.driver.reset()
        
    def getScreenSizeIos(self):
        """
        获取屏幕分辨率，返回横纵坐标
        """    
        size = self.driver.get_window_size()
        print size
        return size['width'], size['height']
    
        
    def clickByPos(self, x, y, duration=None):
        """
        通过坐标点击；duration为持续时间，单位ms
        """
        self.driver.tap([(x, y)], duration)
        time.sleep(1)
        self._LOGGER.debug(u'点击坐标结束')
    
    @setDefaultPara 
    def clickById(self, Id, *args, **kwargs):
        """
        通过控件的id属性点击；
        """
        if str(kwargs['flowTag']) == '1':
            try:
                self.sleep(kwargs['totalTime'], refresh_time=kwargs['refresh_time'], Id=Id)
            except AssertionError as e:                
                pass
        try:
            self.__select_Id_iOS(Id).click()
            self._LOGGER.debug(u'点击Id: ' + Id + u'，结束')

        except AttributeError as e:
            raise AssertionError(1)
        
    @setDefaultPara 
    def clickByName(self, name, *args, **kwargs):
        """
        通过控件的name属性点击；
         """
        if str(kwargs['flowTag']) == '1':
            try:
                self.sleep(kwargs['totalTime'], refresh_time=kwargs['refresh_time'], name=name)
            except AssertionError as e:
                pass
        try:
            self.__select_name_iOS(name, rule).click()
            self._LOGGER.debug(u'点击text: ' + name + u'，结束')
        except AttributeError as e:
            raise AssertionError(2)  
        
    @setDefaultPara    
    def clickByXpath(self, xpath, *args, **kwargs):
        """
        通过控件的xpath点击；
         """
        if str(kwargs['flowTag']) == '1':
            try:
                self.sleep(kwargs['totalTime'], refresh_time=kwargs['refresh_time'], xpath=xpath)
            except AssertionError as e:
                pass
        try:
            self.__select_xpath_iOS(xpath, rule).click()
            self._LOGGER.debug(u'点击text: ' + xpath + u'，结束')
        except AttributeError as e:
            raise AssertionError(3)        
           
    @setDefaultPara 
    def getValueByXpath(self, name, *args, **kwargs):
        """
        通过控件的xpath获取value属性的值
        """
        if str(kwargs['flowTag']) == '1':
            try:
                self.sleep(kwargs['totalTime'],refresh_time=kwargs['refresh_time'], xpath=xpath)
            except AssertionError as e:
                pass        
        try:
            re_text = self.__select_xpath_iOS(xpath).get_attribute("value")
            self._LOGGER.debug(u"获取text: " + re_text.decode('utf-8') + u'，结束')
            return re_text
        except AttributeError as e:              
            raise AssertionError(3)
        
    @setDefaultPara  
    def setValueByXpath(self, input_text, xpath, *args, **kwargs):
        """
        通过控件的xpath输入文本
        input_text为你想输入文本
        """    
        try:
            self.__select_xpath_iOS(xpath).click()
            self.__select_xpath_iOS(xpath).send_keys(input_text)
            self._LOGGER.debug(u'T文本: ' + input_text + u'，输入结束')
        except AttributeError as e:            
            raise AssertionError(3)
    
    def isIdInPage(self, Id):
        """
        判断id元素是否存在，有返回值
        """

        if self.__select_Id_iOS(Id):
            return True
        else:
            return False      
        
    def isNameInPage(self, name):
        """
        判断name是否存在，有返回值
        """
        if self.__select_name_iOS(name):
            return True
        else:
            return False
       
    def isXpathInPage(self, xpath):
        """
        判断xpath是否存在，有返回值
        """
        if self.__select_xpath_iOS(xpath):
            return True
        else:
            return False
     
    @setDefaultPara 
    def isExistById(self, Id, instruction, isIn=0, *args, **kwargs):
        """
        通过控件的id属性判断操作是否成功，instruction为此处步骤描述内容；
        """
        #self._LOGGER.debug(instruction.decode('utf-8'))
        if str(kwargs['flowTag']) == '1':
            try:
                self.sleep(kwargs['totalTime'], refresh_time=kwargs['refresh_time'], Id=Id)
            except AssertionError as e:
                pass

        if int(isIn) == 0:
            if self.__select_Id_iOS(Id):
                pass
            else:
                raise AssertionError
        elif int(isIn) == 1:
            if not self.__select_Id_iOS(Id):
                pass
            else:
                raise AssertionError
            raise AssertionError
        else:
            raise ValueError(u"参数输入有误，请确认后输入参数") 
        
    @setDefaultPara 
    def isExistByName(self, name, instruction, isIn=0, *args, **kwargs):
        """
        通过控件的name属性判断操作是否成功，instruction为此处步骤描述内容；
        isIn为存在标志：默认为0，表示存在；1表示不存在
        """        
        #self._LOGGER.debug(instruction.decode('utf-8'))
        if str(kwargs['flowTag']) == '1':
            try:
                self.sleep(kwargs['totalTime'], refresh_time=kwargs['refresh_time'], name=name)
            except AssertionError as e:
                pass

        if int(isIn) == 0:
            if self.__select_name_iOS(name, rule):
                pass
            else:
                raise AssertionError
        elif int(isIn) == 1:
            if not self.__select_name_iOS(name,rule):
                pass
            else:
                raise AssertionError
        else:            
            raise ValueError(u"参数输入有误，请确认后输入参数")
        
    @setDefaultPara
    def isExistByXpath(self, xpath, instruction, isIn=0, *args, **kwargs):
        """
        通过控件的xpath判断操作是否成功，instruction为此处步骤描述内容；
        isIn为存在标志：默认为0，表示存在；1表示不存在
        
        """
        #self._LOGGER.debug(instruction.decode('utf-8'))
        if str(kwargs['flowTag']) == '1':
            try:
                self.sleep(kwargs['totalTime'], refresh_time=kwargs['refresh_time'], xpath=xpath)
            except AssertionError as e:
                pass

        if int(isIn) == 0:
            if self.__select_xpath_iOS(xpath):
                pass
            else:
                raise AssertionError
        elif int(isIn) == 1:
            if not self.__select_xpath_iOS(xpath):
                pass
            else:
                raise AssertionError
        else:
            raise ValueError(u"参数输入有误，请确认后输入参数")
        
    
    def __select_Id_iOS(self, Id):
        """
        iOS:Id
        """
        try:
            el = self.driver.find_element('id', Id)
            return el
        except selenium.common.exceptions.NoSuchElementException as e:
            return False    
    
    def __select_name_iOS(self, name):
        """
        iOS:name
        """
        try:
            el = self.driver.find_element('name', name)
            return el
        except selenium.common.exceptions.NoSuchElementException as e:
            return False
        
    def __select_xpath_iOS(self, xpath):
        """
        iOS:xpath
        """
        try:
            el = self.driver.find_element('xpath', xpath)
            return el
        except selenium.common.exceptions.NoSuchElementException as e:
            return False  
    

    def swipeByPos(self, start_x, start_y, end_x, end_y, duration=None):
        """
        通过坐标滑动；duration为持续时间，单位ms
        """
        self.driver.swipe(start_x, start_y, end_x, end_y, duration)
        time.sleep(1)
        self._LOGGER.debug(u'滑动结束')

    '''   
    @setDefaultPara 
    def setValueById(self, input_text, Id_2, *args, **kwargs):
           
            #通过控件的Id属性输入文本；input_text为你想输入文本，支持中英文
           
        #input_text = base_on.codeUnify(input_text)
        if 'Id_before' not in kwargs:
            kwargs['Id_before'] = Id_2

        else:
            try:
                self.__select_Id_iOS(kwargs['Id_before']).click()
                self.__select_Id_iOS(Id_2).click()
                self.__select_Id_iOS(Id_2).send_keys(input_text)
                self._LOGGER.debug(u'I文本: ' + input_text + u'，输入结束')
            except AttributeError as e:
                raise AssertionError
    '''
    
    @setDefaultPara 
    def clearText(self, *args, **kwargs):
        '''
        清除光标所在输入框的文字
        '''
        #目前仅发现通过xpath清除的需求
        if 'xpath' in kwargs:
            self .__select_xpath_iOS(kwargs['xpath']).clear()
            self._LOGGER.debug(u'清除文字，完成')

        # elif 'Id' in kwargs:
        #     self .__select_Id_iOS(kwargs['Id']).clear()
        # elif 'name' in kwargs:
        #     self.__select_name_iOS(kwargs['name']).clear()
        else:
            raise ValueError
    
    @setDefaultPara     
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
                    if 'id' in kwargs:
                        if self.__select_Id_iOS()(kwargs['id'], 'e'):
                            break
                    elif 'name' in kwargs:
                        if self.__select_name_iOS(kwargs['name'], 'e'):
                            break
                    elif 'xpath' in kwargs:
                        if self.__select_xpath_iOS(kwargs['xpath']):
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


    @setDefaultPara 
    def scrollByElement(self, *args, **kwargs):
        """
        通过text,desc或者Id,name,xpath滑动，direction为0代表下滑，为1反之；step为步数，默认滑动40下
        """
        #默认方向为下滑
        if 'direction' not in kwargs:
            kwargs['direction'] = 0

        #默认下滑步数50
        if 'step' not in kwargs:
            kwargs['step'] = 50

        stepCount = 0
        while stepCount <= kwargs['step']:
            if kwargs['direction'] == 0:
                #self.driver.execute_script('mobile: swipe', {'direction': 'up'})
                self.driver.execute_script('mobile: scroll', {'direction': 'down'})
            elif kwargs['direction'] == 1:
                self.driver.execute_script('mobile: scroll', {'direction': 'up'})
            else:
                raise ValueError
            #判断传入的控件类型
            if 'Id' in kwargs:
                if self.__select_Id_iOS(kwargs['Id']).get_attribute("visible")=='true':
                    break
            elif 'name' in kwargs:
                if self.__select_name_iOS(kwargs['name']).get_attribute("visible")=='true':
                    break
            elif 'xpath' in kwargs:
                if self.__select_xpath_iOS(kwargs['xpath']).get_attribute("visible")=='true':
                    break
            else:
                self._LOGGER.critical(u'核心参数未给出，或者参数形式有误，请参考文档后，再使用！')
                #self.set_ime()
                raise ValueError
            time.sleep(2)
            stepCount += 1
            
    def testExit(self):
        """
        退出测试
        """
        self.driver.quit()
        self._LOGGER.debug(u'退出测试，完成')

    def getCurrentTime(self):
        '''
        输出固定格式的时间
        '''
        currenttime = self.getCurrentTime()
        timeArray = time.localtime(currenttime)
        formatTime = time.strftime("%Y-%m-%d-%H:%M:%S", timeArray)
        return formatTime



    
