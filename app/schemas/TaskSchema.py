from pydantic import BaseModel, ConfigDict


class TaskBase(BaseModel):
    title: str
    description: str
    file_key: str | None = None


class FilenameRequest(BaseModel):
    filename: str


class TaskPresignedUrl(BaseModel):
    presigned_url: str
    object_key: str


class TaskCreate(TaskBase):
    pass


class TaskRead(TaskBase):
    id: int

    model_config = ConfigDict(from_attributes=True)
