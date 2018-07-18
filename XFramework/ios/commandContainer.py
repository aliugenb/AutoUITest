# -*- coding:utf-8 -*-
import os

class CommandContainer(object):
    """
    存储命令行
    """
    PHONE_UDID = 'idevice_id -l'
    #获取手机的设备版本：
    PLATFORM_VERSION = 'ideviceinfo -k ProductVersion'
    #获取手机的设备名：
    PHONE_NAME = 'ideviceinfo -k ProductType'
    #获取手机截图：
    SCREENCAP = 'idevicescreenshot'
   
        
    PROJECTPATH = os.path.abspath(os.path.join(os.getcwd(), "../.."))
    PIC_SAVEPATH = PROJECTPATH +'/testDriver/testLOG/screencap/'
    MOVIE_SAVEPATH = PROJECTPATH +'/testDriver/testLOG/screenrecord/'
    
    XRECORD_PATH=PROJECTPATH +'/xrecord/bin/'
    #获取xrecord设备连接：
    XRECORD_DEVICES= 'xrecord --quicktime --list'
    XRECORD_iPhone= 'xrecord --quicktime --id'
   

    XIMALAYA_PKG = 'com.gemd.iting'  

    SPECIAL_CHARACTER_LIST = r'[\\/:*?" <>|]'
