FROM python:3.12.5-slim

# added explicitly for GDAL
RUN echo "deb http://deb.debian.org/debian bookworm main" >> /etc/apt/sources.list

RUN apt update && apt install -y vim postgresql-client gdal-bin

COPY ./docker/migration/requirements.txt /tmp

RUN pip install -r /tmp/requirements.txt

COPY ./src/common/taxi-db /tmp/taxi-db

RUN pip install -e /tmp/taxi-db

RUN mkdir /app

ARG USER=alembic

RUN useradd ${USER}

USER ${USER}

WORKDIR /app

COPY ./docker/migration/upgrade ./docker/migration/downgrade /usr/bin/

COPY ./alembic/data/road.gpkg /tmp/
