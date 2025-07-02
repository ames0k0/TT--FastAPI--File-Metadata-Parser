import sqlalchemy as sa
import sqlalchemy.orm as sao

from core.config import settings
from . import models


class Postgres:
    engine: sa.Engine
    session_factory: sao.sessionmaker[sao.Session]

    @classmethod
    def initialize(cls):
        cls.engine = sa.create_engine(url=str(settings.POSTGRES_DSN))
        cls.session_factory = sao.sessionmaker(
            bind=cls.engine,
            expire_on_commit=False,
        )
        models.Base.metadata.create_all(cls.engine)

    @classmethod
    def get_scoped_session(cls) -> sao.scoped_session[sao.Session]:
        return sao.scoped_session(cls.session_factory)

    @classmethod
    def terminate(cls):
        cls.session_factory.close_all()
