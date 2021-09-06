"""
@Author: cgDeepLearn
@Contact: cglearningnow@163.com
@File: redis_op.py
@Time: 2021/4/20 17:50

@docstring: 
"""
# !/usr/bin/env python3
# -*- coding: utf-8 -*-

import redis
import json
from config import cfg


class RedisOp(object):
    def __init__(self, host, port, db, password=None):
        pool = redis.ConnectionPool(host=host, port=port,
                                    db=db, password=password,
                                    decode_responses=True)
        self.conn = redis.Redis(connection_pool=pool)

    def pipeline(self):
        return self.conn.pipeline()

    def exists(self, key):
        return self.conn.exists(key)

    def hexists(self, key, field):
        return self.conn.hexists(key, field)

    def get(self, key):
        return self.conn.get(key)

    def hget(self, key, field):
        return self.conn.hget(key, field)

    def hgetall(self, key):
        return self.conn.hgetall(key)

    def set(self, key, value, ex=None):
        return self.conn.set(key, value, ex=ex)  # 设置过期时间,默认没有

    def hset(self, key, field, value):
        return self.conn.hset(key, field, value)

    def hsetnx(self, key, field, value):
        return self.conn.hsetnx(key, field, value)

    def hget_uniq(self, key, field):
        return self.conn.hget(key, field)

    def hset_uniq(self, key, filed, value):
        return self.conn.hset(key, filed, value)

    def hsetnx_uniq(self, key, filed, value):
        return self.conn.hsetnx(key, filed, value)

    def hincrby(self, key, filed, amount):
        return self.conn.hincrby(key, filed, amount)

    def delete(self, key):
        return self.conn.delete(key)

    def hdel(self, key, field):
        return self.conn.hdel(key, field)

    def sismember(self, key, value):
        return self.conn.sismember(key, value)


redis_host, redis_port, redis_pwd, redis_db = cfg.get_redis_cfg()
redis_op = RedisOp(
    host=redis_host, port=redis_port, db=int(redis_db), password=redis_pwd)
