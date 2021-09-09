"""
@Author: cgDeepLearn
@Contact:cglearningnow@163.com
@File: api.py
@Time: 2021/9/6 15:33

@docstring: 
"""
# !/usr/bin/env python3
# -*- coding: utf-8 -*-
from flask_restful import Resource
from flask import request
from utils.decorator import format_result
from views import TaskView, TaskListView


class TaskListAPI(Resource):
    @format_result
    def get(self):
        """任务列表"""
        res = TaskListView.get_tasks()
        return res

    @format_result
    def post(self):
        """新增任务"""
        task_info = request.get_json()
        res = TaskListView.add_task(task_info)
        return res


class TaskAPI(Resource):
    @format_result
    def delete(self, task_id):
        """删除任务及其下的子任务"""
        # task_id下包含的子任务
        sub_job_ids = request.get_json()["sub_job_ids"]
        res = TaskView.delete_task(task_id, sub_job_ids)
        return res


def tasks_add_resources(api):
    # 对task列表的操作(获取任务列表 和新增任务)
    api.add_resource(TaskListAPI, '/task-worker/tasks')
    # 对某个task进行查看、删除操作
    api.add_resource(TaskAPI, '/task-worker/tasks/<task_id>')
