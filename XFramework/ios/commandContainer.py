# -*- coding:utf-8 -*-


class CommandContainer(object):
    """
    存储命令行
    """
    PHONE_UDID = 'idevice_id -l'
    #获取手机的设备版本：
    PLATFORM_VERSION = 'ideviceinfo -k ProductVersion'
    #获取手机的设备名：
    PHONE_NAME = 'ideviceinfo -k ProductType'

    XIMALAYA_PKG = 'com.gemd.iting'

    SPECIAL_CHARACTER_LIST = r'[\\/:*?" <>|]'
