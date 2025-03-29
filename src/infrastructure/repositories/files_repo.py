from sqlalchemy.ext.asyncio import AsyncSession

from src.infrastructure.models import FileModel
from src.infrastructure.repositories.base import SQLAlchemyRepository
from src.infrastructure.repositories.interfaces import IFilesRepository


class FilesRepository(SQLAlchemyRepository, IFilesRepository):

    def __init__(self, session: AsyncSession):
        self.__session = session
        super().__init__(session, FileModel)
