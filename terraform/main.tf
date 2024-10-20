terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 4.16"
    }
  }

  required_version = ">= 1.2.0"
}

provider "aws" {
  region = "eu-central-1"
}

resource "aws_s3_bucket" "mlflow_taxi_bucket" {
  bucket = "mlflow-taxi"

  tags = {
    Name        = "MLflow Taxi bucket"
    Environment = "Dev"
  }
}

resource "aws_s3_bucket_public_access_block" "test_bucket_access_block" {
  bucket = aws_s3_bucket.mlflow_taxi_bucket.id

  block_public_acls       = false
  block_public_policy     = false
  restrict_public_buckets = false
  ignore_public_acls      = false
}
