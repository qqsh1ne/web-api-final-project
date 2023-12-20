from datetime import datetime
from typing import List

from sqlalchemy import ForeignKey, DateTime, func, String, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from db import Base


class Forum(Base):
    __tablename__ = 'forums'

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String, index=True, unique=True)

    author_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"))
    author: Mapped["User"] = relationship(back_populates="forums", lazy="selectin")

    threads: Mapped[List["Thread"]] = relationship(back_populates="forum", lazy="selectin")

    created_at = mapped_column(DateTime(timezone=True), default=datetime.now, server_default=func.now())
    updated_at = mapped_column(DateTime(timezone=True), default=datetime.now, onupdate=func.now())
