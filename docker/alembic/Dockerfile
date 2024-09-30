FROM python:3.12.5-slim

RUN apt update && apt install -y vim

COPY ./requirements.txt /tmp

RUN pip install -r /tmp/requirements.txt

RUN mkdir /app

WORKDIR /app
