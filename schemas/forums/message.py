from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict


class MessageSchemaBase(BaseModel):
    content: str
    author_id: int
    thread_id: int


class MessageSchemaCreate(MessageSchemaBase):
    pass


class MessageSchemaUpdate(MessageSchemaBase):
    content: Optional[str] = None
    author_id: Optional[int] = None
    thread_id: Optional[int] = None


class MessageSchema(MessageSchemaBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: datetime
    updated_at: datetime
