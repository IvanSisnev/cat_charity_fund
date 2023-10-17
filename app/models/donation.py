"""
Модель пожертвований.
"""
from sqlalchemy import Column, Integer, ForeignKey, Text

from basemodel import AbstractBase


class Donation(AbstractBase):  # noqa
    user_id = Column(Integer, ForeignKey('user.id'))
    comment = Column(Text, nullable=True)

    def __repr__(self):
        return f'Пожертвование. Распределено по проектам: {super().__repr__()}'
