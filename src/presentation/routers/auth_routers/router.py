from typing import Annotated

from fastapi import APIRouter
from fastapi.params import Depends

from config import VERSION
from src.application.use_cases.auth_usecases import YandexAuth, UpdateToken
from src.domain.entities import User
from src.presentation.dependencies import AuthDependencies
from src.presentation.routers.schemas import TokenData, UserSchema

router = APIRouter(
    prefix=f'/api/v{VERSION}/auth',
    tags=['Auth']
)


@router.get('/yandex')
async def auth_callback(
    code: str,
    auth: Annotated[YandexAuth, Depends(AuthDependencies.get_auth)],
) -> TokenData:
    return await auth(code)


@router.get('/token')
async def update_token(
        user: Annotated[User, Depends(AuthDependencies.get_active_user)],
        update_token: Annotated[UpdateToken, Depends(AuthDependencies.update_token)],
) -> TokenData:
    return await update_token(user)


@router.get('/me')
async def get_me(
        user: Annotated[UserSchema, Depends(AuthDependencies.get_active_user)]
) -> UserSchema:
    return user
