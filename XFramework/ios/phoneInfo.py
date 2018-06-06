# -*- coding:utf-8 -*-
from appium import webdriver
from baseOn import BaseOn as bo
import os

configData_default = {}
configData_default["platformName"] = "iOS"
configData_default["newCommandTimeout"] = 3000
configData_default["testAppPath"] = '/Users/nali/Downloads/ting-6.3.99-666.ipa'



def getDriver(configData=configData_default):
    app = os.path.join(os.path.dirname(__file__), configData['testAppPath'])
    app = os.path.abspath(app)   

    desired_caps = {}
    desired_caps['platformName'] = configData['platformName'] 
    desired_caps['platformVersion'] = bo.getPlatformVersionIos()
    desired_caps['deviceName'] = bo.getPhoneNameIos()
    desired_caps['app']=app
    #desired_caps['udid']='2e58ffd37a53a8a3920f51b4ab73fe5e6a363d22'
    desired_caps['udid']=bo.getPhoneUdid()
    desired_caps['automationName']='XCUITest'
    desired_caps['newCommandTimeout']=configData['newCommandTimeout']
    desired_caps['allowTouchIdEnroll']=True
    desired_caps['noReset'] = True
    desired_caps["unicodeKeyboard"] = True  # 支持中文
    driver = webdriver.Remote('http://localhost:4723/wd/hub', desired_caps)
    
    return driver
