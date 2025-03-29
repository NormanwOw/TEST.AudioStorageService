from abc import ABC, abstractmethod
from typing import Any, TypeVar
from uuid import UUID

from fastapi import UploadFile
from sqlalchemy.orm import InstrumentedAttribute

from src.infrastructure.models import Base

T = TypeVar('T', bound=Base)


class ISQLAlchemyRepository(ABC):

    @abstractmethod
    async def add(self, data: T) -> T:
        raise NotImplementedError

    @abstractmethod
    async def find_all(
            self,
            filter_field: InstrumentedAttribute = None,
            filter_value: Any = None,
            order_by: InstrumentedAttribute = None
    ) -> list[T]:
        raise NotImplementedError

    @abstractmethod
    async def find_one(self, filter_field: InstrumentedAttribute = None, filter_value: Any = None) -> T:
        raise NotImplementedError

    @abstractmethod
    async def update(
            self, values: dict,
            filter_field: InstrumentedAttribute = None,
            filter_value: Any = None
    ):
        raise NotImplementedError

    @abstractmethod
    async def delete_one(
            self,
            filter_field: InstrumentedAttribute,
            filter_value: Any
    ):
        raise NotImplementedError

    @abstractmethod
    async def delete(self):
        raise NotImplementedError


class IUsersRepository(ISQLAlchemyRepository, ABC):

    @abstractmethod
    async def delete_by_email(self, email: str):
        raise NotImplementedError


class IFilesRepository(ISQLAlchemyRepository, ABC):
    pass


class FilesStorageRepository(ABC):

    @abstractmethod
    async def save(self, user_id: UUID, file: UploadFile, file_name: str):
        raise NotImplementedError
