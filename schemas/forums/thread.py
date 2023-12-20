from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict


class ThreadSchemaBase(BaseModel):
    title: str
    author_id: int
    forum_id: int


class ThreadSchemaCreate(ThreadSchemaBase):
    pass


class ThreadSchemaUpdate(ThreadSchemaBase):
    title: Optional[str] = None
    author_id: Optional[int] = None
    forum_id: Optional[int] = None


class ThreadSchema(ThreadSchemaBase):
    model_config = ConfigDict(from_attributes=True)


    id: int
    created_at: datetime
    updated_at: datetime
