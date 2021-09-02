"""
@Author: cgDeepLearn
@Contact:cglearningnow@163.com
@File: wmap.py
@Time: 2021/9/1 16:20

@docstring: 
"""
# !/usr/bin/env python3
# -*- coding: utf-8 -*-

from ..utils.redis_op import redis_op


class Singleton(object):
    """单例类装饰器"""

    def __init__(self, cls):
        self._cls = cls
        self._instance = {}

    def __call__(self):
        if self._cls not in self._instance:
            self._instance[self._cls] = self._cls()
        return self._instance[self._cls]


@Singleton
class JobMap(object):
    def __init__(self, job_map_key="rule_job_map", worker_map_key="rule_worker_map"):
        self._job_map_key = job_map_key
        self._worker_map_key = worker_map_key

    def has_job(self, jid):
        return redis_op.hexists(self._job_map_key, jid)

    def create_job(self, jid, worker):
        #
        redis_op.hset(self._job_map_key, jid, worker)
        current_cnt = self.get_job_cnt(worker)
        new_cnt = current_cnt + 1
        self.set_job_cnt(worker, new_cnt)

    def delete_job(self, jid):
        job_at = self.find_worker(jid)
        redis_op.hdel(self._job_map_key, jid)
        current_cnt = self.get_job_cnt(job_at)
        new_cnt = current_cnt - 1
        self.set_job_cnt(job_at, new_cnt)

    def find_worker(self, jid):
        worker = redis_op.hget(self._job_map_key, jid)
        return worker

    def set_worker(self, worker, jids=None):
        if jids:
            j_cnt = len(jids)
        else:
            j_cnt = 0
        # 设置cnt
        self.set_job_cnt(worker, j_cnt)
        # 设置每个jid
        for jid in jids:
            redis_op.hset(self._job_map_key, jid, worker)

    def get_job_cnt(self, worker):
        cnt = int(redis_op.hget(self._worker_map_key, worker))
        return cnt

    def set_job_cnt(self, worker, cnt):
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


job_map = JobMap()
