"""
@Author: cgDeepLearn
@Contact:cglearningnow@163.com
@File: parser.py
@Time: 2021/9/6 16:36

@docstring: 
"""
# !/usr/bin/env python3
# -*- coding: utf-8 -*-
import json
from .wmap import sub_jid_separator
from utils.db import pg_execute_sql

class Parser(object):
    def __init__(self, *args, **kwargs):
        slug = kwargs.get('slug', 'base')  # 标识
        info = kwargs["info"]  # 要解析的信息，需要通过info关键字参数传递过来
        self.slug = slug
        self.info = info

    @staticmethod
    def get_task_detail(tid):
        """根据实际情况重载此方法"""
        pass

    def parse_trigger(self, trigger):
        """解析触发器， 根据实际情况重载此方法
        trigger: {
            "type": "interval",
            "value": "5 sec"
        }
        or
        trigger: {
            "type": "cron",
            "value": "5 9-18/2 * * *"
        }
        """
        # trigger类型: interval-间隔, cron-定时
        t_type = trigger["type"]  # 类型
        t_value = trigger["value"]  # 值
        if t_type == "interval":
            # 间隔
            t_value = trigger["value"]
            freq, unit = t_value.split()
            freq = int(freq)
            unit = unit.lower()
            # 单位转换为标准格式
            if unit in ["sec", "second", "seconds"]:
                unit = "seconds"
            elif unit in ["min", "minute", "minutes"]:
                unit = "minutes"
            elif unit in ["hour", "hours"]:
                unit = "hours"
            elif unit in ["day", "days"]:
                unit = "days"
            else:
                raise Exception(f"not support unit: {unit}")
            t_expr = json.dumps({unit: freq})
        elif t_type == "cron":
            # cron定时
            cron_field_len = len(t_value.split())
            if cron_field_len == 5:
                # 标准cron, 转换为扩展7位
                t_expr = f"* {t_value} *"
            elif cron_field_len == 7:
                # 相比标准cron 扩展了秒和年
                t_expr = t_value
            else:
                raise Exception(f"wrong cron_field_len: {cron_field_len}")
        else:
            raise Exception("not support trigger type: {t_type}")
        # 解析转换后的信息
        trigger_info = {
            "type": t_type,
            "t_expr": t_expr
        }
        return trigger_info

    def parse_action(self, action):
        """解析子任务实际需要执行的动作
        根据不同的动作类型，重载实现此方法
        action: {
            "func": "random",
            "kwargs": {
                "seed": 1
            }
        }
        """
        a_func = action["func"]
        kwargs = action["kwargs"]
        action_info = {
            "func": a_func,
            "kwargs": kwargs,
            "related_info": {}
        }
        return action_info

    def parse_out(self):
        """解析info,生成job相关的信息,
        需要子类重载此方法"""
        info = self.info
        res = dict()
        # res = info_parse(info)
        return res


class DemoParser(Parser):
    def __init__(self, *args, **kwargs):
        super(DemoParser, self).__init__(*args, **kwargs)
        slug = kwargs.get('slug', 'demo')
        self.slug = slug
        self.tid = self.info["tid"]
        self.task_id = self.info["task_id"]

    @staticmethod
    def get_task_detail(tid):
        """根据tid获取任务详细信息"""
        task_detail_table = "t_task_detail"
        sql = f"""
        SELECT sub_name, trigger::json, action::json
        FROM {task_detail_table}
        WHERE task_id = {tid}
        """
        sub_infos = list()
        for row in pg_execute_sql(sql):
            sub_info = {
                "sub_name": row[0],
                "trigger": row[1],
                "action": row[2]
            }
            sub_infos.append(sub_info)
        return sub_infos

    def parse_out(self):
        """demoParse的解析info实现"""
        result = dict()
        sub_infos = self.get_task_detail(self.tid)
        for sub_info in sub_infos:
            sub_name = sub_info["sub_name"]
            trigger = sub_info["trigger"]
            action = sub_info["action"]
            # 拼接成子任务id
            sub_job_id = f"{self.task_id}{sub_jid_separator}{sub_name}"
            trigger_info = self.parse_trigger(trigger)
            action_info = self.parse_action(action)
            result[sub_job_id] = {
                "trigger_info": trigger_info,
                "action_info": action_info
            }
        return result



