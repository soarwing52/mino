# app/services/task_service.py
from sqlalchemy.orm import Session
from app.models.task import Task
from app.schemas.task import TaskCreate


def create_task(db: Session, task_create: TaskCreate) -> Task:
    db_task = Task(title=task_create.title, description=task_create.description)
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
