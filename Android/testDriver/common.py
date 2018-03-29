# -*- coding:utf-8 -*-
import sys
import os


def pathGet():
    """
    返回XFramework所在路径
    """
    # targetPath = sys.argv[0]
    targetPath = os.path.realpath(sys.argv[0])
    targetPath = targetPath.split('uiautotest_excel')
    targetPath = targetPath[0] + 'uiautotest_excel'
    sys.path.append(targetPath)
