# scheduler

A interface integrate with manager and worker  running in backend docker

集成APScheduler 的任务调度框架，运行于docker环境, 支持worker扩展

## 环境准备

安装好`docker` 和`docker-compose`

- [x] `docker` version: 20.10.5
- [x] `docker-compose` version 1.29.2
- [x] `python` version: 3.8.5 (docker镜像里)
    - [x] DBUtils==1.3.0
    - [x] psycopg2==2.8.6
    - [x] Flask==1.1.2
    - [x] Flask-RESTful==0.3.8
    - [x] APScheduler==3.7.0
    - [x] redis==3.5.3
    - [x] requests==2.25.1
  
## 快速开始

1. 进入项目主目录，构建python-base基础环境镜像包，用来快速构建其他镜像

```shell
bash build-python-base.sh
#...
#Removing intermediate container 19c1b58de2d2
# ---> 075b6db01bfb
#Successfully built 075b6db01bfb
#Successfully tagged python-base:latest

```

此步骤得到一个`python-base:latest`的镜像，里面含有项目依赖的python库

2. 构建项目镜像,主要包含`sbackend`、`smgr`、`sworker`三个镜像，具体配置查看[docker-compose.yml](./docker-compose.yml)文件

```shell
docker-compose -f docker-compose build
```

3. 运行项目

- 创建项目docker子网(看[docker-compose.yml](./docker-compose.yml)里`net`的名字)

```shell
docker network create scheduler_net
docker network ls
```

- 初步运行

```shell
docker-compose -f docker-compose up -d
```

项目包含`sredis`、`spostgres`、`sbackend`、`smgr`以及两个`sworker`(sworker1和sworker2)容器，
初次运行会从docker仓库拉取`redis`和`postgres`两个镜像的对应版本

4. 初始化数据库

```shell
docker cp scripts/backend.sql scheduler_spostgres_1:/tmp
docker exec -it scheduler_spostgres_1 sh
psql --username "$POSTGRES_USER" --dbname "$POSTGRES_DATABASE" -f /tmp/backend.sql
exit
```

5. 调用restful接口测试

`postman`测试

- 获取任务列表

```shell
GET http://your-host:40001/tasks   (Headers: Content-Type:application/json; charset=utf-8)

RESPONSE:
{
    "data": [],
    "success": true,
    "message": "Succeed"
}
```

- 新增任务

```shell
POST http://your-host:40001/tasks 

data: {
        "taskName": "任务r",
        "taskDetail": [
            {
                "subName": "t-random",
                "subTrigger": {
                    "type": "cron",
                    "value": "12-30/4 * * * * * *"
                },
                "subAction": {
                    "func": "random",
                    "kwargs": {
                        "seed": 4
                    }
                }
            },
            {
                "subName": "t-tiktok",
                "subTrigger": {
                    "type": "interval",
                    "value": "4 sec"
                },
                "subAction": {
                    "func": "tiktok",
                    "kwargs": {}
                }
            }
        ]
    }

RESPONSE:

{
  "data": {
    "taskId": 1
  },
  "success": true,
  "message": "Succeed"
}
```

- 查看某个任务详情

```shell
GET http://your-host:40001/tasks/1

RESPONSE:
{
  {
    "data": {
        "taskName": "任务r",
        "taskDetail": [
            {
                "subName": "t-random",
                "subTrigger": {
                    "type": "cron",
                    "value": "12-30/4 * * * * * *"
                },
                "subAction": {
                    "func": "random",
                    "kwargs": {
                        "seed": 4
                    }
                }
            },
            {
                "subName": "t-tiktok",
                "subTrigger": {
                    "type": "interval",
                    "value": "4 sec"
                },
                "subAction": {
                    "func": "tiktok",
                    "kwargs": {}
                }
            }
        ]
    },
    "success": true,
    "message": "Succeed"
}
}
```

- 删除任务

```shell
DELETE http://your-host:40001/tasks/1

RESPONSE:

{
    "data": "ok",
    "success": true,
    "message": "Succeed"
}
```

6. 查看日志

由于几个容器都做了日志目录挂载到宿主机的`/var/log/xxx`目录,可以到宿主机的对应目录下去查看日志

```vim /var/log/sbackend/sbackend.log```

