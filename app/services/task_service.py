# app/services/task_service.py
from sqlalchemy.orm import Session
from app.models.task import Task
from app.schemas import TaskSchema
from app.core import minio
import uuid
import tempfile


def generate_presigned_url(filename: str):
    object_key = f"tasks/{uuid.uuid4()}_{filename}"
    url = minio.generate_presigned_url(
        bucket_name=minio.BucketName.BACKUP,
        object_name=object_key,
        method="PUT",
    )
    response = TaskSchema.TaskPresignedUrl(presigned_url=url, object_key=object_key)
    return response


def create_task(db: Session, task_create: TaskSchema.TaskCreate) -> Task:
    # 直接使用 presigned url 上傳後的 key
    db_task = Task(
        title=task_create.title,
        description=task_create.description,
        file_key=task_create.file_key,
    )
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task


def get_task(db: Session, task_id: int) -> Task | None:
    return db.query(Task).filter(Task.id == task_id).first()


def list_tasks(db: Session) -> list[Task]:
    return db.query(Task).all()


def delete_task(db: Session, task_id: int) -> bool:
    task = db.query(Task).filter(Task.id == task_id).first()
    if task:
        db.delete(task)
        db.commit()
        return True
    return False
