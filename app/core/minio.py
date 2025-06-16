# app/core/minio.py
from minio import Minio

minio_client = Minio(endpoint="your-minio-ip:9000", access_key="your-access_key", secret_key="your_secret_key", secure=False)

MINIO_BUCKET = "your-bucket-name"

# 檢查桶是不是存在
if not minio_client.bucket_exists(MINIO_BUCKET):
    minio_client.make_bucket(MINIO_BUCKET)
