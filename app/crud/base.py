"""
Базовый класс для операций с БД.
"""
from fastapi.encoders import jsonable_encoder
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession


class BaseCRUD:
    """
    Описывает базовые методы для операций с БД.
    """
    def __init__(self, model):
        self.model = model

    async def get(
            self,
            obj_id: int,
            session: AsyncSession,
    ):
        """
        Забирает объект модели из БД по его id.
        """
        db_obj = await session.execute(
            select(self.model).where(
                self.model.id == obj_id
            )
        )
        return db_obj.scalars().first()

    async def get_many(
            self,
            session: AsyncSession
    ):
        """
        Забирает список всех объектов модели из БД.
        """
        db_objs = await session.execute(select(self.model))
        return db_objs.scalars().all()

    async def create(
            self,
            obj_in,
            session: AsyncSession,
            # todo
            # user: Optional[User] = None
    ):
        """
        Записывает объект модели в БД.
        """
        obj_in_data = obj_in.dict()
        # todo
        # # Если пользователь был передан...
        # if user is not None:
        #     # ...то дополнить словарь для создания модели.
        #     obj_in_data['user_id'] = user.id
        db_obj = self.model(**obj_in_data)
        session.add(db_obj)
        await session.commit()
        await session.refresh(db_obj)
        return db_obj

    async def update( # noqa
            self,
            db_obj,
            obj_in,
            session: AsyncSession,
    ):
        """
        Изменяет объект модели в БД.
        """
        obj_data = jsonable_encoder(db_obj)
        update_data = obj_in.dict(exclude_unset=True)

        for field in obj_data:
            if field in update_data:
                setattr(db_obj, field, update_data[field])
        session.add(db_obj)
        await session.commit()
        await session.refresh(db_obj)
        return db_obj

    async def remove( # noqa
            self,
            db_obj,
            session: AsyncSession,
    ):
        """
        Удаляет объект модели из БД.
        """
        await session.delete(db_obj)
        await session.commit()
        return db_obj
