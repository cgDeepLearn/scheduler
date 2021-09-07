"""
@Author: cgDeepLearn
@Contact:cglearningnow@163.com
@File: views.py
@Time: 2021/9/6 15:33

@docstring: 接口实现视图
"""
# !/usr/bin/env python3
# -*- coding: utf-8 -*-
from worker import APSWorker


class TaskListView(object):
    """任务列表的操作: 新增和查看"""
    @classmethod
    def get_tasks(cls):
        res = 1
        return res

    @classmethod
    def add_task(cls, data):
        res = 2
        return res


class TaskView(object):
    """对单个任务的操作:查看、修改、删除"""

    @classmethod
    def delete_task(cls, task_id, sub_job_ids):
        """删除任务"""
        APSWorker.remove_task(task_id, sub_job_ids)
        return task_id
