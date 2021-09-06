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
from views import JobView, JobListView


class JobListAPI(Resource):
    @format_result
    def get(self):
        res = JobListView.get_jobs()
        return res

    @format_result
    def post(self):
        job_info = request.get_json()
        res = JobListView.add_job(job_info)
        return res


class JobAPI(Resource):
    @format_result
    def get(self, job_id):
        res = JobView.get_job_info(job_id)
        return res

    @format_result
    def delete(self, job_id):
        res = JobView.delete_job(job_id)
        return res


def jobs_add_resources(api):
    # 对job列表的操作(获取任务列表 和新增任务)
    api.add_resource(JobListAPI, '/task-mgr/jobs')
    # 对某个job进行查看、删除操作
    api.add_resource(JobAPI, '/task-mgr/jobs/<job_id>')