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
            print type(note1)
            print '点击允许'
        sleep(2)
        note2 = self.driver.find_elements('id','以后再说')
        print note2
        print type(note2)
        if note2:
            note2[0].click()
            print len(note2)
            print note2[len(note2)-1]
            print '点击以后再说'
        sleep(2)
        el = self.driver.find_element('name', '通知')
        el.click()
        print '点击通知'
        sleep(2)
        el1 = self.driver.find_element('name', '密码登录')
        el1.click()
        print '点击密码登录'
        sleep(2)
      



if __name__ == "__main__":
    suite = unittest.TestLoader().loadTestsFromTestCase(AppiumTests)
    unittest.TextTestRunner(verbosity=2).run(suite)
