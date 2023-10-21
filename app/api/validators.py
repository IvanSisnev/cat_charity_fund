"""
Валидаторы приложения.
"""
from http import HTTPStatus

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.charity_project import charity_project_crud
from app.models import CharityProject
from app.core.error_messages import (project_name_already_exists,
                                     funded_project_deletion_not_allowed,
                                     finished_project_no_editing,
                                     full_vs_invested_controversy,
                                     non_existing_project
                                     )


async def check_charity_project_name_unique(charity_project_name: str,
                                            session: AsyncSession) -> None:
    """
    Проверить название проекта на уникальность.
    """
    charity_project_id = await charity_project_crud.get_id_by_name(
        charity_project_name, session
    )
    if charity_project_id is not None:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail=project_name_already_exists,
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
            status_code=HTTPStatus.NOT_FOUND,
            detail=non_existing_project
        )
    return charity_project


async def check_charity_project_full_amount(
        full_amount: int,
        invested_amount: int
) -> None:
    """
    Проверить, что требуемая сумма не меньше уже внесенной.
    """
    if full_amount < invested_amount:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail=full_vs_invested_controversy
        )


async def check_charity_project_before_editing(
        charity_project_id: int,
        session: AsyncSession,
        message=finished_project_no_editing
) -> CharityProject:
    """
    Проверить проект перед его изменением: проект существует и он не закрыт.
    """
    charity_project = await check_charity_project_exists(
        charity_project_id, session
    )

    if charity_project.fully_invested:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
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
        message=funded_project_deletion_not_allowed
    )

    if charity_project.invested_amount > 0:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail=funded_project_deletion_not_allowed
        )
    return charity_project
