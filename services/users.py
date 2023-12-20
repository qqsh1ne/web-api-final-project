from typing import List

from models import User
from schemas.users import UserSchemaCreate, UserSchemaUpdate
from utils.unitofwork import UnitOfWork


class UsersService:
    async def create_user(self, uow: UnitOfWork, user_schema: UserSchemaCreate) -> User:
        async with uow:
            user = await uow.users.create(user_schema)
            await uow.commit()
            return user

    async def get_user(self, uow: UnitOfWork, user_id: int) -> User:
        async with uow:
            user = await uow.users.get(user_id)
            return user

    async def get_user_by_name(self, uow: UnitOfWork, user_name: str) -> User:
        async with uow:
            user = await uow.users.get_by_name(user_name)
            return user

    async def get_users(self, uow: UnitOfWork, offset: int = 0, limit: int | None = None) -> List[User]:
        async with uow:
            users = await uow.users.get_all(offset=offset, limit=limit)
            return users

    async def edit_user(self, uow: UnitOfWork, user_id: int, user_schema: UserSchemaUpdate) -> User:
        async with uow:
            user = await uow.users.edit(user_id, user_schema)
            await uow.commit()
            return user

    async def delete_user(self, uow: UnitOfWork, user_id: int):
        async with uow:
            await uow.users.delete(user_id)
            await uow.commit()
