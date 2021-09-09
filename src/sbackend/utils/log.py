"""
@Author: cgDeepLearn
@Contact:cglearningnow@163.com
@File: log.py
@Time: 2021/9/3 14:30

@docstring: 
"""
# !/usr/bin/env python3
# -*- coding: utf-8 -*-

import logging
import datetime
from logging.handlers import RotatingFileHandler
from config import cfg
import os


def shanghai(sec, what):
    shanghai_time = datetime.datetime.now() + datetime.timedelta(hours=8)
    return shanghai_time.timetuple()


class Logger(object):
    __instance = {}

    def __init__(self, logfilepath, max_bytes, backup_count):
        logging.basicConfig(filename=logfilepath, level=logging.DEBUG)
        logging.Formatter.converter = shanghai
        self.logger = logging.getLogger(logfilepath)
        self.logger.propagate = False

        # create console handler and set level to debug
        # ch = logging.StreamHandler()
        ch = RotatingFileHandler(
            logfilepath, mode='a', maxBytes=int(max_bytes),
            backupCount=int(backup_count), encoding=None, delay=0)
        ch.setLevel(logging.INFO)

        # create formatter
        formatter = logging.Formatter(fmt="%(asctime)s %(levelname)s %(threadName)s %(filename)s:%(lineno)d|%(funcName)s: %(message)s")

        # add formatter to ch
        ch.setFormatter(formatter)

        # add ch to logger
        if self.logger.hasHandlers():
            self.logger.handlers.clear()
        self.logger.addHandler(ch)

    @classmethod
    def getInstance(cls):
        logpath, max_bytes, backup_count, log_filename = cfg.get_log_cfg()
        log_filename = f"{log_filename}.log"  # 加上log后缀
        if not os.path.exists(logpath):
            os.makedirs(logpath)

        if log_filename not in Logger.__instance:
            Logger.__instance[log_filename] = Logger(
                os.path.join(logpath, log_filename), max_bytes, backup_count)
        return Logger.__instance[log_filename]


server_logger = Logger.getInstance().logger
