import uuid
from asyncio import current_task
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, AsyncEngine, \
    async_scoped_session
from sqlalchemy.engine.result import Result
from sqlalchemy import select, or_
from sqlalchemy.orm import sessionmaker
from typing import Optional, Any

from app.types.category import Category as CategoryT
from app.models.tables import Category


class SQLManager:
    _engine: AsyncEngine
    _local_session: async_scoped_session

    def connect_to_database(self, conn_str: str) -> None:
        print('INFO:     connecting to db.')
        self._engine = create_async_engine(conn_str, echo=True)
        async_session_factory = sessionmaker(bind=self._engine, class_=AsyncSession,
                                             expire_on_commit=False)
        self._local_session = async_scoped_session(async_session_factory, scopefunc=current_task)
        print('INFO:     connected to db.')

    async def close_database_connection(self) -> None:
        print('INFO:     closing connection with db.')
        await self._local_session().close()
        await self._engine.dispose()
        print('INFO:     closed connection with db.')

    async def _read_from_db(self, query) -> Result:
        query_result: Result = await self._local_session.execute(query)
        await self._local_session.commit()
        return query_result

    async def get_categories(self, user_id: Optional[uuid.UUID]) -> list[CategoryT]:
        query_filter: Any
        default_categories_filter = Category.created_by_id.is_(None)
        if user_id:
            user_categories_filter = Category.created_by_id == user_id
            query_filter = or_(user_categories_filter, default_categories_filter)
        else:
            query_filter = default_categories_filter
        query = select(Category).filter(query_filter)
        categories: list[tuple[Category]] = (await self._read_from_db(query)).all()
        return [category.get_dict() for (category,) in categories]
