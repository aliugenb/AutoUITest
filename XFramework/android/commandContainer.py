# -*- coding:utf-8 -*-


class CommandContainer(object):
    """
    存储命令行
    """
    # Android命令
    # 获取手机名称
    GET_PHONE_NAME = 'adb shell getprop ro.product.model'
    # 获取手机版本
    GET_PHONE_VERSION = 'adb shell getprop ro.build.version.release'
    # 获取手机厂商
    GET_PHONE_PRODUCER = 'adb shell getprop ro.product.brand'
    # 获取手机已安装的输入法
    GET_PHONE_HAD_IME = 'adb shell ime list -s'
    # 获取手机当前输入法
    GET_PHONE_CURRENT_IME = 'adb shell settings get secure default_input_method'
    # 设置手机输入法
    SET_PHONE_IME = 'adb shell settings put secure default_input_method'  # 此方法后面必须再加包名
    # 获取手机分辨率
    GET_SCREEN_SIZE = 'adb shell wm size'
    # 非中文输入
    INPUT_TEXT = 'adb shell input text'
    PULLFILE_PHOHE_TO_COMPUTER = 'adb pull'  # 后接文件路径
    PHONE_KEYEVENT = 'adb shell input keyevent'  # 后接key值
    PHONE_SCREENCAP = 'adb shell screencap -p'  # 后接手机路径
    ADB_SWIPE = 'adb shell input swipe'  # 后接滑动坐标
    PHONE_DEVICES = 'adb devices'
    PHONE_SHELL = 'adb shell'
    CLEAR_APP_DATA = 'adb shell pm clear'
    START_APP = 'adb shell am start -W -S -n'
    SEARCH_APP_PRO = 'adb shell ps | grep'
    START_ADB = 'adb start-server'
    KILL_ADB = 'adb kill-server'
    GET_SCREEN_DETAIL = 'adb shell dumpsys window displays | head -n 3'
    FORCE_STOP_APP = 'adb shell am force-stop'

    """
    包名/Activity名
    """
    # appium输入法包名
    APPIUM_IME_PKG = 'io.appium.android.ime'
    # 喜马拉雅
    XIMALAYA_PKG = 'com.ximalaya.ting.android'
    XIMALAYA_ACTIVITY = 'com.ximalaya.ting.android/com.ximalaya.ting.android.host.activity.WelComeActivity'

    """
    常用路径
    """
    # 图片存放
    WIN_PATH_F = ''
    # 图片存放
    PHONE_PATH = 'sdcard/AutoTest/screencap'
    # 对比图片存放
    PHONE_PIC_COMPARE_PATH = "sdcard/AutoTest/temp"
    # 图片存放
    LINIX_PATH_F = "/opt/lampp/htdocs/kodexplorer/data/Group/public/home/UITest/Android/screenshot/"

    '''
    其他
    '''
    SPECIAL_CHARACTER_LIST = r'[\\/:*?" <>|]'
