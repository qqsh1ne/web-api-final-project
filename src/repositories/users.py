from sqlalchemy import select

from models.users import User
from utils.repository import SQLAlchemyRepository


class UsersRepository(SQLAlchemyRepository):
    model = User

    async def get_by_name(self, obj_name):
        stmt = select(self.model).filter_by(name=obj_name)
        result = await self.session.execute(stmt)
        return result.scalar_one()
