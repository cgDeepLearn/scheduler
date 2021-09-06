"""
@Author: cgDeepLearn
@Contact:cglearningnow@163.com
@File: decorator.py
@Time: 2021/9/3 14:30

@docstring: 
"""
# !/usr/bin/env python3
# -*- coding: utf-8 -*-

from functools import wraps
from flask.wrappers import Response
from .log import server_logger as logger


def format_result(func):
    """包装结果格式返回给调用者"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        ret = {}
        try:
            data = func(*args, **kwargs)
            if type(data) is Response:
                return data
            ret['data'] = data
            ret['success'] = True
            ret['message'] = 'Succeed'
        except Exception as e:
            ret['message'] = str(e)
            ret['data'] = None
            ret['success'] = False
        logger.info(f"request_{func}, result: {ret}")
        return ret
    return wrapper
