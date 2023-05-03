from typing import Optional, Type, TypeVar, Union, Any

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete

from app.models.base import Base
from app.schemas.base import BaseInDB, BaseUpdateInDB
from app.dal.constants import GET_MULTI_DEFAULT_SKIP


ModelType = TypeVar('ModelType', bound=Base)
InDBSchemaType = TypeVar('InDBSchemaType', bound=BaseInDB)


class DBRepo:

    def __init__(self):
        ...

    async def get(
        self,
        session: AsyncSession,
        *,
        table_model: Type[ModelType],
        query_filter: Optional = None
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
        query_filter: Optional = None,
        skip: int = GET_MULTI_DEFAULT_SKIP,
        limit: Optional[int] = None
    ) -> list[ModelType]:
        query = select(table_model)
        if query_filter is not None:
            query = query.filter(query_filter)
        query = query.offset(skip)
        if limit is not None:
            query = query.limit(limit)
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

    async def update(
        self,
        session: AsyncSession,
        *,
        updated_obj: BaseUpdateInDB
    ) -> ModelType:
        db_obj_to_update: Optional[ModelType] = await self.get(
            session,
            table_model=updated_obj.Config.orm_model,
            query_filter=updated_obj.Config.orm_model.id == updated_obj.id
        )
        obj_to_update_data = db_obj_to_update.dict()
        updated_data: dict[str, Any] = updated_obj.to_orm().dict()
        for field in obj_to_update_data:
            if field in updated_data:
                setattr(db_obj_to_update, field, updated_data[field])
        session.add(db_obj_to_update)
        await session.commit()
        await session.refresh(db_obj_to_update)
        return db_obj_to_update

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
