import os
import shutil
from datetime import datetime
from typing import List
from uuid import UUID

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
