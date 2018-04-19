# -*- coding:utf-8 -*-
from appium import webdriver
from baseOn import BaseOn as bo


def getDriver(configData):
    desired_caps = {}
    desired_caps['automationName'] = 'UiAutomator2'  # 使用UI2
    desired_caps['platformName'] = configData['platformName']  # 设备系统
    desired_caps['platformVersion'] = bo().getPlatformVersion()  # 设备系统版本
    desired_caps['deviceName'] = bo().getDeviceName()  # 设备名称
    # ximalaya
    desired_caps['appPackage'] = configData['appPackage']
    desired_caps['appActivity'] = configData['appActivity']
    desired_caps['newCommandTimeout'] = configData['newCommandTimeout']
    desired_caps["unicodeKeyboard"] = True  # 支持中文
    driver = webdriver.Remote('http://localhost:4723/wd/hub', desired_caps)
    return driver
