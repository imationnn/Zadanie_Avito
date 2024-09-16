from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

from app.config import PGConfig


class PGDatabase:
    def __init__(self, pg_config: PGConfig = PGConfig()):
        self.pg_config = pg_config
        self.engine = create_async_engine(url=self.pg_config.pg_dsn, echo=self.pg_config.echo)
        self.async_session_factory = async_sessionmaker(
            bind=self.engine,
            autoflush=False,
            autocommit=False,
            expire_on_commit=False
        )

    @property
    def session_factory(self):
        return self.async_session_factory

    async def get_session(self) -> AsyncGenerator[AsyncSession, None]:
        async with self.async_session_factory() as session:
            yield session


db_connector = PGDatabase()
