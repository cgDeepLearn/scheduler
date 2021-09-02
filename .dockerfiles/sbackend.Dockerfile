FROM python-base:latest

COPY ./src/sbackend /use/app/sbackend

WORKDIR /usr/app/sbackend

ENV TZ=Asia/Shanghai

ENV BACKEND_PORT=30001

EXPOSE $BACKEND_PORT

CMD ["python3", "main.py", "sbackend"]
