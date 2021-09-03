"""
@Author: cgDeepLearn
@Contact:cglearningnow@163.com
@File: views.py
@Time: 2021/9/3 14:29

@docstring: 
"""
# !/usr/bin/env python3
# -*- coding: utf-8 -*-


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
        return task_id

    @classmethod
    def modify_task(cls, task_id, task_info):
        return task_info

    @classmethod
    def delete_task(cls, task_id):
        return task_id