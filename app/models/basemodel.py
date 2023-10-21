"""
Базовый класс для моделей.
"""
from datetime import datetime

from sqlalchemy import Column, Integer, Boolean, DateTime

from app.core.db import Base

# todo переименовать?
class AbstractBase(Base): # noqa
    __abstract__ = True
    full_amount = Column(Integer)
    invested_amount = Column(Integer, default=0)
    fully_invested = Column(Boolean, default=False)
    create_date = Column(DateTime, default=datetime.now)
    close_date = Column(DateTime)

    def __repr__(self):
        return f'{self.invested_amount} из {self.full_amount}.'
