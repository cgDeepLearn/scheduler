"""
@Author: cgDeepLearn
@Contact:cglearningnow@163.com
@File: main.py
@Time: 2021/9/1 14:46

@docstring: mgr main
"""
# !/usr/bin/env python3
# -*- coding: utf-8 -*-
from flask import Flask
from flask_restful import Api
from config import cfg
from utils import logger
from api import tasks_add_resources
from mgr.wmap import job_map


def init_app():
    f_app = Flask(__name__)
    api = Api(f_app)
    tasks_add_resources(api)
    logger.info("mgr start")
    return f_app


if __name__ == "__main__":
    flask_ip, flask_port, flask_debug = cfg.get_flask_cfg()
    job_map.delete_worker_map()  # mgr启动时删除worker_map
    app = init_app()
    app.run(host=flask_ip, port=flask_port, debug=flask_debug)
