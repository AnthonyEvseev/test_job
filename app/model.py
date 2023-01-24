from uuid import UUID, uuid4

from pydantic import BaseModel, Field


class Task(BaseModel):
    task_uid: UUID = Field(default_factory=uuid4)
    a: int
    b: int
