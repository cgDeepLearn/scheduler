"""
@Author: cgDeepLearn
@Contact:cglearningnow@163.com
@File: parser.py
@Time: 2021/9/6 16:36

@docstring: 
"""
# !/usr/bin/env python3
# -*- coding: utf-8 -*-
from .wmap import sub_jid_separator


class Parser(object):
    def __init__(self, *args, **kwargs):
        slug = kwargs.get('slug', 'base')  # 标识
        info = kwargs["info"]  # 要解析的信息，需要通过info关键字参数传递过来
        self.slug = slug
        self.info = info

    def parse_out(self):
        """解析info,生成jon相关的信息"""
        info = self.info
        res = dict()
        # res = info_parse(info)
        return res


class DemoParser(Parser):
    def __init__(self, *args, **kwargs):
        super(DemoParser, self).__init__(*args, **kwargs)
        slug = kwargs.get('slug', 'demo')
        self.slug = slug
        self.task_id = self.info["task_id"]

    def parse_out(self):
        """demoParse的解析info实现"""
        res = dict()
        sub_job_names = ["ta", "tb"]
        sub_job_ids = [f"{self.task_id}{sub_jid_separator}{name}" for name in sub_job_names]
        for sub_job_id in sub_job_ids:
            res[sub_job_id] = {
                "trigger_info": {
                    "type": "interval",
                    "value": {
                        "minutes": 1
                    }
                },
                "related_info": {}
            }
        return res



