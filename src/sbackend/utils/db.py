"""
@Author: cgDeepLearn
@Contact:cglearningnow@163.com
@File: db.py
@Time: 2021/9/3 17:18

@docstring: postgres 数据库接口
"""
# !/usr/bin/env python3
# -*- coding: utf-8 -*-

import psycopg2
from config import cfg
from DBUtils.PooledDB import PooledDB
from datetime import datetime
from psycopg2 import extras as ex


class DBPool(object):
    __instance = None

    def __init__(self):
        db, user, passwd, host, port = cfg.get_db_cfg()
        self.pool = PooledDB(creator=psycopg2, mincached=1,
                             maxcached=20, maxconnections=50, blocking=True,
                             host=host, user=user, password=passwd,
                             database=db, port=int(port))

    def execute(self, sql_str):
        conn = self.pool.connection()
        cur = conn.cursor()
        cur.execute(sql_str)
        conn.commit()
        cur.close()
        conn.close()

    def executeValues(self, sql_str, values):
        conn = self.pool.connection()
        cur = conn.cursor()
        cur.execute(sql_str, values)
        conn.commit()
        cur.close()
        conn.close()

    def executeValuesRet(self, sql_str, values):
        conn = self.pool.connection()
        cur = conn.cursor()
        cur.execute(sql_str, values)
        ret = cur.fetchall()
        conn.commit()
        cur.close()
        conn.close()
        return ret

    def executeRet(self, sql_str):
        conn = self.pool.connection()
        cur = conn.cursor()
        cur.execute(sql_str)
        ret = cur.fetchall()
        conn.commit()
        cur.close()
        conn.close()
        return ret

    def executeMany(self, sql_str, datalist):
        conn = self.pool.connection()
        cur = conn.cursor()
        ex.execute_values(cur, sql_str, datalist, page_size=1000)
        conn.commit()
        cur.close()
        conn.close()

    def selectByColumn(self, sqlCode):
        conn = self.pool.connection()
        cur = conn.cursor()
        cur.execute(sqlCode)
        rows = cur.fetchall()
        header = cur.description
        columnList = [h[0] for h in header]
        typeList = [h[1] for h in header]
        indexList = [i for i in range(len(rows))]
        return {"index": indexList, "columns": columnList,
                "types": typeList, "data": rows}

    @staticmethod
    def getInstance():
        if DBPool.__instance is None:
            DBPool.__instance = DBPool()
        return DBPool.__instance


def pg_execute_sql(sql_str):
    ret = DBPool.getInstance().executeRet(sql_str)
    return ret
