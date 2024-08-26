#!/bin/bash

mlflow server \
       --backend-store-uri postgresql://${DB_USER}:${DB_PASSWORD}@${DB_HOST}:${DB_PORT}/${DB_NAME}?options=-c%20search_path%3D${MLFLOW_SCHEMA} \
       --default-artifact-root s3://${S3_BUCKET_NAME} \
       --host 0.0.0.0 \
       --port ${MLFLOW_PORT}