```log
INFO:werkzeug:192.168.1.165 - - [10/Sep/2021 02:38:46] "GET /tasks HTTP/1.1" 200 -
DEBUG:urllib3.connectionpool:Starting new HTTP connection (1): smgr:40002
DEBUG:urllib3.connectionpool:http://smgr:40002 "DELETE /task-mgr/tasks/2 HTTP/1.1" 200 62
2021-09-10 10:39:01,727 INFO Thread-6 decorator.py:33|wrapper: request_<function TaskAPI.delete at 0x7f4d858ae790>, result: {'data': 'ok', 'success': True, 'message': 'Succeed'}
INFO:werkzeug:192.168.1.165 - - [10/Sep/2021 02:39:01] "DELETE /tasks/2 HTTP/1.1" 200 -
DEBUG:urllib3.connectionpool:Starting new HTTP connection (1): smgr:40002
DEBUG:urllib3.connectionpool:http://smgr:40002 "POST /task-mgr/tasks HTTP/1.1" 200 54
2021-09-10 10:44:45,796 INFO Thread-7 decorator.py:33|wrapper: request_<function TaskListAPI.post at 0x7f4d858ae430>, result: {'data': {'taskName': '任务s', 'taskDetail': [{'subName': 't-random', 'subTrigger': {'type': 'cron', 'value': '12-30/4 * * * * * *'}, 'subAction': {'func': 'random', 'kwargs': {'seed': 4}}}, {'subName': 't-tiktok', 'subTrigger': {'type': 'interval', 'value': '4 sec'}, 'subAction': {'func': 'tiktok', 'kwargs': {}}}], 'taskId': 3}, 'success': True, 'message': 'Succeed'}
INFO:werkzeug:192.168.1.165 - - [10/Sep/2021 02:44:45] "POST /tasks HTTP/1.1" 200 -
2021-09-10 10:44:54,942 INFO Thread-8 decorator.py:33|wrapper: request_<function TaskAPI.get at 0x7f4d858ae550>, result: {'data': {'taskName': '任务s', 'taskDetail': [{'subName': 't-random', 'subTrigger': {'type': 'cron', 'value': '12-30/4 * * * * * *'}, 'subAction': {'func': 'random', 'kwargs': {'seed': 4}}}, {'subName': 't-tiktok', 'subTrigger': {'type': 'interval', 'value': '4 sec'}, 'subAction': {'func': 'tiktok', 'kwargs': {}}}]}, 'success': True, 'message': 'Succeed'}
INFO:werkzeug:192.168.1.165 - - [10/Sep/2021 02:44:54] "GET /tasks/3 HTTP/1.1" 200 -
DEBUG:urllib3.connectionpool:Starting new HTTP connection (1): smgr:40002
DEBUG:urllib3.connectionpool:http://smgr:40002 "DELETE /task-mgr/tasks/3 HTTP/1.1" 200 62
2021-09-10 10:46:30,544 INFO Thread-9 decorator.py:33|wrapper: request_<function TaskAPI.delete at 0x7f4d858ae790>, result: {'data': 'ok', 'success': True, 'message': 'Succeed'}
INFO:werkzeug:192.168.1.165 - - [10/Sep/2021 02:46:30] "DELETE /tasks/3 HTTP/1.1" 200 -

```

也可以进入容器查看日志:

- 查看容器id

```shell
docker ps -a |grep scheduler

df3ad534d5dc   sbackend:0.1.0             "python3 main.py sba…"   17 minutes ago   Up 17 minutes               0.0.0.0:40001->40001/tcp, :::40001->40001/tcp               scheduler_sbackend_1
c1e21e08fe40   sworker:0.1.0              "python3 main.py swo…"   17 hours ago     Up 17 hours                 40001/tcp, 40003/tcp                                        scheduler_sworker1_1
e68d8693e2c1   sworker:0.1.0              "python3 main.py swo…"   17 hours ago     Up 17 hours                 40001/tcp, 40003/tcp                                        scheduler_sworker2_1
1e69f31baf00   smgr:0.1.0                 "python3 main.py smgr"   17 hours ago     Up 17 hours                 0.0.0.0:40002->40002/tcp, :::40002->40002/tcp               scheduler_smgr_1
781997fd4a5c   redis:alpine               "docker-entrypoint.s…"   17 hours ago     Up 17 hours                 0.0.0.0:46379->6379/tcp, :::46379->6379/tcp                 scheduler_sredis_1
e8f76523dfaf   postgres:12.5              "docker-entrypoint.s…"   17 hours ago     Up 17 hours                 0.0.0.0:45432->5432/tcp, :::45432->5432/tcp                 scheduler_spostgres_1

```

- 进入`smgr`容器查看

