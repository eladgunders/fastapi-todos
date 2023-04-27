import uuid
from asyncio import current_task
from typing import Optional, Type, TypeVar

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, AsyncEngine, \
    async_scoped_session
from sqlalchemy.engine.result import Result
from sqlalchemy.orm import sessionmaker
from sqlalchemy import select, delete, or_, and_

from app.models.base import Base
from app.models.tables import Category, Priority, Todo
from app.schemas import CategoryInDB, TodoInDB


ModelType = TypeVar("ModelType", bound=Base)


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

    async def _get_by_id(self, item_id: int, model: Type[ModelType]) -> Optional[ModelType]:
        query_filter = model.id == item_id
        query = select(model).filter(query_filter)
        item = await self._read_from_db(query)
        return item.scalars().first()

    async def _add_one(self, item: ModelType) -> ModelType:
        self._local_session.add(item)
        await self._local_session.commit()
        await self._local_session.refresh(item)
        return item

    async def _delete_by_id(self, item_id: int, model: Type[ModelType]) -> None:
        query = delete(model).where(model.id == item_id)
        await self._local_session.execute(query)
        await self._local_session.commit()

    async def get_priorities(self) -> list[Priority]:
        query = select(Priority)
        priorities = await self._read_from_db(query)
        return priorities.scalars().all()

    async def get_category(self, category_id: int) -> Optional[Category]:
        return await self._get_by_id(category_id, Category)

    async def get_categories(
            self,
            created_by_id: uuid.UUID,
            categories_ids: Optional[list[int]] = None
    ) -> list[Category]:
        default_categories_filter = Category.created_by_id.is_(None)
        user_categories_filter = Category.created_by_id == created_by_id
        query_filter = or_(user_categories_filter, default_categories_filter)
        if categories_ids:
            categories_ids_filter = Category.id.in_(categories_ids)
            query_filter = and_(query_filter, categories_ids_filter)
        query = select(Category).filter(query_filter)
        categories = await self._read_from_db(query)
        return categories.scalars().all()

    async def add_category(self, category: CategoryInDB) -> Category:
        return await self._add_one(category.to_orm())

    async def delete_category(self, category_id: int) -> None:
        await self._delete_by_id(category_id, Category)

    async def get_todo(self, todo_id: int) -> Optional[Todo]:
        return await self._get_by_id(todo_id, Todo)

    async def get_todos(self, created_by_id: uuid.UUID) -> list[Todo]:
        query_filter = Todo.created_by_id == created_by_id
        query = select(Todo).filter(query_filter)
        todos = await self._read_from_db(query)
        return todos.scalars().all()

    async def add_todo(self, todo: TodoInDB) -> Todo:
        return await self._add_one(todo.to_orm())

    async def delete_todo(self, todo_id: int) -> None:
        await self._delete_by_id(todo_id, Todo)
