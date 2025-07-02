from uuid import UUID

import sqlalchemy as sa
from starlette.datastructures import QueryParams
from sqlalchemy.dialects.postgresql import JSONB

from database import models
from services.base import BaseService


class FileMetadataService(BaseService):
    """FileMetadata Service"""

    def create(
        self, id: UUID, name: str, fs_path: str, available_metadata: dict
    ) -> models.FileMetadata:
        """Creates FileMetadata object"""
        file_metadata = models.FileMetadata(
            id=id,
            name=name,
            fs_path=fs_path,
            available_metadata=available_metadata,
        )
        self.session.add(file_metadata)
        self.session.commit()

        return file_metadata

    def filter(self, query_params: QueryParams):
        """Filters by query params"""
        return (
            self.session.query(models.FileMetadata)
            .filter(
                models.FileMetadata.available_metadata.cast(JSONB).contains(
                    sa.cast(dict(query_params), JSONB),
                )
            )
            .all()
        )
