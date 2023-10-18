"""
Валидаторы приложения.
"""
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.charityproject import charity_project_crud
from app.models import CharityProject


async def check_name_unique(charity_project_name: str,
                            session: AsyncSession) -> None:
    """
    Проверяет название проекта на уникальность.
    """
    charity_project_id = await charity_project_crud.get_id_by_name(
        charity_project_name, session
    )
    if charity_project_id:
        raise HTTPException(
            status_code=422,
            detail='Проект с таким именем уже существует в базе.',
        )


async def check_charity_project_exists(
        charity_project_id: int,
        session: AsyncSession,
) -> CharityProject:
    """
    Проверяет наличие проекта в БД.
    """
    charity_project = await charity_project_crud.get(
        charity_project_id,
        session
    )
    if not charity_project:
        raise HTTPException(
            status_code=404,
            detail='Такого проекта нет в базе.'
        )
    return charity_project
