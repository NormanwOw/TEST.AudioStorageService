from typing import Optional

from fastapi import UploadFile

from src.application.use_cases.base import UseCase
from src.domain.entities import User, AudioFile
from src.infrastructure.models import FileModel
from src.infrastructure.repositories.interfaces import FilesStorageRepository
from src.infrastructure.uow.interfaces import IUnitOfWork


class SaveFile(UseCase[[User, UploadFile], None]):

    def __init__(
        self,
        uow: IUnitOfWork,
        file_storage_repo: FilesStorageRepository
    ):
        self.uow = uow
        self.file_storage_repo = file_storage_repo

    async def __call__(self, user: User, file: UploadFile, file_name: Optional[str]):
        async with self.uow:
            file_entity = AudioFile.factory(user.id, file, file_name)
            file_model = FileModel(**file_entity.model_dump(), user_id=user.id)
            await self.uow.files.add(file_model)
            await self.file_storage_repo.save(user.id, file, file_entity.name)
            await self.uow.commit()
