import uuid
import json
from typing import Annotated

from fastapi import FastAPI
from fastapi import Request
from fastapi import UploadFile
from fastapi import File
from fastapi import status
from psycopg2.extras import Json

from services.suip_data import SuipDataService
from core.config import settings


app = FastAPI(
    title="Тестовое задания",
    summary="REST API для запуска парсинга и получения сохранённых данных​",
)


@app.get(
    "/suip-data",
    tags=["suip-data"],
)
def get_filtered_file_metadata(
    request: Request,
):
    """Список сохранённых результатов с возможностью фильтрации"""
    cursor = settings.postgres.conn.cursor()
    cursor.execute(
        """
        SELECT * FROM file_metadata
        WHERE available_metadata::jsonb @> %s::jsonb
        """,
        (Json(dict(request.query_params)),),
    )
    return cursor.fetchall()


@app.post(
    "/suip-data/parse",
    status_code=status.HTTP_201_CREATED,
    tags=["suip-data"],
)
def post_file_to_parse_metadata(
    file: Annotated[
        UploadFile,
        File(description="Файл для парсинга"),
    ],
):
    """Ручной запуск парсинга и сохранения данных в JSON-формате"""

    file_metadata = SuipDataService().parse_file_metadata(
        file_bytes=file.file.read(),
    )

    file_uuid = str(uuid.uuid4())

    # Local Storage
    fs_path = settings.FILE_METADATA_FILEPATH_TEMPLATE.as_posix().format(
        FILE_ID=file_uuid,
    )
    with open(file=fs_path, mode="w") as ftw:
        json.dump(file_metadata, ftw)

    cursor = settings.postgres.conn.cursor()
    cursor.execute(
        """
        INSERT INTO file_metadata VALUES (
            %s, %s, %s, %s
        )
        """,
        (
            file_uuid,
            file.filename or str(file_uuid),
            fs_path,
            Json(file_metadata),
        ),
    )
    settings.postgres.conn.commit()


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        app=app,
        host=settings.APP_HOST,
        port=settings.APP_PORT,
    )