```shell
docker exec -it scheduler_smgr_1 sh

vim /var/log/smgr/smgr.log

...
2021-09-10 10:37:40,213 INFO Thread-5 manager.py:43|create_task: create_req: {'task_id': 'DemoTask_2', 'jobs_info': {'DemoTask_2:t-random': {'trigger_inf
2021-09-10 10:37:40,213 INFO Thread-5 decorator.py:33|wrapper: request_<function TaskListAPI.post at 0x7f0591df2b80>, result: {'data': 'ok', 'success': T
INFO:werkzeug:172.18.0.4 - - [10/Sep/2021 02:37:40] "POST /task-mgr/tasks HTTP/1.1" 200 -
DEBUG:urllib3.connectionpool:Starting new HTTP connection (1): sworker1:40003
DEBUG:urllib3.connectionpool:http://sworker1:40003 "DELETE /task-worker/tasks/DemoTask_2 HTTP/1.1" 200 62                                                
2021-09-10 10:39:01,715 INFO Thread-6 manager.py:64|delete_task: task_id: DemoTask_2 delete_res: {'data': 'DemoTask_2', 'success': True, 'message': 'Succ
2021-09-10 10:39:01,716 INFO Thread-6 decorator.py:33|wrapper: request_<function TaskAPI.delete at 0x7f0591df2dc0>, result: {'data': 'DemoTask_2', 'succe
INFO:werkzeug:172.18.0.4 - - [10/Sep/2021 02:39:01] "DELETE /task-mgr/tasks/2 HTTP/1.1" 200 -                                                            
DEBUG:urllib3.connectionpool:Starting new HTTP connection (1): sworker1:40003                                                                            
DEBUG:urllib3.connectionpool:http://sworker1:40003 "POST /task-worker/tasks HTTP/1.1" 200 54       
2021-09-10 10:44:45,794 INFO Thread-7 manager.py:43|create_task: create_req: {'task_id': 'DemoTask_3', 'jobs_info': {'DemoTask_3:t-random': {'trigger_inf
2021-09-10 10:44:45,794 INFO Thread-7 decorator.py:33|wrapper: request_<function TaskListAPI.post at 0x7f0591df2b80>, result: {'data': 'ok', 'success': T
INFO:werkzeug:172.18.0.4 - - [10/Sep/2021 02:44:45] "POST /task-mgr/tasks HTTP/1.1" 200 -
DEBUG:urllib3.connectionpool:Starting new HTTP connection (1): sworker1:40003
DEBUG:urllib3.connectionpool:http://sworker1:40003 "DELETE /task-worker/tasks/DemoTask_3 HTTP/1.1" 200 62                                                
2021-09-10 10:46:30,534 INFO Thread-8 manager.py:64|delete_task: task_id: DemoTask_3 delete_res: {'data': 'DemoTask_3', 'success': True, 'message': 'Succ
2021-09-10 10:46:30,535 INFO Thread-8 decorator.py:33|wrapper: request_<function TaskAPI.delete at 0x7f0591df2dc0>, result: {'data': 'DemoTask_3', 'succe
INFO:werkzeug:172.18.0.4 - - [10/Sep/2021 02:46:30] "DELETE /task-mgr/tasks/3 HTTP/1.1" 200 -  
```

- 进入`sworker1`/`sworker2`容器查看

