# models/task.py
from sqlalchemy import Column, Integer, String, Text
from app.core.db import Base


class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=False)
    file_key = Column(String(255), nullable=False)  # MinIO object key
