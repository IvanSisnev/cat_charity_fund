"""
Валидаторы приложения.
"""
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.charity_project import charity_project_crud
from app.models import CharityProject


# todo HTTPStatus
# todo сообщения в константы?


async def check_charity_project_name_unique(charity_project_name: str,
                                            session: AsyncSession) -> None:
    """
    Проверяет название проекта на уникальность.
    """
    charity_project_id = await charity_project_crud.get_id_by_name(
        charity_project_name, session
    )
    if charity_project_id is not None:
        raise HTTPException(
            status_code=400,
            detail='Проект с таким именем уже существует!',
        )


async def check_charity_project_exists(
        charity_project_id: int,
        session: AsyncSession,
) -> CharityProject:
    """
    Проверить наличие проекта в БД.
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


async def check_charity_project_full_amount(
        full_amount: int,
        invested_amount: int
) -> None:
    """
    Проверить, что требуемая сумма не меньше внесенной.
    """
    if full_amount < invested_amount:
        raise HTTPException(
            status_code=400,
            detail='Требуемая сумма не может быть меньше внесенной.'
        )


async def check_charity_project_before_editing(
        charity_project_id: int,
        session: AsyncSession,
        message='Закрытый проект нельзя редактировать!'
) -> CharityProject:
    """
    Проверить проект перед его изменением: проект существует и он не закрыт.
    """
    charity_project = await check_charity_project_exists(
        charity_project_id, session
    )

    if charity_project.fully_invested:
        raise HTTPException(
            status_code=400,
            detail=message
        )
    return charity_project


async def check_charity_project_before_deleting(
        charity_project_id: int,
        session: AsyncSession,
) -> CharityProject:
    """
    Проверить проект перед удалением: проект существует, он не закрыт и в
    него не внесены средства.
    """
    charity_project = await check_charity_project_before_editing(
        charity_project_id, session,
        message='В проект были внесены средства, не подлежит удалению!'
    )

    if charity_project.invested_amount > 0:
        raise HTTPException(
            status_code=400,
            detail='В проект были внесены средства, не подлежит удалению!'
        )
    return charity_project
