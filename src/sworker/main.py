"""
@Author: cgDeepLearn
@Contact:cglearningnow@163.com
@File: main.py
@Time: 2021/9/1 14:46

@docstring: 
"""
# !/usr/bin/env python3
# -*- coding: utf-8 -*-
from flask import Flask
from flask_restful import Api
from config import cfg
from utils import logger
from api import tasks_add_resources


def init_app():
    f_app = Flask(__name__)
    api = Api(f_app)
    tasks_add_resources(api)
    logger.info("worker start")
    return f_app


if __name__ == "__main__":
    flask_ip, flask_port, flask_debug = cfg.get_flask_cfg()
    app = init_app()
    app.run(host=flask_ip, port=flask_port, debug=flask_debug)
