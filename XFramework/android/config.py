# -*- coding:utf-8 -*-


def xiaomi_init(uiObj):
    """小米手机初始化
    """
    numCount = 10
    while numCount > 0:
        # 判断是否位于启动页广告，是则点击跳过
        if uiObj.isIdInPage('com.ximalaya.ting.android:id/main_count_down_text'):
            uiObj.clickById('com.ximalaya.ting.android:id/main_count_down_text')
        # 判断是有定位权限，有则点击允许
        if uiObj.isIdInPage('android:id/button1'):
            uiObj.clickById('android:id/button1')
        if uiObj.isIdInPage('android:id/button1'):
            uiObj.clickById('android:id/button1')
        # 判断是否有选择开发者，有则点击是
        if uiObj.isIdInPage('com.ximalaya.ting.android.main.application:id/main_ok_btn'):
            uiObj.clickById('com.ximalaya.ting.android.main.application:id/main_ok_btn')
        # 判断是否有升级提醒，有则点击忽略
        if uiObj.isIdInPage('com.ximalaya.ting.android:id/neutral_btn'):
            uiObj.clickById('com.ximalaya.ting.android:id/neutral_btn')
        # 判断是否有广告悬浮按钮，有则点击关闭
        if uiObj.isIdInPage('com.ximalaya.ting.android.main.application:id/main_ad_broadside_close'):
            uiObj.clickById('com.ximalaya.ting.android.main.application:id/main_ad_broadside_close')
        # 判断是否有广告，有则点击关闭
        if uiObj.isIdInPage('com.ximalaya.ting.android.main.application:id/main_close_ad'):
            uiObj.clickById('com.ximalaya.ting.android.main.application:id/main_close_ad')
        # 判断是否有选择兴趣页，有则点击跳过
        if uiObj.isIdInPage('com.ximalaya.ting.android.main.application:id/main_btn_skip'):
            uiObj.clickById('com.ximalaya.ting.android.main.application:id/main_btn_skip')
        # 判断是否无弹框，无弹框则打破循环进入测试
        if uiObj.isTextInPage('首页')\
           and (not uiObj.isIdInPage('com.ximalaya.ting.android.main.application:id/main_btn_skip')
                or not uiObj.isIdInPage('com.ximalaya.ting.android:id/main_btn_skip')):
            break
        else:
            numCount -= 1
    else:
        uiObj._LOGGER.warning(u'xiaomi: 点击初始化app弹窗失败，请检测app控件名是否正确！')


def huawei_init(uiObj):
    """华为手机初始化
    """
    numCount = 10
    while numCount > 0:
        # 判断是否位于启动页广告，是则点击跳过
        if uiObj.isIdInPage('com.ximalaya.ting.android:id/main_count_down_text'):
            uiObj.clickById('com.ximalaya.ting.android:id/main_count_down_text')
        # 判断是有定位权限，有则点击允许
        if uiObj.isIdInPage('com.android.packageinstaller:id/permission_allow_button'):
            uiObj.clickById('com.android.packageinstaller:id/permission_allow_button')
        if uiObj.isIdInPage('com.android.packageinstaller:id/permission_allow_button'):
            uiObj.clickById('com.android.packageinstaller:id/permission_allow_button')
        # 判断是否有选择开发者，有则点击是
        if uiObj.isIdInPage('com.ximalaya.ting.android.main.application:id/main_ok_btn'):
            uiObj.clickById('com.ximalaya.ting.android.main.application:id/main_ok_btn')
        # 判断是否有升级提醒，有则点击忽略
        if uiObj.isIdInPage('com.ximalaya.ting.android:id/neutral_btn'):
            uiObj.clickById('com.ximalaya.ting.android:id/neutral_btn')
        # 判断是否有广告悬浮按钮，有则点击关闭
        if uiObj.isIdInPage('com.ximalaya.ting.android.main.application:id/main_ad_broadside_close'):
            uiObj.clickById('com.ximalaya.ting.android.main.application:id/main_ad_broadside_close')
        # 判断是否有广告，有则点击关闭
        if uiObj.isIdInPage('com.ximalaya.ting.android.main.application:id/main_close_ad'):
            uiObj.clickById('com.ximalaya.ting.android.main.application:id/main_close_ad')
        # 判断是否有选择兴趣页，有则点击跳过
        if uiObj.isIdInPage('com.ximalaya.ting.android.main.application:id/main_btn_skip'):
            uiObj.clickById('com.ximalaya.ting.android.main.application:id/main_btn_skip')
        # 判断是否无弹框，无弹框则打破循环进入测试
        if uiObj.isTextInPage('首页')\
           and (not uiObj.isIdInPage('com.ximalaya.ting.android.main.application:id/main_btn_skip')
                or not uiObj.isIdInPage('com.ximalaya.ting.android:id/main_btn_skip')):
            break
        else:
            numCount -= 1
    else:
        uiObj._LOGGER.warning(u'honor: 点击初始化app弹窗失败，请检测app控件名是否正确！')


