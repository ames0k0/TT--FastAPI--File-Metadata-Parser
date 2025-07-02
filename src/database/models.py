from datetime import datetime

from sqlalchemy import func
from sqlalchemy import JSON
from sqlalchemy import UUID
from sqlalchemy import DateTime
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column


class Base(DeclarativeBase):
    pass


class FileMetadata(Base):
    __tablename__ = "file_metadata"

    id: Mapped[str] = mapped_column(UUID, primary_key=True)
    name: Mapped[str]
    fs_path: Mapped[str]
    available_metadata: Mapped[dict] = mapped_column(JSON)

    created_at: Mapped[datetime] = mapped_column(DateTime, default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, default=func.now(), onupdate=func.now()
    )

    def __repr__(self) -> str:
        return f"FileMetadata(id={self.id!r}, file_name={self.name!r})"
