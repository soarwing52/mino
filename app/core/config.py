# app/core/config.py
import boto3

from dotenv import load_dotenv

load_dotenv()


MINIO_CONFIG = {
    "aws_access_key_id": "<your_key>",
    "aws_secret_access_key": "<your_secret_key>",
    "region_name": "us-east-1",
    "endpoint_url": "http://yourminio.example.com:9000",
    "bucket_name": "your-bucket-name",
}


def get_s3_client():
    return boto3.client("s3", **MINIO_CONFIG)