def honor_init(uiObj):
    """荣耀手机初始化
    """
    numCount = 10
    while numCount > 0:
        # 判断是否位于启动页广告，是则点击跳过
        if uiObj.isIdInPage('com.ximalaya.ting.android:id/main_count_down_text'):
            uiObj.clickById('com.ximalaya.ting.android:id/main_count_down_text')
        # 判断是有定位权限，有则点击允许
        if uiObj.isIdInPage('com.android.packageinstaller:id/permission_allow_button'):
            uiObj.clickById('com.android.packageinstaller:id/permission_allow_button')
        if uiObj.isIdInPage('com.android.packageinstaller:id/permission_allow_button'):
            uiObj.clickById('com.android.packageinstaller:id/permission_allow_button')
        # 判断是否有选择开发者，有则点击是
        if uiObj.isIdInPage('com.ximalaya.ting.android.main.application:id/main_ok_btn'):
            uiObj.clickById('com.ximalaya.ting.android.main.application:id/main_ok_btn')
        # 判断是否有升级提醒，有则点击忽略
        if uiObj.isIdInPage('com.ximalaya.ting.android:id/neutral_btn'):
            uiObj.clickById('com.ximalaya.ting.android:id/neutral_btn')
        # 判断是否有广告悬浮按钮，有则点击关闭
        if uiObj.isIdInPage('com.ximalaya.ting.android.main.application:id/main_ad_broadside_close'):
            uiObj.clickById('com.ximalaya.ting.android.main.application:id/main_ad_broadside_close')
        # 判断是否有广告，有则点击关闭
        if uiObj.isIdInPage('com.ximalaya.ting.android.main.application:id/main_close_ad'):
            uiObj.clickById('com.ximalaya.ting.android.main.application:id/main_close_ad')
        # 判断是否有选择兴趣页，有则点击跳过
        if uiObj.isIdInPage('com.ximalaya.ting.android.main.application:id/main_btn_skip'):
            uiObj.clickById('com.ximalaya.ting.android.main.application:id/main_btn_skip')
        # 判断是否无弹框，无弹框则打破循环进入测试
        if uiObj.isTextInPage('首页')\
           and (not uiObj.isIdInPage('com.ximalaya.ting.android.main.application:id/main_btn_skip')
                or not uiObj.isIdInPage('com.ximalaya.ting.android:id/main_btn_skip')):
            break
        else:
            numCount -= 1
    else:
        uiObj._LOGGER.warning(u'honor: 点击初始化app弹窗失败，请检测app控件名是否正确！')


def vivo_init(uiObj):
    """VIVO手机初始化
    """
    pass


def oppo_init(uiObj):
    """OPPO手机初始化
    """
    pass


def qiku_init(uiObj):
    """奇酷手机初始化
    """
    numCount = 10
    while numCount > 0:
        # 判断是否位于启动页广告，是则点击跳过
        if uiObj.isIdInPage('com.ximalaya.ting.android:id/main_count_down_text'):
            uiObj.clickById('com.ximalaya.ting.android:id/main_count_down_text')
        # 判断是否有选择开发者，有则点击是
        if uiObj.isIdInPage('com.ximalaya.ting.android.main.application:id/main_ok_btn'):
            uiObj.clickById('com.ximalaya.ting.android.main.application:id/main_ok_btn')
        # 判断是否有升级提醒，有则点击忽略
        if uiObj.isIdInPage('com.ximalaya.ting.android:id/neutral_btn'):
            uiObj.clickById('com.ximalaya.ting.android:id/neutral_btn')
        # 判断是否有广告悬浮按钮，有则点击关闭
        if uiObj.isIdInPage('com.ximalaya.ting.android.main.application:id/main_ad_broadside_close'):
            uiObj.clickById('com.ximalaya.ting.android.main.application:id/main_ad_broadside_close')
        # 判断是否有广告，有则点击关闭
        if uiObj.isIdInPage('com.ximalaya.ting.android.main.application:id/main_close_ad'):
            uiObj.clickById('com.ximalaya.ting.android.main.application:id/main_close_ad')
        # 判断是否有选择兴趣页，有则点击跳过
        if uiObj.isIdInPage('com.ximalaya.ting.android.main.application:id/main_btn_skip'):
            uiObj.clickById('com.ximalaya.ting.android.main.application:id/main_btn_skip')
        # 判断是否无弹框，无弹框则打破循环进入测试
        if uiObj.isTextInPage('首页')\
           and (not uiObj.isIdInPage('com.ximalaya.ting.android.main.application:id/main_btn_skip')
                or not uiObj.isIdInPage('com.ximalaya.ting.android:id/main_btn_skip')):
            break
        else:
            numCount -= 1
    else:
        uiObj._LOGGER.warning(u'qiku: 点击初始化app弹窗失败，请检测app控件名是否正确！')
