import json
from uuid import UUID

from core.config import settings


class FileStorageService:
    """FileStorage Service"""

    def create_json_file(self, file_id: UUID, data: dict) -> str:
        fs_path = settings.FILE_METADATA_FILEPATH_TEMPLATE.as_posix().format(
            FILE_ID=file_id,
        )
        with open(file=fs_path, mode="w") as ftw:
            json.dump(data, ftw)

        return fs_path
