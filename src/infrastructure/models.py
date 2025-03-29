import uuid
from datetime import datetime
from typing import List

from sqlalchemy import UUID, ForeignKey
from sqlalchemy.dialects.postgresql import TIMESTAMP
from sqlalchemy.orm import DeclarativeBase, mapped_column, Mapped, relationship

from src.domain.entities import User, AudioFile


class Base(DeclarativeBase):
    id: Mapped[uuid] = mapped_column(
        UUID, nullable=False, primary_key=True, unique=True, default=uuid.uuid4
    )


class FileModel(Base):
    __tablename__ = 'files'

    name: Mapped[str] = mapped_column(nullable=False, index=True)
    path: Mapped[str] = mapped_column(nullable=False)
    user_id: Mapped[uuid] = mapped_column(
        ForeignKey('users.id', ondelete='CASCADE'), nullable=False
    )
    date_added: Mapped[datetime] = mapped_column(TIMESTAMP, default=datetime.utcnow, nullable=False)

    user = relationship(
        'UserModel',
        back_populates='files',
        uselist=False,
        lazy='selectin'
    )


class UserModel(Base):
    __tablename__ = 'users'

    email: Mapped[str] = mapped_column(nullable=False, unique=True, index=True)
    is_active: Mapped[bool] = mapped_column(default=True)
    is_superuser: Mapped[bool] = mapped_column(default=False)
    date_added: Mapped[datetime] = mapped_column(TIMESTAMP, default=datetime.utcnow, nullable=False)

    files: Mapped[List['FileModel']] = relationship(
        'FileModel',
        back_populates='user',
        cascade='all, delete-orphan',
        lazy='selectin'
    )

    def to_domain(self) -> User:
        return User(
            id=self.id,
            email=self.email,
            is_active=self.is_active,
            is_superuser=self.is_superuser,
            date_added=self.date_added,
            files=[
                AudioFile(
                    id=file.id,
                    name=file.name,
                    path=file.path,
                    date_added=file.date_added
                ) for file in self.files
            ],
        )
