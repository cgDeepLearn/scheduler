FROM python-base:latest

COPY ./src/sworker /usr/app/sworker

WORKDIR /usr/app/sworker

ENV TZ=Asia/Shanghai

ENV WORKER_PORT=40001

EXPOSE $WORKER_PORT

COPY ./scripts/sworker-start.sh /usr/app/sworker
RUN sed -i 's/\r//' sworker-start.sh
RUN chmod +x sworker-start.sh

CMD ["/bin/sh", "sworker-start.sh"]