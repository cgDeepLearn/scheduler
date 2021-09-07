"""
@Author: cgDeepLearn
@Contact:cglearningnow@163.com
@File: process.py
@Time: 2021/9/7 15:14

@docstring: 
"""
# !/usr/bin/env python3
# -*- coding: utf-8 -*-


class JobParser(object):
    """子任务参数解析"""

    @classmethod
    def get_trigger_info(cls, attach_info):
        """获取定时触发器的相关信息
        interval: 时间间隔
        cron: cron表达式
        """
        trigger_info = attach_info["trigger_info"]
        trigger_type = trigger_info["type"]
        trigger_expr = trigger_info["value"]
        if trigger_type == "interval":
            # 时间间隔类型读取间隔信息
            seconds = trigger_expr.get("seconds", 0)
            minutes = trigger_expr.get("minutes", 0)
            hours = trigger_expr.get("hours", 0)
            days = trigger_expr.get("days", 0)
            expr_info = {
                "seconds": seconds,
                "minutes": minutes,
                "hours": hours,
                "days": days
            }
        else:
            # cron类型 ,cron表达式为字符串
            expr_info = trigger_expr
        return trigger_type, expr_info


class JobProcess(object):
    @classmethod
    def run(cls):
        pass
