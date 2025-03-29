from typing import Optional

from aiohttp.abc import HTTPException
from fastapi import UploadFile

from config import Settings
from src.application.use_cases.base import UseCase
from src.domain.entities import User, AudioFile
from src.infrastructure.logger.interfaces import ILogger
from src.infrastructure.models import FileModel
from src.infrastructure.repositories.interfaces import FilesStorageRepository
from src.infrastructure.uow.interfaces import IUnitOfWork


class SaveFile(UseCase[[User, UploadFile], None]):

    def __init__(
        self,
        uow: IUnitOfWork,
        file_storage_repo: FilesStorageRepository,
        settings: Settings,
        logger: ILogger,
    ):
        self.uow = uow
        self.file_storage_repo = file_storage_repo
        self.settings = settings
        self.logger = logger

    async def __call__(self, user: User, file: UploadFile, file_name: Optional[str]):
        try:
            async with self.uow:
                extension = file.filename.split('.')[-1]
                AudioFile.check_extension(extension, self.settings)
                file_entity = AudioFile.factory(user.id, file, file_name)
                file_model = FileModel(**file_entity.model_dump(), user_id=user.id)
                await self.uow.files.add(file_model)
                await self.file_storage_repo.save(user.id, file, file_entity.name)
                await self.uow.commit()
                self.logger.info(f'Сохранён файл {file_entity.name} пользователя {user.id}')
        except HTTPException as ex:
            raise ex
        except Exception as ex:
            self.logger.error(f'Ошибка при сохранении файла '
                              f'{file_entity.name} у пользователя {user.id} {user.email}')
            raise ex
