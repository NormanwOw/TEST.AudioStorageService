import os
import shutil
import uuid
from datetime import datetime
from typing import List, Optional
from uuid import UUID

from fastapi import UploadFile, HTTPException
from pydantic import BaseModel

from config import Settings


class User(BaseModel):
    id: UUID
    email: str
    is_active: bool
    is_superuser: bool
    date_added: datetime
    files: List['AudioFile']

    def delete_files(self):
        folder_path = f'audio_files/{self.id}'
        if os.path.exists(folder_path) and os.path.isdir(folder_path):
            shutil.rmtree(folder_path)
        self.files.clear()


class AudioFile(BaseModel):
    id: UUID
    name: str
    path: str
    date_added: datetime

    @staticmethod
    def factory(
        user_id: UUID, file: UploadFile, file_name: Optional[str]
    ) -> 'AudioFile':
        extension = file.filename.split('.')[-1]
        if file_name:
            file_name = f'{file_name}.{extension}'
        else:
            file_name = file.filename

        return AudioFile(
            id=uuid.uuid4(),
            name=file_name,
            path=f'{user_id}/{file_name}',
            date_added=datetime.utcnow(),
        )

    @staticmethod
    def check_extension(extension: str, settings: Settings):
        allowed_extensions = settings.ALLOWED_AUDIO_EXTENSIONS
        if extension not in allowed_extensions:
            str_extensions = ', '.join(allowed_extensions)
            raise HTTPException(
                status_code=400,
                detail=f'Allowed audio file extensions are {str_extensions}',
            )
