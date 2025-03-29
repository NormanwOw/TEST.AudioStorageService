from datetime import timedelta, datetime, timezone

from fastapi import HTTPException
from fastapi.security import HTTPAuthorizationCredentials
from jwt import InvalidTokenError
from passlib.context import CryptContext
import jwt

from config import Settings, settings
from src.domain.value_objects import UserData
from src.presentation.routers.schemas import UserSchema, TokenData


class AuthService:

    def __init__(self, settings: Settings):
        self.settings = settings
        self.pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')

    def get_user(self, token_data: HTTPAuthorizationCredentials) -> UserSchema:
        credentials_exception = HTTPException(
            status_code=401,
            detail='Could not validate credentials',
            headers={'WWW-Authenticate': 'Bearer'},
        )
        try:
            payload = jwt.decode(
                token_data.credentials,
                settings.SECRET_KEY,
                algorithms=[settings.ALGORITHM]
            )
            email: str = payload.get('sub')
            if email is None:
                raise credentials_exception

        except InvalidTokenError:
            raise credentials_exception

        return UserSchema(email=email)

    def create_access_token(self, user_data: UserData, expires_delta: timedelta | None = None) -> TokenData:
        if not expires_delta:
            expires_delta = timedelta(minutes=15)

        expire = datetime.now(timezone.utc) + expires_delta
        encoded_jwt = jwt.encode(
            {'exp': expire, 'sub': user_data.email},
            self.settings.SECRET_KEY, algorithm=self.settings.ALGORITHM
        )
        return TokenData(token=encoded_jwt)
