from typing import Annotated

from fastapi import Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from config import Settings
from src.application.use_cases.auth_usecases import GetActiveUser, GetSuperuser, UpdateToken, YandexAuth
from src.application.use_cases.file_usecases import SaveFile
from src.application.use_cases.user_usecases import DeleteUser, UpdateUser
from src.domain.entities import User
from src.domain.services.auth_service import AuthService
from src.infrastructure.external.yandex_client import YandexClient
from src.infrastructure.logger.logger import logger
from src.infrastructure.repositories.file_storage_repo import DiskStorageRepository
from src.infrastructure.session import async_session
from src.infrastructure.uow.impl import UnitOfWork

oauth_scheme = HTTPBearer()


class AuthDependencies:

    settings = Settings()
    uow = UnitOfWork(async_session)
    auth_service = AuthService(settings)
    yandex_client = YandexClient(settings)

    @classmethod
    async def get_auth(cls):
        return YandexAuth(
            cls.uow, cls.yandex_client, cls.auth_service, cls.settings, logger
        )

    @classmethod
    async def get_active_user(
            cls, token: Annotated[HTTPAuthorizationCredentials, Depends(oauth_scheme)]
    ) -> User:
        get_user = GetActiveUser(cls.uow, cls.auth_service, logger)
        return await get_user(token)

    @classmethod
    async def get_superuser(
            cls, token: Annotated[HTTPAuthorizationCredentials, Depends(oauth_scheme)]
    ) -> User:
        get_superuser = GetSuperuser(cls.uow, cls.auth_service, logger)
        return await get_superuser(token)

    @classmethod
    async def update_token(cls):
        return UpdateToken(cls.uow, cls.auth_service, cls.settings, logger)


class UserDependencies:
    uow = UnitOfWork(async_session)

    @classmethod
    async def update_user(cls):
        return UpdateUser(cls.uow, logger)

    @classmethod
    async def delete_user(cls):
        return DeleteUser(cls.uow, logger)


class FileDependencies:
    uow = UnitOfWork(async_session)
    file_storage_repo = DiskStorageRepository()
    settings = Settings()

    @classmethod
    async def save_file(cls):
        return SaveFile(cls.uow, cls.file_storage_repo, cls.settings, logger)
