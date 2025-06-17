from minio import Minio
from minio.error import S3Error

client = Minio("localhost:9000", access_key="minioadmin", secret_key="minioadmin", secure=False)

bucket_name = "my-bucket"
if not client.bucket_exists(bucket_name):
    client.make_bucket(bucket_name)

file_path = "test.txt"
object_name = "test.txt"

try:
    x = client.fput_object(bucket_name, object_name, file_path)
    print(x.location)
    print("上傳成功")
except S3Error as e:
    print("上傳失敗:", e)
