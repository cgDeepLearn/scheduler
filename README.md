# scheduler

A interface integrate with manager and worker  running in backend docker

集成APScheduler 的任务调度框架，运行于docker环境, 支持worker扩展

## 环境准备

- [x] `docker` version: 20.10.5
- [x] `docker-compose` version 1.29.2
- [x] `python` version: 3.8.5
    - [x] DBUtils==1.3.0
    - [x] psycopg2==2.8.6
    - [x] Flask==1.1.2
    - [x] Flask-RESTful==0.3.8
    - [x] APScheduler==3.7.0
    - [x] redis==3.5.3
    - [x] requests==2.25.1
    