"""
@Author: cgDeepLearn
@Contact:cglearningnow@163.com
@File: interface.py
@Time: 2021/9/1 16:04

@docstring: 
"""
# !/usr/bin/env python3
# -*- coding: utf-8 -*-
from config import cfg
from module.hello.api import hello_add_resources
from module.tasks.api import tasks_add_resources


def add_resources(api):
    cfg.get_redis_cfg()
    hello_add_resources(api)  # hello 模块
    tasks_add_resources(api)  # tasks 模块
