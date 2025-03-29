import os
import shutil
import uuid
from datetime import datetime
from typing import List, Optional
from uuid import UUID

from fastapi import UploadFile
from pydantic import BaseModel


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
    def factory(user_id: UUID, file: UploadFile, file_name: Optional[str]):
        if file_name:
            file_name = f'{file_name}.{file.filename.split(".")[-1]}'
        else:
            file_name = file.filename

        return AudioFile(
            id=uuid.uuid4(),
            name=file_name,
            path=f'{user_id}/{file_name}',
            date_added=datetime.utcnow(),
        )
