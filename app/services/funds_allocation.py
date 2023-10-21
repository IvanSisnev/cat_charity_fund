"""
Управление пожертвованными средствами.
"""
from datetime import datetime
from typing import Type, Tuple

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import AbstractBase


async def full_amount_closure(obj: AbstractBase) -> AbstractBase:
    """
    Завершить проект или пожертвование.
    """
    obj.invested_amount = obj.full_amount
    obj.fully_invested = True
    obj.close_date = datetime.now()
    return obj


async def allocate_funds(obj_in: AbstractBase,
                         model: Type[AbstractBase],
                         session: AsyncSession) -> AbstractBase:
    """
    Распределить средства внутри проектов и пожертвований.
    """
    open_objs = await session.execute(select(model).where(
        model.fully_invested is False).order_by(model.create_date)
    )
    open_objs = open_objs.scalars().all()
    for open_obj in open_objs:
        obj_in, open_obj = await invested_amount_calculation(obj_in, open_obj)
        session.add(obj_in)
        session.add(open_obj)
    await session.commit()
    await session.refresh(obj_in)
    return obj_in


async def invested_amount_calculation(
        obj_in: AbstractBase,
        open_obj: AbstractBase) -> Tuple[AbstractBase, AbstractBase]:
    """
    Сравнить вносимую сумму с требуемой, зачесть и по необходимости закрыть
    проект или пожертвование.
    """
    obj_in_funds = obj_in.full_amount - obj_in.invested_amount
    open_obj_funds = open_obj.full_amount - open_obj.invested_amount
    if obj_in_funds > open_obj_funds:
        obj_in.invested_amount += open_obj_funds
        open_obj = await full_amount_closure(open_obj)
    elif obj_in_funds < open_obj_funds:
        open_obj.invested_amount += obj_in_funds
        obj_in = await full_amount_closure(obj_in)
    else:
        obj_in = await full_amount_closure(obj_in)
        open_obj = await full_amount_closure(open_obj)
    return obj_in, open_obj
