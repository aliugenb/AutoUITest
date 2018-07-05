# -*- coding:utf-8 -*-
import os, sys, logging, time


def setLogPath(filePath=None, fileName='total_log.txt'):
    '''
    设置LOG生成路径和文件名
    '''
    # 设置结果生成路径
    initialPath = os.path.realpath(sys.argv[0])
    tempPath = initialPath.split('testDriver')
    if filePath is None:
        logFile = os.path.join(tempPath[0], 'testDriver', 'testLOG',
                               fileName)
    else:
        logFile = os.path.join(tempPath[0], 'testDriver', 'testLOG',
                               filePath, fileName)
    return logFile


def setResultPath(filename='result.txt'):
    '''
    设置Result生成路径和文件名
    '''
    # 设置结果生成路径
    initialPath = os.path.realpath(sys.argv[0])
    tempPath = initialPath.split('testDriver')
    targetPath = '{}{}{}{}{}'.format(tempPath[0], 'testDriver',
                                     os.sep, 'testLOG', os.sep)
    logFile = targetPath + filename
    return logFile


def logCreater(filePath):
    '''
    设置LOG生成器
    '''
    # 创建logger
    logger = logging.getLogger('ximalaya')
    logger.setLevel(logging.DEBUG)
    # 设置文本日志处理器
    fileHandler = logging.FileHandler(filePath, mode='a')
    fileHandler.setLevel(logging.INFO)
    # 设置控制台日志处理器
    consoleHandler = logging.StreamHandler()
    consoleHandler.setLevel(logging.DEBUG)
    # 输出格式
    formatter = logging.Formatter("%(asctime)s - %(filename)s[line:%(lineno)d] - <%(funcName)s> %(levelname)s: %(message)s")
    fileHandler.setFormatter(formatter)
    consoleHandler.setFormatter(formatter)
    # 将处理器添加到logger
    logger.addHandler(fileHandler)
    logger.addHandler(consoleHandler)
    return logger
