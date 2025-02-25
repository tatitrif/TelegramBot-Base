from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from utils import singleton


class DataBaseError(Exception):
    pass


@singleton
class DatabaseSessionManager:
    def __init__(self) -> None:
        self._engine: AsyncEngine | None = None
        self._session_maker: async_sessionmaker[AsyncSession] | None = None

    def init(
        self,
        host: str,
        engine_kwargs: dict = None,
        session_kwargs: dict = None,
    ) -> None:
        engine_kwargs = engine_kwargs if engine_kwargs else {}
        session_kwargs = session_kwargs if session_kwargs else {}

        self._engine = create_async_engine(host, **engine_kwargs)
        self._session_maker = async_sessionmaker(
            bind=self._engine,
            **session_kwargs,
        )

    @asynccontextmanager
    async def session(self) -> AsyncIterator[AsyncSession]:
        if self._session_maker is None:
            raise DataBaseError("DatabaseSessionManager is not initialized")
        async with self._session_maker() as session:
            try:
                yield session
            except Exception:
                await session.rollback()
                raise


db_manager: DatabaseSessionManager = DatabaseSessionManager()
