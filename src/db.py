from sqlalchemy.orm import declarative_base, declared_attr, sessionmaker
from typing import AsyncGenerator
from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import (AsyncSession, async_sessionmaker,
                                    create_async_engine)
from sqlalchemy.orm import DeclarativeBase, declared_attr, sessionmaker

from src.config import settings

ASYNC_DATABASE_URL = f'postgresql+asyncpg://{settings.DB_USER}:{settings.DB_PASS}@{settings.DB_HOST}:{settings.DB_PORT}/{settings.DB_NAME}'
async_engine = create_async_engine(ASYNC_DATABASE_URL)
async_session_maker = async_sessionmaker(
    async_engine,
    class_=AsyncSession,
    expire_on_commit=False,
)

class PreBase:
    ''' Для alembic. '''

    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()

Base = declarative_base(cls=PreBase)

async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session

