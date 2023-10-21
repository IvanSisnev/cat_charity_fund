"""
Эндпоинты благотворительных проектов.
"""
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.core.user import current_superuser
from app.crud.charity_project import charity_project_crud
from app.schemas.charity_project import (CharityProjectCreate,
                                         CharityProjectRead,
                                         CharityProjectUpdate)
from app.api.validators import (check_charity_project_name_unique,
                                check_charity_project_before_editing,
                                check_charity_project_before_deleting,
                                check_charity_project_full_amount)
from app.services.funds_allocation import allocate_funds
from app.models import Donation

router = APIRouter()


@router.post(
    '/',
    response_model=CharityProjectRead,
    response_model_exclude_none=True,
    dependencies=[Depends(current_superuser)],
)
async def charity_project_create(
        charity_project: CharityProjectCreate,
        session: AsyncSession = Depends(get_async_session)
):
    """
    Создать благотворительный проект.
    """
    await check_charity_project_name_unique(charity_project.name, session)
    new_project = await charity_project_crud.create(charity_project, session)
    new_project = await allocate_funds(new_project, Donation, session)
    return new_project


@router.get(
    '/',
    response_model=list[CharityProjectRead],
    response_model_exclude_none=True
)
async def charity_project_get_all(
        session: AsyncSession = Depends(get_async_session),
):
    """
    Получить список всех благотворительных проектов.
    """
    all_projects = await charity_project_crud.get_many(session)
    return all_projects


@router.patch(
    '/{charity_project_id}',
    response_model=CharityProjectRead,
    dependencies=[Depends(current_superuser)]
)
async def charity_project_update(
        charity_project_id: int,
        obj_in: CharityProjectUpdate,
        session: AsyncSession = Depends(get_async_session),
):
    """
    Изменить существующий проект.
    """
    if obj_in.name:
        await check_charity_project_name_unique(obj_in.name, session)
    charity_project = await check_charity_project_before_editing(
        charity_project_id,
        session
    )
    if obj_in.full_amount:
        await check_charity_project_full_amount(obj_in.full_amount,
                                                charity_project.invested_amount
                                                )
    charity_project = await charity_project_crud.update(charity_project,
                                                        obj_in,
                                                        session)
    charity_project = await allocate_funds(charity_project, Donation, session)
    return charity_project


@router.delete(
    '/{charity_project_id}',
    response_model=CharityProjectRead,
    dependencies=[Depends(current_superuser)]
)
async def charity_project_delete(
        charity_project_id: int,
        session: AsyncSession = Depends(get_async_session),
):
    """
    Удалить проект из БД.
    """
    charity_project = await check_charity_project_before_deleting(
        charity_project_id, session)
    charity_project = await charity_project_crud.remove(charity_project,
                                                        session)
    return charity_project
