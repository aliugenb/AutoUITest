# -*- coding:utf-8 -*-
from XFramework.base_exception import BaseError


class SleepOutError(BaseError):
    """
    Exception raised for sleep out.

    Attributes:
       expression -- sleep out expression in which the error occurred
       message -- explanation of the error
    """

    def __init__(self, expression=u'SleepOutError', message=u'等待元素出现超时，请查看元素是否在此页面'):
       self.expression = expression
       self.message = message

    def __str__(self):
        return str(self.expression + ': ' + self.message)
