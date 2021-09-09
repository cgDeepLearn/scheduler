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
from views import TaskView, TaskListView, RegisterView


task_id_format = "DemoTask_{}"


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
        tid = task_info["tid"]
        data = {
            # 用于存储与redis的key
            "tid": tid,
            "task_id": task_id_format.format(tid),
            "task_info": task_info
        }
        res = TaskListView.add_task(data)
        return res


class TaskAPI(Resource):
    @format_result
    def get(self, tid):
        """任务详情"""
        task_id = task_id_format.format(tid)
        res = TaskView.get_task_info(task_id)
        return res

    @format_result
    def delete(self, tid):
        """删除任务"""
        task_id = task_id_format.format(tid)
        res = TaskView.delete_task(task_id)
        return res


class RegisterAPI(Resource):
    @format_result
    def post(self):
        register_info = request.get_json()
        res = RegisterView.handle(register_info)
        return res


def tasks_add_resources(api):
    # 对task列表的操作(获取任务列表 和新增任务)
    api.add_resource(TaskListAPI, '/task-mgr/tasks')
    # 对某个task进行查看、删除操作
    api.add_resource(TaskAPI, '/task-mgr/tasks/<tid>')
    api.add_resource(RegisterAPI, '/task-mgr/register-worker')
