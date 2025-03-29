from abc import ABC, abstractmethod
from datetime import timedelta

from fastapi.security import HTTPAuthorizationCredentials

from src.domain.value_objects import UserData
from src.presentation.routers.schemas import UserSchema, TokenData


class IAuthService(ABC):

    @abstractmethod
    def get_user(self, token_data: HTTPAuthorizationCredentials) -> UserSchema:
        raise NotImplementedError

    @abstractmethod
    def create_access_token(
            self, user_data: UserData, expires_delta: timedelta | None = None
    ) -> TokenData:
        raise NotImplementedError
