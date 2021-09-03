"""
@Author: cgDeepLearn
@Contact:cglearningnow@163.com
@File: main.py
@Time: 2021/9/1 14:41

@docstring: 
"""
# !/usr/bin/env python3
# -*- coding: utf-8 -*-
from flask import Flask
from flask_restful import Api
from module.interface import add_resources
from config import cfg
from utils.log import server_logger as logger


def init_app():
    f_app = Flask(__name__)
    api = Api(f_app)
    add_resources(api)
    logger.info("backend start")
    return f_app


if __name__ == "__main__":
    app = init_app()
    host, port, debug = cfg.get_flask_cfg()
    app.run(use_reloader=debug, debug=debug, host=host,
            port=port, threaded=True)
