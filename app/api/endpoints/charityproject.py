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

router = APIRouter()


@router.post(
    '/', response_model=CharityProjectRead,
    # response_model_exclude_none=True,
)
async def charity_project_create(
        charity_project: CharityProjectCreate,
        session: AsyncSession = Depends(get_async_session)
):
    """
    Создает благотворительный проект.
    """
    # TODO проверка на уникальность названия
    new_project = await charity_project_crud.create(charity_project, session)
    return new_project
