FROM python:3.8.3-alpine

WORKDIR /usr/src/app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apk add --update --no-cache mariadb-connector-c-dev \
	&& apk add --no-cache --virtual .build-deps \
		mariadb-dev \
		gcc \
		musl-dev \
	&& pip install mysqlclient==1.4.6 \
	&& apk del .build-deps

COPY app/requirements.txt .

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

ADD ./app .

RUN mkdir staticfiles
