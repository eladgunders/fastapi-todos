import uuid
from asyncio import current_task
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, AsyncEngine, \
    async_scoped_session
from sqlalchemy.engine.result import Result
from sqlalchemy import select, delete, or_
from sqlalchemy.orm import sessionmaker, selectinload
from typing import Optional, Any, Type, TypeVar

from app.models.base import Base
from app.models.tables import Category, Priority, Todo, TodoCategory
from app.schemas.category import CategoryIn
from app.schemas.todo import TodoIn


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

    async def _add_one(self, item: ModelType) -> ModelType:
        self._local_session.add(item)
        await self._local_session.commit()
        return item

    async def _delete_by_id(self, item_id: int, model: Type[ModelType]) -> None:
        query = delete(model).where(model.id == item_id)
        await self._local_session.execute(query)
        await self._local_session.commit()

    async def get_priorities(self) -> list[Priority]:
        query = select(Priority)
        priorities = await self._read_from_db(query)
        return priorities.scalars().all()

    async def get_categories(self, created_by_id: Optional[uuid.UUID]) -> list[Category]:
        query_filter: Any
        default_categories_filter = Category.created_by_id.is_(None)
        if created_by_id:
            user_categories_filter = Category.created_by_id == created_by_id
            query_filter = or_(user_categories_filter, default_categories_filter)
        else:
            query_filter = default_categories_filter
        query = select(Category).filter(query_filter)
        categories = await self._read_from_db(query)
        return categories.scalars().all()

    async def get_category(self, category_id: int) -> Optional[Category]:
        query_filter = Category.id == category_id
        query = select(Category).filter(query_filter)
        category = await self._read_from_db(query)
        return category.scalars().first()

    async def add_category(self, category: CategoryIn) -> Category:
        category_data = dict(category)
        category_obj = Category(**category_data)
        return await self._add_one(category_obj)

    async def delete_category(self, category_id: int) -> None:
        await self._delete_by_id(category_id, Category)

    async def get_todos(self, created_by_id: uuid.UUID) -> list[Todo]:
        query_filter = Todo.created_by_id == created_by_id
        query = select(Todo).filter(query_filter).options(
            selectinload(Todo.priority),
            selectinload(Todo.todos_categories).selectinload(TodoCategory.category)
        )
        todos = await self._read_from_db(query)
        return todos.scalars().all()

    # async def add_todo(self, todo: TodoIn, categories: list[int]) -> None:
    #     await self._add_one(todo, Todo)

