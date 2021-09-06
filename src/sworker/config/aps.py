"""
@Author: ChenGang
@Contact:chengang@neucloud.cn
@File: aps.py
@Time: 2021/8/19 10:00

@docstring: 
"""
# !/usr/bin/env python3
# -*- coding: utf-8 -*-
import socket
import redis
from apscheduler.jobstores.redis import RedisJobStore
from apscheduler.executors.pool import ThreadPoolExecutor, ProcessPoolExecutor
from config import cfg

r_host, r_port, r_pwd, r_db = cfg.get_redis_cfg()

redis_config = {
    'host': r_host,
    'port': r_port,
    'db': r_db,
    'password': r_pwd
}

redis_pool = redis.ConnectionPool(**redis_config)
uniq_worker_flag = f"worker_{cfg.get_worker_index()}"
redis_jobs_key = f"apscheduler.jobs_worker{uniq_worker_flag}"
redis_run_times_key = f"apscheduler.run_times_{uniq_worker_flag}"

jobstores = {
    # 'redis': RedisJobStore(**redis_config, jobs_key=redis_jobs_key, run_times_key=redis_run_times_key)
    'redis': RedisJobStore(connection_pool=redis_pool,
                           jobs_key=redis_jobs_key,
                           run_times_key=redis_run_times_key)
    # 'sqlite': SQLAlchemyJobStore(url='sqlite:///jobs.sqlite')
}


executors = {
    # 默认使用线程池
    'default': ThreadPoolExecutor(100),
    # 进程池
    'process_pool': ProcessPoolExecutor(10)
}

job_defaults = {
    # 开启job合并
    'coalesce':  True,
    # job最大实例限制数
    'max_instance': 1,
    'misfire_grace_time': 30,
}
