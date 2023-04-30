from typing import Optional, Type, TypeVar, Union, overload

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete

from app.models.base import Base
from app.schemas import BaseInDB


ModelType = TypeVar('ModelType', bound=Base)
InDBSchemaType = TypeVar('InDBSchemaType', bound=BaseInDB)


class DBRepo:

    def __init__(self):
        ...

    @overload
    async def get(
        self,
        session: AsyncSession,
        *,
        table_model: Type[ModelType],
        query_filter=None,
        multi=True
    ) -> list[ModelType]:
        ...

    @overload
    async def get(
        self,
        session: AsyncSession,
        *,
        table_model: Type[ModelType],
        query_filter=None,
        multi=False
    ) -> Optional[ModelType]:
        ...

    async def get(
        self,
        session: AsyncSession,
        *,
        table_model: Type[ModelType],
        query_filter=None,
        multi: bool = False
    ) -> Union[Optional[ModelType], list[ModelType]]:
        query = select(table_model)
        if query_filter is not None:
            query = query.filter(query_filter)
        result = await session.execute(query)
        db_objs = result.scalars()
        return db_objs.all() if multi else db_objs.first()

    async def create(
        self,
        session: AsyncSession,
        *,
        obj_to_create: InDBSchemaType
    ) -> ModelType:
        db_obj: ModelType = obj_to_create.to_orm()
        session.add(db_obj)
        await session.commit()
        await session.refresh(db_obj)
        return db_obj

    async def delete(
        self,
        session: AsyncSession,
        *,
        table_model: Type[ModelType],
        id_to_delete: int
    ) -> None:
        query = delete(table_model).where(table_model.id == id_to_delete)
        await session.execute(query)
        await session.commit()
