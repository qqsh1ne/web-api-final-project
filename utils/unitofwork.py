from db import async_session_maker
from repositories.forums import ForumsRepository, ThreadsRepository, MessagesRepository
from repositories.users import UsersRepository


class UnitOfWork:
    def __init__(self):
        self.session_factory = async_session_maker

    async def __aenter__(self):
        self.session = self.session_factory()

        self.users = UsersRepository(self.session)
        self.forums = ForumsRepository(self.session)
        self.threads = ThreadsRepository(self.session)
        self.messages = MessagesRepository(self.session)

    async def __aexit__(self, *args):
        # await self.rollback()
        await self.session.close()

    async def commit(self):
        await self.session.commit()

    async def rollback(self):
        await self.session.rollback()