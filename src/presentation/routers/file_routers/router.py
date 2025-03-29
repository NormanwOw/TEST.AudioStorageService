from typing import Annotated, List

from fastapi import UploadFile, File, APIRouter, Response
from fastapi.params import Depends

from config import VERSION
from src.application.use_cases.file_usecases import SaveFile
from src.domain.entities import User
from src.presentation.dependencies import FileDependencies, AuthDependencies
from src.presentation.routers.schemas import FileSchema

router = APIRouter(
    prefix=f'/api/v{VERSION}/files',
    tags=['Files']
)


@router.get('')
async def get_files_info(
    user: Annotated[User, Depends(AuthDependencies.get_active_user)]
) -> List[FileSchema]:
    return user.files


@router.post('')
async def upload_audio(
    save_file: Annotated[SaveFile, Depends(FileDependencies.save_file)],
    user: Annotated[User, Depends(AuthDependencies.get_active_user)],
    file: UploadFile = File(...),
    file_name: str = None,
):
    await save_file(user, file, file_name)
    return Response(status_code=201)
