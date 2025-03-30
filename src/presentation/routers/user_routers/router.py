from typing import Annotated

from fastapi import APIRouter, Response
from fastapi.params import Depends

from config import VERSION
from src.application.use_cases.user_usecases import DeleteUser, UpdateUser
from src.domain.entities import User
from src.domain.value_objects import UserData
from src.presentation.dependencies import AuthDependencies, UserDependencies
from src.presentation.routers.schemas import UserSchema

router = APIRouter(
    prefix=f'/api/v{VERSION}/users',
    tags=['Users']
)


@router.patch(
    path='',
    summary='Обновление личных данных'
)
async def update_user(
    new_user_data: UserData,
    user: Annotated[User, Depends(AuthDependencies.get_active_user)],
    update_user: Annotated[UpdateUser, Depends(UserDependencies.update_user)]
) -> UserSchema:
    return await update_user(user, new_user_data)


@router.delete(
    path='/{email}',
    summary='Удаление пользователя',
    dependencies=[Depends(AuthDependencies.get_superuser)],
    status_code=204
)
async def delete_user(
    email: str,
    delete_user: Annotated[DeleteUser, Depends(UserDependencies.delete_user)]
):
    await delete_user(email)
    return Response(status_code=204)
