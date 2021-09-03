FROM python-base:latest

COPY ./src/smgr /usr/app/smgr

WORKDIR /usr/app/smgr

ENV TZ=Asia/Shanghai

ENV MGR_PORT=30002

EXPOSE $MGR_PORT

CMD ["python3", "main.py", "smgr"]