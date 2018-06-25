# -*- coding:utf-8 -*-

import unittest, os
from time import sleep

from selenium.common.exceptions import NoSuchElementException

from appium import webdriver

class AppiumTests(unittest.TestCase):
    def setUp(self):
        app = os.path.join(os.path.dirname(__file__), '/Users/nali/Downloads/ting-6.3.99-666.ipa')
        app = os.path.abspath(app)
        desired_caps = {}
        #desired_caps['appium-version'] = '1.6.5'
        desired_caps['platformName'] = 'iOS'
        desired_caps['platformVersion'] = '10.1'
        desired_caps['deviceName'] = 'iPhone 5s'
        desired_caps['app']=app
        #desired_caps['udid']='2e58ffd37a53a8a3920f51b4ab73fe5e6a363d22'
        desired_caps['udid']='718a869e2ba724cc8cd2aa81d733d302b4153a17'
        desired_caps['automationName']='XCUITest'
        desired_caps['newCommandTimeout']=1000
        desired_caps['unicodeKeyboard'] = True
        desired_caps['resetKeyboard'] = True
        desired_caps['xcodeOrgId']='AS4ANJJUVM'
        desired_caps['xcodeSigningId']='iPhone Developer'
        desired_caps['allowTouchIdEnroll']=True
        self.driver = webdriver.Remote('http://localhost:4723/wd/hub', desired_caps)

    def tearDown(self):
        self.driver.quit()

    def test_lock(self):
        sleep(10)
        note1 = self.driver.find_element('name', '允许')
        if note1:
            note1.click()
            print '点击允许'
        sleep(2)
        note2 = self.driver.find_element('id','以后再说')
        if note2:
            note2.click()
            print '点击以后再说'
        sleep(2)
        el = self.driver.find_element('name', '通知')
        el.click()
        print '点击通知'
        sleep(2)
        el1 = self.driver.find_element('name', '密码登录')
        el1.click()
        print '点击密码登录'
        sleep(10)
        
        '''
        username = self.driver.find_element_by_ios_predicate('value == "请输入手机号"')
        if username:
            print '存在value=请输入手机号'
            username.click()
            print '光标定位到用户名输入框'            
            sleep(2)
            username.send_keys(u'15010000001') 
            
            
        password = self.driver.find_element_by_ios_predicate('value == "请输入密码"')
        if password:
            print '存在value=请输入密码'
            password.click()
            print '光标定位到密码框'
            password.send_keys(u'a123456') 
            
        siginbut = self.driver.find_element_by_ios_predicate('label == "登录"')
        if siginbut:
            print '存在label=登录的button'
            siginbut.click()
            print '点击登录'
            
        sleep(10)
        '''

if __name__ == "__main__":
    suite = unittest.TestLoader().loadTestsFromTestCase(AppiumTests)
    unittest.TextTestRunner(verbosity=2).run(suite)
