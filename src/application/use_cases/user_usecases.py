from fastapi import HTTPException

from src.application.use_cases.base import UseCase
from src.domain.entities import User
from src.domain.value_objects import UserData
from src.infrastructure.logger.interfaces import ILogger
from src.infrastructure.models import UserModel
from src.infrastructure.uow.interfaces import IUnitOfWork
from src.presentation.routers.schemas import UserSchema


class DeleteUser(UseCase[str, None]):

    def __init__(self, uow: IUnitOfWork, logger: ILogger):
        self.uow = uow
        self.logger = logger

    async def __call__(self, email: str):
        try:
            async with self.uow:
                user = await self.uow.users.find_one(UserModel.email, email)
                if user:
                    await self.uow.users.delete_by_email(email)
                    domain_user: User = user.to_domain()
                    domain_user.delete_files()
                    await self.uow.commit()
                    self.logger.info(f'Удалён пользователь {user.id} {user.email}')
        except HTTPException as ex:
            raise ex
        except Exception as ex:
            self.logger.error(f'Ошибка при удалении пользователя {email}')
            raise ex


class UpdateUser(UseCase[UserData, UserSchema]):

    def __init__(self, uow: IUnitOfWork, logger: ILogger):
        self.uow = uow
        self.logger = logger

    async def __call__(self, user: User, new_user_data: UserData) -> UserSchema:
        try:
            async with self.uow:
                user = await self.uow.users.find_one(UserModel.id, user.id)
                user.email = new_user_data.email
                await self.uow.commit()
                self.logger.info(f'Обновлён пользователь {user.id} {user.email}')
                return UserSchema(email=user.email)
        except HTTPException as ex:
            raise ex
        except Exception as ex:
            self.logger.error(f'Ошибка при обновлении пользователя {user.email} '
                              f'Данные: {new_user_data}')
            raise ex
