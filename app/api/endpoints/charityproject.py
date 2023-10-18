"""
Эндпоинты благотворительных проектов.
"""
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.crud.charityproject import charity_project_crud
from app.schemas.charityproject import (CharityProjectCreate,
                                        CharityProjectRead,
                                        CharityProjectUpdate)
from app.api.validators import (check_name_unique,
                                check_charity_project_exists)

router = APIRouter()


@router.post(
    '/', response_model=CharityProjectRead,
)
async def charity_project_create(
        charity_project: CharityProjectCreate,
        session: AsyncSession = Depends(get_async_session)
):
    """
    Создает благотворительный проект.
    """
    await check_name_unique(charity_project.name, session)
    new_project = await charity_project_crud.create(charity_project, session)
    return new_project


@router.get(
    '/',
    response_model=list[CharityProjectRead],
)
async def charity_project_get_all(
        session: AsyncSession = Depends(get_async_session),
):
    """
    Возвращает список всех благотворительных проектов.
    """
    all_projects = await charity_project_crud.get_many(session)
    return all_projects


@router.patch(
    '/{charity_project_id}',
    response_model=CharityProjectRead,
)
async def charity_project_update(
        charity_project_id: int,
        obj_in: CharityProjectUpdate,
        session: AsyncSession = Depends(get_async_session),
):
    """
    Изменение существующего проекта.
    """
    charity_project = await check_charity_project_exists(charity_project_id,
                                                         session)
    if obj_in.name:
        await check_name_unique(obj_in.name, session)

    charity_project = await charity_project_crud.update(charity_project,
                                                        obj_in,
                                                        session)
    return charity_project


@router.delete(
    '/{charity_project_id}',
    response_model=CharityProjectRead,
)
async def charity_project_delete(
        charity_project_id: int,
        session: AsyncSession = Depends(get_async_session),
):
    """
    Удаляет проект в БД.
    """
    charity_project = await check_charity_project_exists(
        charity_project_id, session
    )
    charity_project = await charity_project_crud.remove(
        charity_project, session
    )
    return charity_project
