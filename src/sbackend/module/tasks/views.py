"""
@Author: cgDeepLearn
@Contact:cglearningnow@163.com
@File: views.py
@Time: 2021/9/3 14:29

@docstring: 
"""
# !/usr/bin/env python3
# -*- coding: utf-8 -*-
import json
import requests
from utils import logger
from utils.db import pg_execute_sql, DBPool
from psycopg2 import extras as pg_extras
from config import cfg


task_table = "t_task"
task_detail_table = "t_task_detail"


class TaskListView(object):
    """任务列表的操作: 新增和查看"""
    @classmethod
    def get_tasks(cls):
        sql = f"""
            SELECT a.id, a.name, COUNT(1), a.create_time, a.update_time
            FROM {task_table}  AS a INNER JOIN {task_detail_table} AS b
            ON a.id = b.task_id
            WHERE NOT a.is_delete AND NOT b.is_delete
            GROUP BY a.id
            ORDER BY a.update_time DESC
        """
        result = list()
        for row in pg_execute_sql(sql):
            task_id = row[0]
            task_name = row[1]
            sub_task_count = row[2]
            create_time = row[3].strftime("%Y-%m-%d %H:%M:%S")
            update_time = row[4].strftime("%Y-%m-%d %H:%M:%S")
            task_info = {
                "taskId": task_id,
                "taskName": task_name,
                "subTaskCount": sub_task_count,
                "createTime": create_time,
                "updateTime": update_time
            }
            result.append(task_info)
        return result

    @classmethod
    def add_task(cls, task_info):
        """添加任务"""
        task_name = task_info["taskName"]
        user = "admin"  # get from front
        sub_task_info = task_info["taskDetail"]
        conn = DBPool.getInstance().pool.connection()
        cur = conn.cursor()
        try:
            # 插入到任务表
            task_insert_sql = f"""
            INSERT INTO {task_table}(name, create_by, update_by)
            values('{task_name}', '{user}', '{user}')
            returning id
            """

            cur.execute(task_insert_sql)
            added_task_id = cur.fetchall()[0][0]
            # detail表插入
            task_detail_sql = f"""
            INSERT INTO {task_detail_table}(task_id, sub_name, trigger, action)
            VALUES %s
            """
            detail_values = list()
            for sub_info in sub_task_info:
                sub_name = sub_info["subName"]
                sub_trigger = json.dumps(sub_info["subTrigger"])
                sub_action = json.dumps(sub_info["subAction"])
                one_record = (added_task_id, sub_name, sub_trigger, sub_action)
                detail_values.append(one_record)
            if not detail_values:
                raise Exception("no task detail info")
            pg_extras.execute_values(cur, task_detail_sql, detail_values, page_size=1000)
            conn.commit()
            # 向mgr发送新增任务请求
            mgr_host, mgr_port = cfg.get_service_cfg()[1:3]
            mgr_host_port = f"{mgr_host}:{mgr_port}"
            req_data = {"tid": added_task_id}
            r_headers = {'Content-Type': 'application/json;charset=UTF-8'}
            mgr_url = f"http://{mgr_host_port}/task-mgr/tasks"
            res = requests.post(mgr_url, data=json.dumps(req_data),
                                headers=r_headers).json()
            if not res.get("success"):
                # rollback inserted sql or update  is_delete='t'
                raise Exception(res["message"])
            cur.close()
            conn.close()
        except Exception as e:
            conn.rollback()
            logger.error("task insert error")
            cur.close()
            conn.close()
            raise Exception(e)
        return added_task_id


class TaskView(object):
    """对单个任务的操作:查看、修改、删除"""
    @classmethod
    def get_task_info(cls, task_id):
        """查看任务信息"""
        sql = f"""
            SELECT a.name, b.sub_name,b.trigger::json,b.action::json
            FROM {task_table} AS a INNER JOIN {task_detail_table} AS b
            ON a.id = b.task_id
            WHERE NOT a.is_delete AND NOT b.is_delete
            AND a.id = {task_id}
        """
        sub_infos = list()
        task_name = None
        for row in pg_execute_sql(sql):
            task_name = row[0]
            sub_name = row[1]
            sub_trigger = row[2]
            sub_action = row[3]
            sub_info = {
                "subName": sub_name,
                "subTrigger": sub_trigger,
                "subAction": sub_action
            }
            sub_infos.append(sub_info)
        if not task_name:
            raise Exception("任务不存在")
        else:
            result = {
                "taskName": task_name,
                "taskDetail": sub_infos
            }
        return result

    @classmethod
    def modify_task(cls, task_id, task_info):
        """修改任务"""
        pass
        return task_info

    @classmethod
    def delete_task(cls, task_id):
        """删除任务"""
        # 逻辑删除
        delete_task_sql = f"""
        UPDATE {task_table} SET is_delete = 't'
        WHERE id = {task_id}
        """
        delete_task_detail_sql = f"""
        UPDATE {task_detail_table} SET is_delete = 't'
        WHERE task_id = {task_id}
        """
        conn = DBPool.getInstance().pool.connection()
        cur = conn.cursor()
        try:
            cur.execute(delete_task_sql)
            cur.execute(delete_task_detail_sql)
            mgr_host, mgr_port = cfg.get_service_cfg()[1:3]
            mgr_host_port = f"{mgr_host}:{mgr_port}"
            req_data = {"tid": task_id}
            r_headers = {'Content-Type': 'application/json;charset=UTF-8'}
            mgr_url = f"http://{mgr_host_port}/task-mgr/tasks/{task_id}"
            res = requests.delete(mgr_url, data=json.dumps(req_data),
                                headers=r_headers).json()
            if not res.get("success"):
                raise Exception(res["message"])
            conn.commit()
        except Exception as e:
            conn.rollback()
            logger.error("delete task got error")
        finally:
            cur.close()
            conn.close()
        return 'ok'
