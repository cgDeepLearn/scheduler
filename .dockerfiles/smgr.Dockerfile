FROM python-base:latest

COPY ./src/smgr /usr/app/smgr

WORKDIR /usr/app/smgr

ENV TZ=Asia/Shanghai

ENV MGR_PORT=40002

EXPOSE $MGR_PORT

COPY ./scripts/smgr-start.sh /usr/app/smgr
RUN sed -i 's/\r//' smgr-start.sh
RUN chmod +x smgr-start.sh

CMD ["/bin/sh", "smgr-start.sh"]