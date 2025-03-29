from src.application.use_cases.base import UseCase
from src.domain.entities import User
from src.infrastructure.models import UserModel
from src.infrastructure.uow.interfaces import IUnitOfWork


class DeleteUser(UseCase[str, None]):

    def __init__(self, uow: IUnitOfWork):
        self.uow = uow

    async def __call__(self, email: str):
        async with self.uow:
            user = await self.uow.users.find_one(UserModel.email, email)
            if user:
                await self.uow.users.delete_by_email(email)
                domain_user: User = user.to_domain()
                domain_user.delete_files()
                await self.uow.commit()
