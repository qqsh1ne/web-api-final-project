from datetime import datetime

from sqlalchemy import ForeignKey, DateTime, func, String, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from db import Base


class Message(Base):
    __tablename__ = 'messages'

    id: Mapped[int] = mapped_column(primary_key=True)
    content: Mapped[str] = mapped_column(String)

    author_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"))
    author: Mapped["User"] = relationship(back_populates="messages", lazy="selectin")

    thread_id: Mapped[int] = mapped_column(Integer, ForeignKey("threads.id"))
    thread: Mapped["Thread"] = relationship(back_populates="messages", lazy="selectin")

    created_at = mapped_column(DateTime(timezone=True), default=datetime.now, server_default=func.now())
    updated_at = mapped_column(DateTime(timezone=True), default=datetime.now, onupdate=func.now())
