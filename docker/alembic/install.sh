#!/bin/bash

alembic upgrade head

export PGPASSWORD=${DB_PASSWORD}
psql -U ${DB_USER} -h ${DB_HOST} -p ${DB_PORT} -d ${DB_NAME} -v schema=data -f $(pwd)/sql/install.sql