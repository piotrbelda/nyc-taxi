-- taxi db
CREATE DATABASE taxi;
\c taxi
CREATE SCHEMA mlflow;

-- airflow db
CREATE DATABASE airflow;
\c airflow
CREATE USER airflow WITH PASSWORD 'airflow' SUPERUSER;
CREATE SCHEMA airflow;
