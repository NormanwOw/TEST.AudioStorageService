import os
from uuid import UUID

import aiofiles
from fastapi import UploadFile

from src.infrastructure.repositories.interfaces import FilesStorageRepository


class DiskStorageRepository(FilesStorageRepository):

    async def save(self, user_id: UUID, file: UploadFile, file_name: str):
        user_folder = f'audio_files/{user_id}'
        await self.create_folder(user_folder)

        async with aiofiles.open(f'{user_folder}/{file_name}', 'wb') as f:
            await f.write(await file.read())

    async def create_folder(self, user_folder: str):
        if not os.path.exists(user_folder):
            os.makedirs(user_folder)
