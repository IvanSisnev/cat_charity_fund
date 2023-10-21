"""
Настройка БД.
"""
from sqlalchemy import Column, Integer
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import declarative_base, sessionmaker, declared_attr

from app.core.config import settings


class PreBase:
    """
    Расширение базового класса для всех моделей.
    """
    @declared_attr
    def __tablename__(cls) -> str: # noqa
        return cls.__name__.lower()

    id = Column(Integer, primary_key=True)


Base = declarative_base(cls=PreBase)

engine = create_async_engine(settings.db_url)

AsyncSessionLocal = sessionmaker(engine, class_=AsyncSession)


async def get_async_session():
    """
    Асинхронный генератор сессий.
    """
    async with AsyncSessionLocal() as async_session:
        yield async_session
