FROM python-base:latest

COPY ./src/sworker /usr/app/sworker

WORKDIR /usr/app/sworker

ENV TZ=Asia/Shanghai

ENV WORKER_PORT=30001

ENV WORKER_INDEX=1

EXPOSE $WORKER_PORT

CMD ["python3", "main.py", "sworker", "$WORKER_INDEX"]