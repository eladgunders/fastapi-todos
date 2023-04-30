from typing import Optional, Type, TypeVar, Union, Final

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete

from app.models.base import Base
from app.schemas import BaseInDB


ModelType = TypeVar('ModelType', bound=Base)
InDBSchemaType = TypeVar('InDBSchemaType', bound=BaseInDB)

GET_MULTI_DEFAULT_SKIP: Final[int] = 0
GET_MULTI_DEFAULT_LIMIT: Final[int] = 100


class DBRepo:

    def __init__(self):
        ...

    async def get(
        self,
        session: AsyncSession,
        *,
        table_model: Type[ModelType],
        query_filter=None
    ) -> Union[Optional[ModelType], list[ModelType]]:
        query = select(table_model)
        if query_filter is not None:
            query = query.filter(query_filter)
        result = await session.execute(query)
        db_objs = result.scalars()
        return db_objs.first()

    async def get_multi(
        self,
        session: AsyncSession,
        *,
        table_model: Type[ModelType],
        query_filter=None,
        skip: int = GET_MULTI_DEFAULT_SKIP,
        limit: int = GET_MULTI_DEFAULT_LIMIT
    ) -> list[ModelType]:
        query = select(table_model)
        if query_filter is not None:
            query = query.filter(query_filter)
        query = query.offset(skip).limit(limit)
        result = await session.execute(query)
        db_objs = result.scalars()
        return db_objs.all()

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
