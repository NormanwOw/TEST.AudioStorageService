from sqlalchemy import delete
from sqlalchemy.ext.asyncio import AsyncSession

from src.infrastructure.models import UserModel
from src.infrastructure.repositories.base import SQLAlchemyRepository
from src.infrastructure.repositories.interfaces import IUsersRepository


class UsersRepository(SQLAlchemyRepository, IUsersRepository):

    def __init__(self, session: AsyncSession):
        self.__session = session
        super().__init__(session, UserModel)

    async def delete_by_email(self, email: str):
        await self.__session.execute(
            delete(UserModel).where(UserModel.email == email)
        )
