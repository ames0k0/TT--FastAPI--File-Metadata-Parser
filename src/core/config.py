from pathlib import Path
from pydantic import PostgresDsn, Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    APP_HOST: str = "localhost"
    APP_PORT: int = 8000

    POSTGRES_DSN: PostgresDsn = Field(default=...)

    STATIC_DIRECTORY: Path = Path("static") / "file_metadata"
    STATIC_DIRECTORY.mkdir(exist_ok=True, parents=True)

    FILE_METADATA_FILEPATH_TEMPLATE: Path = STATIC_DIRECTORY / "{FILE_ID}.json"


settings = Settings()
