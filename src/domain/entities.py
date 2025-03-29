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


class AudioFile(BaseModel):
    id: UUID
    name: str
    path: str
    date_added: datetime
