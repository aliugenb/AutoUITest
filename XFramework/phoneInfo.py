# -*- coding:utf-8 -*-
import json
from appium import webdriver
from base_on import BaseOn as bo


# class PhoneInfo(BaseOn):
#     """
#         设置初始化常量
#     """
#     def __init__(self):
#         # 测试设备信息
#         self.desired_caps = {}
#         self.desired_caps['automationName'] = 'UiAutomator2'  # 使用UI2
#         self.desired_caps['platformName'] = 'Android'  # 设备系统
#         self.desired_caps['platformVersion'] = self.getPlatformVersion()  # 设备系统版本
#         self.desired_caps['deviceName'] = self.getDeviceName()  # 设备名称
#         # ximalaya
#         self.desired_caps['appPackage'] = 'com.ximalaya.ting.android'
#         self.desired_caps['appActivity'] = '.host.activity.WelComeActivity'
#         self.desired_caps['noReset'] = True  # 不重新安装三个APK
#         self.desired_caps['newCommandTimeout'] = 300
#         self.desired_caps["unicodeKeyboard"] = True  # 支持中文
#
#         self.driver = webdriver.Remote('http://localhost:4723/wd/hub',
#                                        self.desired_caps)
def getConfigPara(filePath):
    configDict = {}
    with open(filePath, 'r') as f:
        tempDict = json.load(f)
    if 'Android' in tempDict:
        configDict = tempDict['Android']
    elif 'IOS' in tempDict:
        configDict = tempDict['IOS']
    else:
        print('平台参数配置错误，退出测试！')
        raise ValueError
    if configDict == {}:
        print('参数配置错误，退出测试！')
        raise ValueError
    return configDict


def getDriver():
    configData = getConfigPara('config.json')
    desired_caps = {}
    desired_caps['automationName'] = 'UiAutomator2'  # 使用UI2
    # desired_caps['platformName'] = 'Android'  # 设备系统
    desired_caps['platformName'] = configData['platformName']  # 设备系统
    desired_caps['platformVersion'] = bo().getPlatformVersion()  # 设备系统版本
    desired_caps['deviceName'] = bo().getDeviceName()  # 设备名称
    # ximalaya
    # desired_caps['appPackage'] = 'com.ximalaya.ting.android'
    # desired_caps['appActivity'] = '.host.activity.WelComeActivity'
    # desired_caps['newCommandTimeout'] = 300
    desired_caps['appPackage'] = configData['appPackage']
    desired_caps['appActivity'] = configData['appActivity']
    desired_caps['newCommandTimeout'] = configData['newCommandTimeout']
    desired_caps["unicodeKeyboard"] = True  # 支持中文
    driver = webdriver.Remote('http://localhost:4723/wd/hub', desired_caps)
    return driver
