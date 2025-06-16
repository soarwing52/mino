# app/schemas/task.py
from pydantic import BaseModel, ConfigDict


class TaskBase(BaseModel):
    title: str
    description: str


class TaskCreate(TaskBase):
    pass


class TaskRead(TaskBase):
    id: int

    model_config = ConfigDict(from_attributes=True)
