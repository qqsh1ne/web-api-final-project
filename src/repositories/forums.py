from sqlalchemy import select

from models import Forum, Thread, Message
from utils.repository import SQLAlchemyRepository


class ForumsRepository(SQLAlchemyRepository):
    model = Forum


class ThreadsRepository(SQLAlchemyRepository):
    model = Thread

    async def get_all_by_forum(self, forum_id: int, offset: int = 0, limit: int | None = None):
        stmt = select(self.model).offset(offset=offset).filter_by(forum_id=forum_id)

        if limit:
            stmt = stmt.limit(limit=limit)

        result = await self.session.execute(stmt)
        items = result.scalars().all()
        return items


class MessagesRepository(SQLAlchemyRepository):
    model = Message

    async def get_all_by_thread(self, thread_id: int, offset: int = 0, limit: int | None = None):
        stmt = select(self.model).offset(offset=offset).filter_by(thread_id=thread_id)

        if limit:
            stmt = stmt.limit(limit=limit)

        result = await self.session.execute(stmt)
        items = result.scalars().all()
        return items
