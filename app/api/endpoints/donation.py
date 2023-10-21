"""
Эндпоинты пожертвований.
"""
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.core.user import current_superuser, current_user
from app.crud.donation import donation_crud
from app.schemas.donation import (DonationCreateBase,
                                  DonationGet,
                                  DonationGetAll)
from app.models import User


router = APIRouter()


@router.post('/', response_model=DonationGet,
             response_model_exclude_none=True)
async def donation_create(donation: DonationCreateBase,
                          session: AsyncSession = Depends(get_async_session)):
    """
    Создать пожертвование.
    """
    new_donation = await donation_crud.create(donation, session)
    return new_donation


@router.get('/', response_model=list[DonationGetAll],
            response_model_exclude_none=True,
            dependencies=[Depends(current_superuser)])
async def donation_get_all(session: AsyncSession = Depends(get_async_session)):
    """
    Получить список всех пожертвований.
    """
    all_donations = await donation_crud.get_many(session)
    return all_donations


@router.get('/my', response_model=list[DonationGet],
            response_model_exclude_none=True,
            dependencies=[Depends(current_user)])
async def donation_get_all_by_user(
        session: AsyncSession = Depends(get_async_session),
        user: User = Depends(current_user)
):
    """
    Получить список всех пожертвований пользователя.
    """
    user_donations = await donation_crud.get_users_donations(user, session)
    return user_donations
