"""
@Author: cgDeepLearn
@Contact:cglearningnow@163.com
@File: views.py
@Time: 2021/9/6 15:33

@docstring: 接口实现视图
"""
# !/usr/bin/env python3
# -*- coding: utf-8 -*-
from worker.worker import aps_worker, sub_jid_separator
from utils import logger


class TaskListView(object):
    """任务列表的操作: 新增和查看"""
    @classmethod
    def get_tasks(cls):
        """查看所有任务及其下的子任务"""
        tasks_info = dict()
        all_job_ids = aps_worker.get_jobs()
        for sub_jid in all_job_ids:
            # sub_jid例子: task_id:sub_job1
            task_id, sub_jid_name = sub_jid.split(sub_jid_separator)
            if task_id not in tasks_info.keys():
                tasks_info[task_id] = list()
            tasks_info[task_id].append(sub_jid)
        return tasks_info

    @classmethod
    def add_task(cls, data):
        task_id = data["task_id"]
        jobs_info = data["jobs_info"]
        logger.info(f"received add task: {task_id}, jobs_info: {jobs_info}")
        try:
            aps_worker.add_task(data)
        except Exception as e:
            logger.error(f"add task:{task_id} got error: {e}")
            raise Exception(e)
        return "ok"


class TaskView(object):
    """对单个任务的操作:查看、修改、删除"""

    @classmethod
    def delete_task(cls, task_id, sub_job_ids):
        """删除任务"""
        aps_worker.remove_task(task_id, sub_job_ids)
        return task_id
