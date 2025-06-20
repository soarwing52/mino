from fastapi import APIRouter, File, Form, UploadFile, Depends, HTTPException
from sqlalchemy.orm import Session

from app.schemas import TaskSchema
from app.services.task_service import create_task, get_task, list_tasks, delete_task
from app.services import task_service
from app.core.db import get_db


task_router = APIRouter()


@task_router.post("/upload-url", response_model=TaskSchema.TaskPresignedUrl, tags=["tasks"])
async def generate_presigned_url(payload: TaskSchema.FilenameRequest):
    return task_service.generate_presigned_url(payload.filename)


@task_router.post("/", response_model=TaskSchema.TaskRead, tags=["tasks"])
async def create_new_task(
    item: TaskSchema.TaskCreate,
    db: Session = Depends(get_db),
):
    return create_task(db, item)


@task_router.get("/", response_model=list[TaskSchema.TaskRead], tags=["tasks"])
async def get_all_tasks(db: Session = Depends(get_db)):
    return list_tasks(db)


@task_router.get("/{task_id}", response_model=TaskSchema.TaskRead)
async def get_task_by_id(task_id: int, db: Session = Depends(get_db)):
    task = get_task(db, task_id)
    if not task:
        raise HTTPException(404, "Not found")
    return task


@task_router.delete("/{task_id}")
async def delete_task_by_id(task_id: int, db: Session = Depends(get_db)):
    if delete_task(db, task_id):
        return {"msg": "Deleted"}
    raise HTTPException(404, "Not found")
