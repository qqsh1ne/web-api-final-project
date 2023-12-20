from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict

from schemas.forums.thread import ThreadSchema


class ForumSchemaBase(BaseModel):
    title: str
    author_id: int


class ForumSchemaCreate(ForumSchemaBase):
    pass


class ForumSchemaUpdate(ForumSchemaBase):
    title: Optional[str] = None
    author_id: Optional[int] = None


class ForumSchema(ForumSchemaBase):
    model_config = ConfigDict(from_attributes=True)
    # threads: Optional[ThreadSchema] = None

    id: int
    created_at: datetime
    updated_at: datetime
