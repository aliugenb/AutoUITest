# -*- coding:utf-8 -*-
from appium import webdriver
from base_on import BaseOn

class PhoneInfo(BaseOn):
    """
        设置初始化常量
    """
    def __init__(self):
        #测试设备信息
        self.desired_caps = {}
        self.desired_caps['automationName'] = 'UiAutomator2' #使用UI2
        self.desired_caps['platformName'] = 'Android' #设备系统
        self.desired_caps['platformVersion'] = self.getPlatformVersion() #设备系统版本
        self.desired_caps['deviceName'] = self.getDeviceName() #设备名称
        #ximalaya
        self.desired_caps['appPackage'] = 'com.ximalaya.ting.android'
        self.desired_caps['appActivity'] = '.host.activity.WelComeActivity'
        self.desired_caps['noReset'] = True # 不重新安装三个APK
        self.desired_caps['newCommandTimeout'] = 300
        self.desired_caps["unicodeKeyboard"] = True #支持中文
        #self.desired_caps["resetKeyboard"] = True #测试完后，重置输入法

        self.driver = webdriver.Remote('http://localhost:4723/wd/hub', self.desired_caps)


# def PhoneInfo():
#     desired_caps = {}
#     desired_caps['automationName'] = 'UiAutomator2' #使用UI2
#     desired_caps['platformName'] = 'Android' #设备系统
#     desired_caps['platformVersion'] = BO().getPlatformVersion() #设备系统版本
#     desired_caps['deviceName'] = BO().getDeviceName() #设备名称
#     #ximalaya
#     desired_caps['appPackage'] = 'com.ximalaya.ting.android'
#     desired_caps['appActivity'] = '.host.activity.WelComeActivity'
#     desired_caps['newCommandTimeout'] = 300
#     desired_caps["unicodeKeyboard"] = True #支持中文
#     #self.desired_caps["resetKeyboard"] = True #测试完后，重置输入法
#
#     driver = webdriver.Remote('http://localhost:4723/wd/hub', desired_caps)
#     return driver
