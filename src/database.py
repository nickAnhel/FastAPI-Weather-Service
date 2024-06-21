from typing import AsyncGenerator, Any
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import DeclarativeBase

from .config import settings


async_engine = create_async_engine(
    url=settings.db_settings.db_url,
    echo=settings.db_settings.echo,
)

async_session = async_sessionmaker(
    bind=async_engine,
    class_=AsyncSession,
    autoflush=False,
    autocommit=False,
    expire_on_commit=False,
)


async def get_async_session() -> AsyncGenerator[AsyncSession, Any]:
    async with async_session() as session:
        yield session


class Base(DeclarativeBase):
    def __repr__(self) -> str:
        res = []
        for key, value in self.__dict__.items():
            if not key.startswith("_"):
                res.append(f"{key}={repr(value)}")
        return f"{self.__class__.__name__}({', '.join(res)})"


async def create_tables() -> None:
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def drop_tables() -> None:
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
