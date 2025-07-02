import contextlib
from typing import Generator

import sqlalchemy.orm as sao
from fastapi import FastAPI

from database.app import Postgres


@contextlib.asynccontextmanager
async def lifespan(app: FastAPI):
    """`startup` and `shutdown` logic"""
    Postgres.initialize()
    yield
    Postgres.terminate()


def get_session() -> Generator[sao.Session, None, None]:
    scoped_session = Postgres.get_scoped_session()
    with scoped_session() as session:
        yield session
