from datetime import timedelta

from fastapi.security import HTTPAuthorizationCredentials
from fastapi.exceptions import HTTPException

from config import Settings
from src.application.use_cases.base import UseCase
from src.domain.entities import User
from src.domain.interfaces import IAuthService
from src.domain.value_objects import UserData
from src.infrastructure.external.base_client import Client
from src.infrastructure.logger.interfaces import ILogger
from src.infrastructure.models import UserModel
from src.infrastructure.uow.interfaces import IUnitOfWork
from src.presentation.routers.schemas import TokenData, UserSchema


class YandexAuth(UseCase[str, TokenData]):

    def __init__(
        self,
        uow: IUnitOfWork,
        yandex_client: Client,
        auth_service: IAuthService,
        settings: Settings,
        logger: ILogger,
    ):
        self.uow = uow
        self.yandex_client = yandex_client
        self.auth_service = auth_service
        self.settings = settings
        self.logger = logger

    async def __call__(self, code: str) -> TokenData:
        try:
            async with self.uow:
                user_data = await self.yandex_client.get_user_data(code)
                user = UserModel(email=user_data.email)
                await self.uow.users.add(user)
                token = self.auth_service.create_access_token(
                    user_data=user_data,
                    expires_delta=timedelta(minutes=self.settings.ACCESS_TOKEN_EXPIRE_MINUTES)
                )
                await self.uow.commit()
                self.logger.info(f'Пользователь {user.email} прошёл аутентификацию')
                return token
        except HTTPException as ex:
            raise ex
        except Exception as ex:
            self.logger.error('Ошибка при авторизации в Яндексе')
            raise ex


class GetActiveUser(UseCase[HTTPAuthorizationCredentials, UserSchema]):

    def __init__(
        self,
        uow: IUnitOfWork,
        auth_service: IAuthService,
        logger: ILogger,
    ):
        self.uow = uow
        self.auth_service = auth_service
        self.logger = logger

    async def __call__(self, token_data: HTTPAuthorizationCredentials) -> User:
        try:
            async with self.uow:
                user_data = self.auth_service.get_user(token_data)
                user: UserModel = await self.uow.users.find_one(UserModel.email, user_data.email)
                if not user:
                    raise HTTPException(detail='User not found', status_code=404)
                if not user.is_active:
                    raise HTTPException(detail='User is not active', status_code=400)

                return user.to_domain()
        except HTTPException as ex:
            raise ex
        except Exception as ex:
            self.logger.error(f'Ошибка при получении пользователя | TokenData: {token_data}')
            raise ex


class GetSuperuser(UseCase[HTTPAuthorizationCredentials, UserSchema]):

    def __init__(
        self,
        uow: IUnitOfWork,
        auth_service: IAuthService,
        logger: ILogger,
    ):
        self.uow = uow
        self.auth_service = auth_service,
        self.logger = logger

    async def __call__(self, token_data: HTTPAuthorizationCredentials) -> User:
        try:
            async with self.uow:
                user_data = self.auth_service.get_user(token_data)
                user = await self.uow.users.find_one(UserModel.email, user_data.email)
                if not user:
                    raise HTTPException(detail='User not found', status_code=404)
                if not user.is_superuser:
                    raise HTTPException(detail='Permission denied', status_code=403)

                return user.to_domain()
        except HTTPException as ex:
            raise ex
        except Exception as ex:
            self.logger.error(f'Ошибка при получении суперпользователя | TokenData: {token_data}')
            raise ex


class UpdateToken(UseCase[User, TokenData]):

    def __init__(
        self,
        uow: IUnitOfWork,
        auth_service: IAuthService,
        settings: Settings,
        logger: ILogger
    ):
        self.uow = uow
        self.auth_service = auth_service
        self.settings = settings
        self.logger = logger

    async def __call__(self, user: User) -> TokenData:
        try:
            token = self.auth_service.create_access_token(
                user_data=UserData(email=user.email),
                expires_delta=timedelta(minutes=self.settings.ACCESS_TOKEN_EXPIRE_MINUTES)
            )
            self.logger.info(f'Пользователь {user.id} {user.email} обновил токен')
            return token
        except HTTPException as ex:
            raise ex
        except Exception as ex:
            self.logger.error(f'Ошибка при обновлении токена у пользователя '
                              f'{user.id} {user.email}')
            raise ex
