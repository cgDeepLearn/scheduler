"""
@Author: cgDeepLearn
@Contact:cglearningnow@163.com
@File: views.py
@Time: 2021/9/3 14:29

@docstring: 
"""
# !/usr/bin/env python3
# -*- coding: utf-8 -*-
from utils.db import pg_execute_sql


class TaskListView(object):
    """任务列表的操作: 新增和查看"""
    @classmethod
    def get_tasks(cls):
        return list()

    @classmethod
    def add_task(cls, task_info):
        return task_info


class TaskView(object):
    """对单个任务的操作:查看、修改、删除"""
    @classmethod
    def get_task_info(cls, task_id):
        """查看任务信息"""
        return task_id

    @classmethod
    def modify_task(cls, task_id, task_info):
        """修改任务"""
        return task_info

    @classmethod
    def delete_task(cls, task_id):
        """删除任务"""
        return task_id
