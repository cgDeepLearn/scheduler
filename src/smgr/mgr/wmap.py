"""
@Author: cgDeepLearn
@Contact:cglearningnow@163.com
@File: wmap.py
@Time: 2021/9/1 16:20

@docstring: 
"""
# !/usr/bin/env python3
# -*- coding: utf-8 -*-
import json
from utils.redis_op import redis_op

sub_jid_separator = ':'  # 子任务redis key的分隔符


class Singleton(object):
    """单例类装饰器"""

    def __init__(self, cls):
        self._cls = cls
        self._instance = {}

    def __call__(self):
        if self._cls not in self._instance:
            self._instance[self._cls] = self._cls()
        return self._instance[self._cls]


class JobMap(object):
    def __init__(self, job_map_key="scheduler_job_map", worker_map_key="scheduler_worker_map"):
        self._job_map_key = job_map_key
        self._worker_map_key = worker_map_key

    def has_task(self, task_id):
        return redis_op.hexists(self._job_map_key, task_id)

    def create_task_info(self, task_id, sub_jids, worker):
        """task_id: 任务id
        sub_job_suffixes: 子任务后缀列表"""
        jid_info = {
            "worker": worker,
            "sub_jids": sub_jids
        }
        redis_op.hset(self._job_map_key, task_id, json.dumps(jid_info))
        current_cnt = self.get_task_cnt(worker)
        new_cnt = current_cnt + 1
        self.set_task_cnt(worker, new_cnt)

    def get_tasks_info(self):
        """获取当前运行所有任务的信息"""
        all_tasks = list()
        for task_id, sub_job_info in redis_op.hgetall(self._job_map_key).items():
            sub_job_info_dict = json.loads(sub_job_info)
            task_info = {
                "task_id": task_id,
                "worker": sub_job_info_dict["worker"],
                "sub_job_cnt": len(sub_job_info_dict["sub_jids"])
            }
            all_tasks.append(task_info)
        return all_tasks

    def delete_task_info(self, task_id):
        job_at = self.find_worker(task_id)
        redis_op.hdel(self._job_map_key, task_id)
        current_cnt = self.get_task_cnt(job_at)
        new_cnt = current_cnt - 1
        self.set_task_cnt(job_at, new_cnt)

    def get_task_info(self, task_id):
        task_info = json.loads(redis_op.hget(self._job_map_key, task_id))
        return task_info

    def find_worker(self, task_id):
        task_info = self.get_task_info(task_id)
        worker = task_info["worker"]
        return worker

    def set_worker(self, worker, sub_jids=None):
        jid_infos = dict()  # 各jid包含的子任务的字典
        if sub_jids:
            for sub_jid in sub_jids:
                # sub_jid例子: task_id:sub_job1
                task_id, sub_jid_name = sub_jid.split(sub_jid_separator)
                if task_id not in jid_infos.keys():
                    jid_infos[task_id] = list()
                jid_infos[task_id].append(sub_jid)
        self.set_task_cnt(worker, 0)  # 初始化为0
        # 设置每个jid的信息
        for task_id, sub_list in jid_infos.items():
            self.create_task_info(task_id, sub_list, worker)

    def get_task_cnt(self, worker):
        cnt = int(redis_op.hget(self._worker_map_key, worker))
        return cnt

    def set_task_cnt(self, worker, cnt):
        redis_op.hset(self._worker_map_key, worker, cnt)

    def get_right_worker(self):
        """找出最少使用的worker"""
        min_cnt = 100000
        min_worker = ''
        for worker, cnt in redis_op.hgetall(self._worker_map_key).items():
            cnt = int(cnt)
            if cnt < min_cnt:
                min_cnt = cnt
                min_worker = worker
        return min_worker

    def delete_worker(self, worker):
        redis_op.hdel(self._worker_map_key, worker)

    def delete_worker_map(self):
        redis_op.delete(self._worker_map_key)


demo_job_map = JobMap(job_map_key="demo_scheduler_job_map",
                      worker_map_key="demo_scheduler_worker_map")
