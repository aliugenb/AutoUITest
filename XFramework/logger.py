# -*- coding:utf-8 -*-
import os, sys, logging, time, platform

def setLogPath(filename='total_log.txt'):
    '''
    设置LOG生成路径和文件名
    '''
    #设置结果生成路径
    initialPath = os.path.realpath(sys.argv[0])
    if 'Android' in initialPath:
        if 'Windows' in platform.system():
            tempPath = initialPath.split('Android\\')
            targetPath = tempPath[0] + 'Android\\LOG\\'
        else:
            tempPath = initialPath.split('Android/')
            targetPath = tempPath[0] + r'Android/LOG/'
    else:
        print('路径中不存在，Android, 请检查路径')
        raise IOError
    logFile = targetPath + filename
    return logFile

def setResultPath(filename='result.txt'):
    '''
    设置Result生成路径和文件名
    '''
    #设置结果生成路径
    initialPath = os.path.realpath(sys.argv[0])
    #print(targetPath)
    if 'Android' in initialPath:
        if 'Windows' in platform.system():
            tempPath = initialPath.split('Android\\')
            targetPath = tempPath[0] + 'Android\\LOG\\'
        else:
            tempPath = initialPath.split('Android/')
            targetPath = tempPath[0] + r'Android/LOG/'
    else:
        print('路径中不存在，Android, 请检查路径')
        raise IOError
    logFile = targetPath + filename
    return logFile

def logCreater(filePath):
    '''
    设置LOG生成器
    '''
    #创建logger
    logger = logging.getLogger('ximalaya')
    logger.setLevel(logging.DEBUG)
    #设置文本日志处理器
    fileHandler = logging.FileHandler(filePath, mode='a+')
    fileHandler.setLevel(logging.INFO)
    #设置控制台日志处理器
    consoleHandler = logging.StreamHandler()
    consoleHandler.setLevel(logging.DEBUG)
    #输出格式
    formatter = logging.Formatter("%(asctime)s - %(filename)s[line:%(lineno)d] - <%(funcName)s> %(levelname)s: %(message)s")
    fileHandler.setFormatter(formatter)
    consoleHandler.setFormatter(formatter)
    #将处理器添加到logger
    logger.addHandler(fileHandler)
    logger.addHandler(consoleHandler)

    return logger
