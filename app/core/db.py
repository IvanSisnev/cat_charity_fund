"""
Настройка БД
"""
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from app.core.config import settings

Base = declarative_base()
engine = create_async_engine(settings.db_url)
AsyncSessionLocal = sessionmaker(engine, class_=AsyncSession)


async def get_async_session():
    """
    Асинхронный генератор сессий.
    """
    async with AsyncSessionLocal() as async_session:
        yield async_session
