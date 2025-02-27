FROM python:3.12.5-slim

RUN apt update && apt install -y vim postgresql-client

COPY ./docker/migration/requirements.txt /tmp

RUN pip install -r /tmp/requirements.txt

COPY ./src/common/taxi-db /tmp/taxi-db

RUN pip install -e /tmp/taxi-db

RUN mkdir /app

ARG USER=alembic

RUN useradd ${USER}

USER ${USER}

WORKDIR /app

COPY ./docker/migration/upgrade /usr/bin

COPY ./docker/migration/downgrade /usr/bin
