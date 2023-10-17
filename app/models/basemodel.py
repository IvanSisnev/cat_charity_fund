"""
Базовый класс для моделей.
"""
from datetime import datetime

from sqlalchemy import Column, Integer, Boolean, DateTime

from app.core.db import Base


class AbstractBase(Base): # noqa
    __abstract__ = True
    # todo
    # __table_args__ = (
    # CheckConstraint('full_amount >= invested_amount >= 0'),
    # )
    # todo ограничения здесь?
    full_amount = Column(Integer)
    invested_amount = Column(Integer, default=0)
    fully_invested = Column(Boolean, default=False)
    create_date = Column(DateTime, default=datetime.now)
    close_date = Column(DateTime)

    def __repr__(self):
        return f'{self.invested_amount} из {self.full_amount}.'
