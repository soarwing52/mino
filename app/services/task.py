# app/services/task_service.py
from sqlalchemy.orm import Session
from app.models.task import Task
from app.schemas.task import TaskCreate
from app.core.minio import minio_client, MINIO_BUCKET
import uuid


def create_task(db: Session, task_create: TaskCreate, file, object_key=None) -> Task:
    # 1. 產生 object_key
    object_key = f"tasks/{uuid.uuid4()}_{file.filename}"

    # 2. 上傳到 MinIO
    minio_client.put_object(MINIO_BUCKET, object_key, file.file, length=-1, content_type=file.content_type)

    # 3. 儲存到資料庫
    db_task = Task(title=task_create.title, description=task_create.description, file_key=object_key)
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
