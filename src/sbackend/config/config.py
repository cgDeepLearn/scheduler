"""
@Author: cgDeepLearn
@Contact:cglearningnow@163.com
@File: config.py
@Time: 2021/9/1 16:25

@docstring: 
"""
# !/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
from configparser import ConfigParser

LOG_SECTION_NAME = 'Log:Setup'
FLASK_SECTION_NAME = 'Flask:Setup'
REDIS_SECTION_NAME = 'Redis:Setup'
SERVICES_SECTION_NAME = 'Services:Setup'


env_config = dict(os.environ)


class Config(object):
    """
        responsible for retrieve configurations from octopus.ini
    """

    def __init__(self, configini):
        self.cfgparser = ConfigParser()
        self.cfgparser.optionxform = str
        self.cfgparser.read(configini)

    def get_log_cfg(self):
        """
        [Log:Setup]
        LOG_PATH = '/var/log/dm_dpc/'
        MAXSIZE = 5*1024*1024
        BACKUP_COUNT = 2
        """
        _meta = {}
        if self.cfgparser.has_section(LOG_SECTION_NAME):
            _meta = dict(self.cfgparser.items(LOG_SECTION_NAME))

        log_path = _meta.get('LOG_PATH', 'None')
        max_size = _meta.get('MAX_SIZE', 'None')
        backup_count = _meta.get('BACKUP_COUNT', 'None')

        return log_path, max_size, backup_count

    def get_redis_cfg(self):
        _meta = {}
        if env_config.get("REDIS_HOST"):
            # 环境变量有配置IOTDB数据库信息，使用环境变量的配置否则使用程序的默认配置
            _meta = env_config
        elif self.cfgparser.has_section(REDIS_SECTION_NAME):
            _meta = dict(self.cfgparser.items(REDIS_SECTION_NAME))
        redis_host = _meta.get('REDIS_HOST', 'None')
        redis_port = int(_meta.get('REDIS_PORT', '6379'))
        redis_pwd = _meta.get('REDIS_PASSWORD', '12345')
        redis_db = int(_meta.get('REDIS_DB', '12'))
        return redis_host, redis_port, redis_pwd, redis_db

    def get_flask_cfg(self):
        """
            [Flask:Setup]
            FLASK_PORT = 12000
            FLASK_IP = 172.24.4.47
        """
        _meta = {}
        if self.cfgparser.has_section(FLASK_SECTION_NAME):
            _meta = dict(self.cfgparser.items(FLASK_SECTION_NAME))

        flask_ip = _meta.get('FLASK_IP', '127.0.0.1')
        flask_port = int(_meta.get('FLASK_PORT', '11020'))
        flask_debug = int(_meta.get('FLASK_DEBUG', '1'))
        return flask_ip, flask_port, flask_debug

    def get_services_cfg(self):
        """获取各服务的访问名字"""
        _meta = {}
        if env_config.get("BACKEND_HOST"):
            # 环境变量有配置各服务访问名的配置信息，使用环境变量的配置否则使用程序的默认配置
            _meta = env_config
        elif self.cfgparser.has_section(SERVICES_SECTION_NAME):
            _meta = dict(self.cfgparser.items(SERVICES_SECTION_NAME))
        backend_host = _meta.get("BACKEND_HOST", "dm-backend")  # 后端服务
        iot_host = _meta.get("IOT_HOST", "dm-iot")  # iot入库
        kpi_mgr_host = _meta.get("KPI_MGR_HOST", "kpi-mgr")  # kpi-mgr
        kpi_worker_host = _meta.get("KPI_WORKER_HOST", "kpi-worker")  # kpi-worker
        rule_mgr_host = _meta.get("RULE_MGR_HOST", "rule-mgr")  # rule-mgr
        rule_worker_host = _meta.get("RULE_WORKER_HOST",
                                     "rule-worker")  # rule-worker
        dfc_host = _meta.get("DFC_HOST", "dm-dfc")  # dm-dfc
        return backend_host, iot_host, kpi_mgr_host, kpi_worker_host, rule_mgr_host, rule_worker_host, dfc_host


cfg = Config("config/cfg.ini")
