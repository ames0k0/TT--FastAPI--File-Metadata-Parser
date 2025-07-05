import os
from pathlib import Path

import psycopg2


class Postgres:
    __slots__ = ("conn",)

    def __init__(self):
        self.conn = psycopg2.connect(os.environ.get("POSTGRES_DSN"))
        self.create_tables()

    def create_tables(self):
        cursor = self.conn.cursor()
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS file_metadata (
                id                  UUID PRIMARY KEY,
                name                VARCHAR,
                fs_path             VARCHAR,
                available_metadata  JSON
            )
            """
        )
        self.conn.commit()


class Settings:
    APP_HOST: str = os.environ.get("APP_HOST", "localhost")
    APP_PORT: int = int(os.environ.get("APP_PORT", "8000"))

    postgres: Postgres = Postgres()

    STATIC_DIRECTORY: Path = Path("static") / "file_metadata"
    STATIC_DIRECTORY.mkdir(exist_ok=True, parents=True)

    FILE_METADATA_FILEPATH_TEMPLATE: Path = STATIC_DIRECTORY / "{FILE_ID}.json"


settings = Settings()
