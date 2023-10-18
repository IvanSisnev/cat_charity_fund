"""
Валидаторы приложения.
"""
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.charityproject import charity_project_crud
from app.models import CharityProject


async def check_name_unique(
        charity_project_name: str,
        session: AsyncSession,
) -> None:
    charity_project_id = await meeting_room_crud.get_room_id_by_name(
        room_name, session)
    if room_id is not None:
        raise HTTPException(
            status_code=422,
            detail='Переговорка с таким именем уже существует!',
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
