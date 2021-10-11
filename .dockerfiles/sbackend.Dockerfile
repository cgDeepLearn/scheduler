FROM python-base:latest

COPY ./src/sbackend /usr/app/sbackend

WORKDIR /usr/app/sbackend

ENV TZ=Asia/Shanghai

ENV BACKEND_PORT=30001

EXPOSE $BACKEND_PORT

COPY ./scripts/sbackend-start.sh /usr/app/sbackend
RUN sed -i 's/\r//' sbackend-start.sh
RUN chmod +x sbackend-start.sh

CMD ["/bin/sh", "sbackend-start.sh"]
