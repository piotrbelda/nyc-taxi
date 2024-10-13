FROM python:3.12.5-slim

RUN apt update && apt install -y vim

COPY ./docker/alembic/requirements.txt /tmp

RUN pip install -r /tmp/requirements.txt

COPY ./src/common/taxi-db /tmp/taxi-db

RUN pip install -e /tmp/taxi-db

RUN mkdir /app

WORKDIR /app
