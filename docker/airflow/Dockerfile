FROM apache/airflow:3.1.5

USER root

RUN apt update && apt install -y vim

USER airflow

COPY ./docker/airflow/requirements.txt /tmp

RUN pip install -r /tmp/requirements.txt

COPY ./src/common/taxi-db /tmp/taxi-db

RUN pip install -e /tmp/taxi-db

RUN pip show taxi-db
