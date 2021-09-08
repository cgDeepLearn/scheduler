"""
@Author: cgDeepLearn
@Contact:cglearningnow@163.com
@File: worker.py
@Time: 2021/9/7 15:14

@docstring: 
"""
# !/usr/bin/env python3
# -*- coding: utf-8 -*-
import datetime
import json
import socket
import requests
import pytz
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from apscheduler.triggers.interval import IntervalTrigger
from apscheduler.events import EVENT_JOB_EXECUTED, EVENT_JOB_ERROR
from config.aps import jobstores, executors, job_defaults
from utils import logger
from config import cfg
from .process import JobParser, JobProcess


class APSWorker(object):
    __instance = None
    __inited = False

    def __new__(cls, *args, **kwargs):
        if not cls.__instance:
            cls.__instance = object.__new__(cls)
        return cls.__instance

    def __init__(self):
        if not self.__inited:
            self.__inited = True
            tz = pytz.timezone('Asia/Shanghai')
            self.scheduler = BackgroundScheduler(
                jobstores=jobstores, executors=executors,
                job_defaults=job_defaults, timezone=tz)
            self.scheduler._logger = logger
            # add_listener
            self.scheduler.add_listener(self.my_listener, EVENT_JOB_EXECUTED | EVENT_JOB_ERROR)
            self.scheduler.start()
            self.register()  # 注册worker

    def my_listener(self, event):
        if event.exception:
            self.scheduler._logger.error(f"{str(event.job_id)} error")
        else:
            self.scheduler._logger.info(f"{str(event.job_id)} run ok")

    def get_jobs(self, jobstore='redis'):
        jobs = self.scheduler.get_jobs(jobstore=jobstore)
        job_ids = list()
        for job in jobs:
            job_ids.append(job.id)
        return job_ids

    def register(self):
        """启动时，将worker信息注册到mgr"""
        loaded_jids = self.get_jobs()
        worker_config = cfg.get_services_cfg()
        mgr_host, mgr_port, worker_host = worker_config[-3:]
        mgr_url = f'http://{mgr_host}:{mgr_port}/task-mgr/register-worker/'
        _, worker_port = cfg.get_flask_cfg()[0:2]
        # worker_host = socket.gethostbyname(socket.gethostname())
        worker_host_port = f'{worker_host}:{worker_port}'
        requests_headers = {'Content-Type': 'application/json;charset=UTF-8'}
        req_data = {
            'worker_host': worker_host_port,
            'all_sub_jids': loaded_jids
        }
        register_res = requests.post(mgr_url,
                                     data=json.dumps(req_data),
                                     headers=requests_headers,
                                     timeout=5)
        logger.info(
            f'register req: {req_data}, res: {register_res.text}')

    def add_task(self, task_args, jobstore='redis'):
        """将任务下的子任务分别创建运行"""
        task_id = task_args["task_id"]
        jobs_info = task_args["jobs_info"]
        for sub_job_id, attach_info in jobs_info.items():
            self.add_job(sub_job_id, attach_info, jobstore=jobstore)
            logger.info(f"added sub_job: {sub_job_id} of {task_id}")
        logger.info(f"task_id:{task_id} added")

    def add_job(self, jid, attach_info, jobstore='redis'):
        """添加单个子任务"""
        trigger_type, expr_info = JobParser.get_trigger_info(attach_info)

        if trigger_type == "cron":
            # cron trigger
            cron_field_list = expr_info.split(' ')
            ctrigger = CronTrigger(second=cron_field_list[0],
                                   minute=cron_field_list[1],
                                   hour=cron_field_list[2],
                                   day=cron_field_list[3],
                                   month=cron_field_list[4],
                                   day_of_week=cron_field_list[5],
                                   year=cron_field_list[6])
        elif trigger_type == "interval":
            # 时间间隔trigger
            seconds = expr_info["seconds"]
            minutes = expr_info["minutes"]
            hours = expr_info["hours"]
            days = expr_info["days"]
            ctrigger = IntervalTrigger(seconds=seconds, minutes=minutes,
                                       hours=hours, days=days)
        else:
            raise Exception(f"trigger_type error: {trigger_type}")
        self.scheduler.add_job(JobProcess.run, trigger=ctrigger,
                               id=str(jid), args=(jid, attach_info),
                               jobstore=jobstore, replace_existing=True)

    def remove_task(self, task_id, sub_job_ids, jobstore='redis'):
        """删除任务下的子任务"""
        for jid in sub_job_ids:
            self.remove_job(jid, jobstore=jobstore)
        logger.info(f"task_id: {task_id} removed jids: {sub_job_ids}")

    def remove_job(self, jid, jobstore='redis'):
        """删除单个子任务"""
        self.scheduler.remove_job(jid, jobstore=jobstore)
        logger.info(f"jid: {jid} removed")