```shell
docker exec -it scheduler_sworker1_1 sh

vim /var/log/sworker/sowrker.log

...
INFO:apscheduler.executors.default:Job "JobProcess.run (trigger: cron[year='*', month='*', day='*', day_of_week='*', hour='*', minute='*', second='12-30/
2021-09-10 10:46:20,004 INFO ThreadPoolExecutor-0_0 worker.py:53|my_listener: DemoTask_3:t-random run ok                                                 
INFO:apscheduler.executors.default:Running job "JobProcess.run (trigger: interval[0:00:04], next run at: 2021-09-10 10:46:25 CST)" (scheduled at 2021-09-
2021-09-10 10:46:21,794 INFO ThreadPoolExecutor-0_0 process.py:74|run_func: jid run tiktok at 2021-09-10 02:46:21.794801                                 
2021-09-10 10:46:21,795 INFO ThreadPoolExecutor-0_0 process.py:88|process_result: jid:DemoTask_3:t-tiktok, result: ok                                    
INFO:apscheduler.executors.default:Job "JobProcess.run (trigger: interval[0:00:04], next run at: 2021-09-10 10:46:25 CST)" executed successfully         
2021-09-10 10:46:21,795 INFO ThreadPoolExecutor-0_0 worker.py:53|my_listener: DemoTask_3:t-tiktok run ok                                                 
INFO:apscheduler.executors.default:Running job "JobProcess.run (trigger: cron[year='*', month='*', day='*', day_of_week='*', hour='*', minute='*', second
2021-09-10 10:46:24,004 INFO ThreadPoolExecutor-0_0 process.py:88|process_result: jid:DemoTask_3:t-random, result: 4                                     
INFO:apscheduler.executors.default:Job "JobProcess.run (trigger: cron[year='*', month='*', day='*', day_of_week='*', hour='*', minute='*', second='12-30/
2021-09-10 10:46:24,004 INFO ThreadPoolExecutor-0_0 worker.py:53|my_listener: DemoTask_3:t-random run ok                                                 
INFO:apscheduler.executors.default:Running job "JobProcess.run (trigger: interval[0:00:04], next run at: 2021-09-10 10:46:29 CST)" (scheduled at 2021-09-
2021-09-10 10:46:25,794 INFO ThreadPoolExecutor-0_0 process.py:74|run_func: jid run tiktok at 2021-09-10 02:46:25.794735                                 
2021-09-10 10:46:25,795 INFO ThreadPoolExecutor-0_0 process.py:88|process_result: jid:DemoTask_3:t-tiktok, result: ok                                    
INFO:apscheduler.executors.default:Job "JobProcess.run (trigger: interval[0:00:04], next run at: 2021-09-10 10:46:29 CST)" executed successfully         
2021-09-10 10:46:25,795 INFO ThreadPoolExecutor-0_0 worker.py:53|my_listener: DemoTask_3:t-tiktok run ok                                                 
INFO:apscheduler.executors.default:Running job "JobProcess.run (trigger: cron[year='*', month='*', day='*', day_of_week='*', hour='*', minute='*', second
2021-09-10 10:46:28,004 INFO ThreadPoolExecutor-0_0 process.py:88|process_result: jid:DemoTask_3:t-random, result: 3                                     
INFO:apscheduler.executors.default:Job "JobProcess.run (trigger: cron[year='*', month='*', day='*', day_of_week='*', hour='*', minute='*', second='12-30/
2021-09-10 10:46:28,005 INFO ThreadPoolExecutor-0_0 worker.py:53|my_listener: DemoTask_3:t-random run ok                                                 
INFO:apscheduler.executors.default:Running job "JobProcess.run (trigger: interval[0:00:04], next run at: 2021-09-10 10:46:33 CST)" (scheduled at 2021-09-
2021-09-10 10:46:29,794 INFO ThreadPoolExecutor-0_0 process.py:74|run_func: jid run tiktok at 2021-09-10 02:46:29.794914                                 
2021-09-10 10:46:29,795 INFO ThreadPoolExecutor-0_0 process.py:88|process_result: jid:DemoTask_3:t-tiktok, result: ok                                    
INFO:apscheduler.executors.default:Job "JobProcess.run (trigger: interval[0:00:04], next run at: 2021-09-10 10:46:33 CST)" executed successfully         
2021-09-10 10:46:29,795 INFO ThreadPoolExecutor-0_0 worker.py:53|my_listener: DemoTask_3:t-tiktok run ok                                                 
2021-09-10 10:46:30,531 INFO Thread-6 base.py:632|remove_job: Removed job DemoTask_3:t-random                                                            
2021-09-10 10:46:30,532 INFO Thread-6 worker.py:111|remove_job: jid: DemoTask_3:t-random removed                                                         
2021-09-10 10:46:30,532 INFO Thread-6 base.py:632|remove_job: Removed job DemoTask_3:t-tiktok                                                            
2021-09-10 10:46:30,532 INFO Thread-6 worker.py:111|remove_job: jid: DemoTask_3:t-tiktok removed                                                         
2021-09-10 10:46:30,532 INFO Thread-6 worker.py:106|remove_task: task_id: DemoTask_3 removed jids: ['DemoTask_3:t-random', 'DemoTask_3:t-tiktok']        
2021-09-10 10:46:30,532 INFO Thread-6 decorator.py:33|wrapper: request_<function TaskAPI.delete at 0x7f31edf43ee0>, result: {'data': 'DemoTask_3', 'succe
INFO:werkzeug:172.18.0.5 - - [10/Sep/2021 02:46:30] "DELETE /task-worker/tasks/DemoTask_3 HTTP/1.1" 200 - 
```

## 更多

有修改代码，重新build生成镜像，重启容器

### 重新生成镜像

```shell
# 都有修改，构建所有镜像
docker-compose -f docker-compose.yml build 
# 只修改了sbackend
docker-compose -f docker-compose.yml build sbackend

```

### 重启容器

- 只修改了sbackend

```shell 
docker-compose -f docker-compose.yml up -d
```

- 修改了smgr、sworker

因为mgr和worker启动有依赖顺序

```shell
# 停止
docker-compose -f docker-compose.yml down
# 重新拉起
docker-compose -f docker-compose.yml up -d
```

### 自定义任务

- 设计相应restful接口 【`sbackend`】
- 定义相应接口传参 【`sbackend`】
- 编写对应的任务解析器`parser` 【`smgr`】
- 编写对应的任务运行处理模块`process` 【`sworker`】