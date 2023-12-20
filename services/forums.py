from typing import List, Optional

from models import Forum, Thread, Message

from schemas.forums.forum import ForumSchemaCreate, ForumSchemaUpdate
from schemas.forums.thread import ThreadSchemaCreate, ThreadSchemaUpdate
from schemas.forums.message import MessageSchemaCreate, MessageSchemaUpdate
from utils.unitofwork import UnitOfWork


class ForumsService:
    # Forum
    async def create_forum(self, uow: UnitOfWork, forum_schema: ForumSchemaCreate) -> Forum:
        async with uow:
            forum = await uow.forums.create(forum_schema)
            await uow.commit()
            return forum

    async def get_forums(self, uow: UnitOfWork, offset: int = 0, limit: Optional[int] = None) -> List[Forum]:
        async with uow:
            forums = await uow.forums.get_all(offset=offset, limit=limit)
            return forums

    async def get_forum(self, uow: UnitOfWork, forum_id: int) -> Forum:
        async with uow:
            forum = await uow.forums.get(forum_id)
            return forum

    async def edit_forum(self, uow: UnitOfWork, forum_id: int, forum_schema: ForumSchemaUpdate) -> Forum:
        async with uow:
            forum = await uow.forums.edit(forum_id, forum_schema)
            await uow.commit()
            return forum

    async def delete_forum(self, uow: UnitOfWork, forum_id: int):
        async with uow:
            await uow.forums.delete(forum_id)
            await uow.commit()

    # Thread
    async def create_thread(self, uow: UnitOfWork, thread_schema: ThreadSchemaCreate) -> Thread:
        async with uow:
            thread = await uow.threads.create(thread_schema)
            await uow.commit()
            return thread

    async def get_threads(self, uow: UnitOfWork, offset: int = 0, limit: Optional[int] = None) -> List[Thread]:
        async with uow:
            threads = await uow.threads.get_all(offset=offset, limit=limit)
            return threads

    async def get_forum_threads(self, uow: UnitOfWork, forum_id: int, offset: int = 0, limit: Optional[int] = None) -> List[Message]:
        async with uow:
            threads = await uow.threads.get_all_by_forum(forum_id=forum_id, offset=offset, limit=limit)
            return threads

    async def get_thread(self, uow: UnitOfWork, thread_id: int) -> Thread:
        async with uow:
            thread = await uow.threads.get(thread_id)
            return thread

    async def edit_thread(self, uow: UnitOfWork, thread_id: int, thread_schema: ThreadSchemaUpdate) -> Thread:
        async with uow:
            thread = await uow.threads.edit(thread_id, thread_schema)
            await uow.commit()
            return thread

    async def delete_thread(self, uow: UnitOfWork, thread_id: int):
        async with uow:
            await uow.threads.delete(thread_id)
            await uow.commit()

    # Message
    async def create_message(self, uow: UnitOfWork, message_schema: MessageSchemaCreate) -> Message:
        async with uow:
            message = await uow.messages.create(message_schema)
            await uow.commit()
            return message

    async def get_messages(self, uow: UnitOfWork, offset: int = 0, limit: Optional[int] = None) -> List[Message]:
        async with uow:
            messages = await uow.messages.get_all(offset=offset, limit=limit)
            return messages

    async def get_thread_messages(self, uow: UnitOfWork, thread_id: int, offset: int = 0, limit: Optional[int] = None) -> List[Message]:
        async with uow:
            messages = await uow.messages.get_all_by_thread(thread_id=thread_id, offset=offset, limit=limit)
            return messages

    async def get_message(self, uow: UnitOfWork, message_id: int) -> Message:
        async with uow:
            message = await uow.messages.get(message_id)
            return message

    async def edit_message(self, uow: UnitOfWork, message_id: int, message_schema: MessageSchemaUpdate) -> Message:
        async with uow:
            message = await uow.messages.edit(message_id, message_schema)
            await uow.commit()
            return message

    async def delete_message(self, uow: UnitOfWork, message_id: int):
        async with uow:
            await uow.messages.delete(message_id)
            await uow.commit()