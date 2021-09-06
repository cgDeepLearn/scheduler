"""
@Author: cgDeepLearn
@Contact:cglearningnow@163.com
@File: views.py
@Time: 2021/9/6 15:33

@docstring: 
"""
# !/usr/bin/env python3
# -*- coding: utf-8 -*-


class JobListView(object):
    """任务列表的操作: 新增和查看"""
    @classmethod
    def get_jobs(cls):
        return list()

    @classmethod
    def add_job(cls, task_info):
        return task_info


class JobView(object):
    """对单个任务的操作:查看、修改、删除"""
    @classmethod
    def get_job_info(cls, job_id):
        """查看任务信息"""
        return job_id

    @classmethod
    def delete_job(cls, job_id):
        """删除任务"""
        return job_id
