import uuid
from typing import Annotated

import sqlalchemy.orm as sao
from fastapi import APIRouter
from fastapi import Depends
from fastapi import Request
from fastapi import UploadFile
from fastapi import File
from fastapi import status

from core import dependencies
from services.storage import FileStorageService
from services.database import FileMetadataService
from services.suip_data import SuipDataService


router = APIRouter(
    prefix="/suip-data",
    tags=["suip-data"],
)


@router.get("")
def download_record(
    request: Request,
    session: sao.Session = Depends(dependency=dependencies.get_session),
):
    """Список сохранённых результатов с возможностью фильтрации"""
    return FileMetadataService(
        session=session,
    ).filter(
        query_params=request.query_params,
    )


@router.post(
    "parse",
    status_code=status.HTTP_201_CREATED,
)
def upload_record(
    file: Annotated[
        UploadFile,
        File(description="Файл для парсинга"),
    ],
    session: sao.Session = Depends(dependency=dependencies.get_session),
):
    """Ручной запуск парсинга и сохранения данных в JSON-формате"""
    file_uuid = uuid.uuid4()
    file_metadata = SuipDataService(session=session).parse_file_metadata(
        file_bytes=file.file.read(),
    )

    file_name = file.filename
    if not file_name:
        file_name = str(file_uuid)

    fs_path = FileStorageService().create_json_file(
        file_id=file_uuid,
        data=file_metadata,
    )

    model = FileMetadataService(session=session).create(
        id=file_uuid,
        name=file_name,
        fs_path=fs_path,
        available_metadata=file_metadata,
    )

    return model
