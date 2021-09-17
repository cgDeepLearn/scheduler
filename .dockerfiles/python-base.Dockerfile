FROM python:3.8.5-alpine

RUN sed -i 's/dl-cdn.alpinelinux.org/mirrors.ustc.edu.cn/g' /etc/apk/repositories
RUN set -x \
    && apk update \
    && apk add --no-cache gcc \
    && apk add --no-cache g++ \
    && apk add --no-cache make \
    && apk add --no-cache libffi-dev \
    && apk add --no-cache openssl-dev \
    && apk add --no-cache postgresql-dev

COPY . /usr/local/python-base

WORKDIR /usr/local/python-base

RUN pip3 install -r requirements.txt -i https://pypi.douban.com/simple

ENV TZ Asia/Shanghai

RUN apk add tzdata && cp /usr/share/zoneinfo/${TZ} /etc/localtime \
    && echo ${TZ} > /etc/timezone \
    && apk del tzdata \
    && mkdir -p /usr/share/zoneinfo/Asia/ \
    && ln -s /etc/localtime /usr/share/zoneinfo/Asia/Shanghai

# 安装完成后清理缓存
RUN apk del gcc g++ make libffi-dev openssl-dev && \
    rm -rf /var/cache/apk/*