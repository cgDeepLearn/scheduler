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
from logging.handlers import RotatingFileHandler
from config import cfg
import os

LOG_FILENAME = 'sbackend.log'


class Logger(object):
    __instance = {}

    def __init__(self, logfilepath, max_bytes, backup_count):
        logging.basicConfig(filename=logfilepath, level=logging.DEBUG)

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
    def getInstance(cls, logfilename):
        logpath, max_bytes, backup_count = cfg.get_log_cfg()
        if not os.path.exists(logpath):
            os.makedirs(logpath)

        if logfilename not in Logger.__instance:
            Logger.__instance[logfilename] = Logger(
                os.path.join(logpath, logfilename), max_bytes, backup_count)
        return Logger.__instance[logfilename]


server_logger = Logger.getInstance(LOG_FILENAME).logger
