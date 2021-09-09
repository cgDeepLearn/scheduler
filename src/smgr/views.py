"""
@Author: cgDeepLearn
@Contact:cglearningnow@163.com
@File: views.py
@Time: 2021/9/6 15:33

@docstring: 接口实现视图
"""
# !/usr/bin/env python3
# -*- coding: utf-8 -*-
from mgr.manager import DemoManager
from mgr.wmap import demo_job_map


class TaskListView(object):
    """任务列表的操作: 新增和查看"""
    @classmethod
    def get_tasks(cls):
        res = demo_job_map.get_tasks_info()
        return res

    @classmethod
    def add_task(cls, data):
        res = DemoManager.create_task(data)
        return res


class TaskView(object):
    """对单个任务的操作:查看、修改、删除"""
    @classmethod
    def get_task_info(cls, task_id):
        """查看任务信息"""
        return task_id

    @classmethod
    def delete_task(cls, task_id):
        """删除任务"""
        DemoManager.delete_task(task_id)
        return task_id


class RegisterView(object):
    """处理worker的注册请求"""
    @classmethod
    def handle(cls, data):
        res = DemoManager.handle_register(data)
        return res
