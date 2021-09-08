"""
@Author: cgDeepLearn
@Contact:cglearningnow@163.com
@File: manager.py
@Time: 2021/9/6 15:17

@docstring: 
"""
# !/usr/bin/env python3
# -*- coding: utf-8 -*-
import json
import requests
from utils import logger
from .wmap import job_map
from .parser import DemoParser

requests_headers = {'Content-Type': 'application/json;charset=UTF-8'}


class DemoManager(object):
    """任务调度"""
    @classmethod
    def create_task(cls, data):
        """创建job,支持一个任务包含多个子任务
        解析任务，生成job相关信息，并将job运行请求发送到worker上"""
        task_id = data["task_id"]
        # 找到合适的worker来运行
        right_worker = job_map.get_right_worker()
        if not right_worker:
            raise Exception(" no right worker")
        job_parser = DemoParser(info=data)
        jobs_info = job_parser.parse_out()
        sub_jod_ids = list(jobs_info.keys())  # 子任务列表
        # run_task request
        run_task_url = f'http://{right_worker}/task-worker/tasks'
        req_data = {
            "task_id": task_id,
            "jobs_info": jobs_info
        }
        res = {"ret": "ok"}
        # res = requests.post(run_task_url, data=json.dumps(req_data),
        #                     headers=requests_headers).json()
        logger.info(f"create_req: {req_data}, create_res: {res}")
        # map 操作对应信息
        job_map.create_task_info(task_id, sub_jod_ids, right_worker)
        return True

    @classmethod
    def delete_task(cls, task_id):
        """删除任务"""
        # 找到任务运行在哪个worker
        task_at_worker = job_map.find_worker(task_id)
        if not task_at_worker:
            raise Exception("task not Existed")
        sub_jids = job_map.get_task_info(task_id)["sub_jids"]
        req_data = {
            "sub_job_ids": sub_jids
        }
        # 向对应worker发送删除任务请求
        remove_task_url = f'http://{task_at_worker}/task-worker/tasks/{task_id}'
        res = {"ret": "ok"}
        # res = requests.delete(remove_task_url,data=json.dumps(req_data),
        #                       headers=requests_headers).json()
        logger.info(f"task_id: {task_id} delete_res: {res}")
        # 删除job_map对应信息
        job_map.delete_task_info(task_id)
        return True

    @classmethod
    def handle_register(cls, data):
        """接收worker启动时注册到mgr中的请求"""
        worker_host = data["worker_host"]
        all_sub_jids = data["all_sub_jids"]  # 所有子任务id的列表
        job_map.set_worker(worker_host, sub_jids=all_sub_jids)
        logger.info(f"registered {worker_host}, info: {data}")
        return
