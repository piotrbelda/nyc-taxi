FROM python:3.12.5-slim

RUN apt update && apt install -y vim

COPY ./docker/backend/requirements.txt /tmp

RUN pip install -r /tmp/requirements.txt

COPY ./src /

WORKDIR /src/app
