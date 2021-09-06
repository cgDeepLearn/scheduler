"""
@Author: cgDeepLearn
@Contact:cglearningnow@163.com
@File: api.py
@Time: 2021/9/3 14:28

@docstring: api接口定义
"""
# !/usr/bin/env python3
# -*- coding: utf-8 -*-

from flask_restful import Resource
from flask import request
from utils.decorator import format_result
from .views import TaskView, TaskListView


class TaskListAPI(Resource):
    @format_result
    def get(self):
        res = TaskListView.get_tasks()
        return res

    @format_result
    def post(self):
        task_info = request.get_json()
        res = TaskListView.add_task(task_info)
        return res


class TaskAPI(Resource):
    @format_result
    def get(self, task_id):
        res = TaskView.get_task_info(task_id)
        return res

    @format_result
    def put(self, task_id):
        new_task_info = request.get_json()
        res = TaskView.modify_task(task_id, new_task_info)
        return res

    @format_result
    def delete(self, task_id):
        res = TaskView.delete_task(task_id)
        return res


def tasks_add_resources(api):
    # 对任务列表的操作(获取任务列表 和新增任务)
    api.add_resource(TaskListAPI, '/tasks')
    # 对某个任务进行查看、修改、删除操作
    api.add_resource(TaskAPI, '/tasks/<task_id>')
