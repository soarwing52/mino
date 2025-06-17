# app/core/minio.py
from minio import Minio
from enum import Enum


class BucketName(str, Enum):
    USER_AVATAR = "user-avatar"
    PRODUCT_IMAGES = "product-images"
    BACKUP = "backup"


def create_minio_client():
    """
    應用啟動後只會初始化一次 MinIO 客戶端
    """
    return Minio(
        "localhost:9000",
        access_key="minioadmin",
        secret_key="minioadmin",
        secure=False,
    )


minio_client = Minio(
    "localhost:9000",
    access_key="minioadmin",
    secret_key="minioadmin",
    secure=False,
)


def get_minio():
    return minio_client


def create_bucket(bucket_name: BucketName):
    """
    創建一個新的 MinIO 桶
    """
    try:
        if not minio_client.bucket_exists(bucket_name.value):
            minio_client.make_bucket(bucket_name.value)
            print(f"桶 {bucket_name.value} 創建成功")
        else:
            print(f"桶 {bucket_name.value} 已存在")
    except Exception as e:
        print(f"創建桶失敗: {e}")


def upload_file(bucket_name: BucketName, file_path: str, object_name: str) -> bool:
    """
    上傳文件到 MinIO 桶
    """
    try:
        if not minio_client.bucket_exists(bucket_name.value):
            raise ValueError(f"桶 {bucket_name.value} 不存在")

        minio_client.fput_object(bucket_name.value, object_name, file_path)
        print(f"文件 {file_path} 成功上傳到 {bucket_name.value}/{object_name}")
        return True
    except Exception as e:
        print(f"上傳失敗: {e}")
        return False
