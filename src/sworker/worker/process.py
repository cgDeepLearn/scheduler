"""
@Author: cgDeepLearn
@Contact:cglearningnow@163.com
@File: process.py
@Time: 2021/9/7 15:14

@docstring: 
"""
# !/usr/bin/env python3
# -*- coding: utf-8 -*-
import json
import datetime
import random
from apscheduler.triggers.cron import CronTrigger
from apscheduler.triggers.interval import IntervalTrigger
from utils import logger


class JobParser(object):
    """子任务参数解析"""

    @classmethod
    def build_trigger(cls, trigger_info):
        """解析触发器信息，构造一个aps trigger"""
        t_type = trigger_info["type"]
        t_expr = trigger_info["expr"]
        if t_type == "cron":
            # cron trigger
            cron_field_list = t_expr.split()
            ctrigger = CronTrigger(second=cron_field_list[0],
                                   minute=cron_field_list[1],
                                   hour=cron_field_list[2],
                                   day=cron_field_list[3],
                                   month=cron_field_list[4],
                                   day_of_week=cron_field_list[5],
                                   year=cron_field_list[6])
        elif t_type == "interval":
            # 时间间隔trigger
            expr_info = json.loads(t_expr)
            seconds = expr_info.get("seconds", 0)
            minutes = expr_info.get("minutes", 0)
            hours = expr_info.get("hours", 0)
            days = expr_info.get("days", 0)
            ctrigger = IntervalTrigger(seconds=seconds, minutes=minutes,
                                       hours=hours, days=days)
        else:
            raise Exception(f"trigger_type error: {t_type}")
        return ctrigger


class JobProcess(object):
    @classmethod
    def run(cls, jid, action_info):
        """
        执行任务
        :param action_info: {
            "func": "random",
            "kwargs": {
                "seed": 1
            }
        }
        """
        try:
            func = action_info["func"]
            kwargs = action_info["kwargs"]
            cls.run_func(jid, func, kwargs)
        except Exception as e:
            logger.error(f"job_id: {jid} got error: {e}")
            raise Exception(e)

    @classmethod
    def run_func(cls, jid, func, kwargs):
        if func == "tiktok":
            logger.info(f"jid run {func} at {str(datetime.datetime.now())}")
            result = 'ok'
        elif func == "random":
            """根据种子生成的随机数a，然后用当前时间戳取余"""
            input_seed = kwargs["seed"]
            random.seed(input_seed)
            random_value = random.randint(2, 10)
            current_timestamp = int(datetime.datetime.now().timestamp())
            result = current_timestamp % random_value
        cls.process_result(jid, result)
        return result

    @classmethod
    def process_result(cls, jid, result):
        logger.info(f"jid:{jid}, result: {result}")
