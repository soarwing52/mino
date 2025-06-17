# app/api/v1/task.py
from fastapi import APIRouter, File, Form, UploadFile, Depends, HTTPException
from sqlalchemy.orm import Session

from app.schemas.task import TaskCreate, TaskRead
from app.services.task_service import create_task, get_task, list_tasks, delete_task
from app.core.db import get_db


router = APIRouter()


@router.post("/", response_model=TaskRead)
async def create_new_task(
    db: Session = Depends(get_db),
    title: str = Form(...),
    description: str = Form(...),
    file: UploadFile = File(...),
):
    item = TaskCreate(title=title, description=description)
    return create_task(db, item, file)


@router.get("/", response_model=list[TaskRead])
def get_all_tasks(db: Session = Depends(get_db)):
    return list_tasks(db)


@router.get("/{task_id}", response_model=TaskRead)
def get_task_by_id(task_id: int, db: Session = Depends(get_db)):
    task = get_task(db, task_id)
    if not task:
        raise HTTPException(404, "Not found")
    return task


@router.delete("/{task_id}")
def delete_task_by_id(task_id: int, db: Session = Depends(get_db)):
    if delete_task(db, task_id):
        return {"msg": "Deleted"}
    raise HTTPException(404, "Not found")
