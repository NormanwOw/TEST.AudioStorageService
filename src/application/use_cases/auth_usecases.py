from datetime import timedelta

from config import Settings
from src.application.use_cases.base import UseCase
from src.domain.interfaces import IAuthService
from src.infrastructure.external.base_client import Client
from src.infrastructure.models import UserModel
from src.infrastructure.uow.interfaces import IUnitOfWork
from src.presentation.routers.schemas import TokenData


class YandexAuth(UseCase[str, TokenData]):

    def __init__(
            self,
            uow: IUnitOfWork,
            yandex_client: Client,
            auth_service: IAuthService,
            settings: Settings
    ):
        self.uow = uow
        self.yandex_client = yandex_client
        self.auth_service = auth_service
        self.settings = settings

    async def __call__(self, code: str) -> TokenData:
        async with self.uow:
            user_data = await self.yandex_client.get_user_data(code)
            user = UserModel(email=user_data.email)
            await self.uow.users.add(user)
            token = self.auth_service.create_access_token(
                user_data=user_data,
                expires_delta=timedelta(minutes=self.settings.ACCESS_TOKEN_EXPIRE_MINUTES)
            )
            await self.uow.commit()
            return token
