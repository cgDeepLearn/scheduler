"""
@Author: cgDeepLearn
@Contact:cglearningnow@163.com
@File: test.py
@Time: 2021/9/6 17:30

@docstring: 
"""
# !/usr/bin/env python3
# -*- coding: utf-8 -*-

from mgr.wmap import job_map
from mgr.parser import DemoParser
from utils.redis_op import redis_op
def test_job_map():
    worker_1 = 'my_worker:1'
    sub_jids = ["taskId_1:t1", "taskId_1:t2", "taskId_2:s1"]
    job_map.set_worker(worker_1, sub_jids=sub_jids)
    r_worker = job_map.get_right_worker()
    w_cnt = job_map.get_task_cnt(r_worker)
    print(r_worker, w_cnt)
    all_tasks = job_map.get_tasks_info()
    print(all_tasks)
    job_map.delete_task_info("taskId_1")
    job_map.delete_task_info("taskId_2")
    # redis_op.delete("scheduler_job_map")
    #job_map.delete_worker(worker_1)


def test_parser():
    data = {
        "tid": 1,
        "task_id": "DemoTask_1"
    }
    dp_info = DemoParser(info=data).parse_out()
    print(dp_info)


if __name__ == "__main__":
    test_job_map()
    #test_parser()