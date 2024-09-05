FROM apache/airflow:2.10.0

USER root

RUN apt update && apt install -y vim

USER airflow

COPY ./requirements.txt /tmp

RUN pip install -r /tmp/requirements.txt
