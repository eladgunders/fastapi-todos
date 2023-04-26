import threading
from typing import Optional
import uuid
from sqlalchemy.exc import IntegrityError

from app.dao.sql_manager import SQLManager
from app.models.tables import Priority, Category, Todo
from app.schemas import CategoryInDB, TodoInDB
from app.core.config import get_config
from app.utils.exceptions import ResourceNotExists, Forbidden


class DBFacade:
    _instance = None
    _lock = threading.Lock()

    def __init__(self):
        raise RuntimeError('Call get_instance() instead')

    def __new__(cls):
        instance = super().__new__(cls)
        config = get_config()
        instance._repo = SQLManager()
        instance._repo.connect_to_database(config.db_conn_str)
        return instance

    @classmethod
    def get_instance(cls):
        if cls._instance:
            return cls._instance
        with cls._lock:
            if cls._instance is None:
                cls._instance = cls.__new__(cls)
            return cls._instance

    async def disconnect_from_databases(self) -> None:
        await self._repo.close_database_connection()

    async def get_priorities(self) -> list[Priority]:
        return await self._repo.get_priorities()

    async def get_categories(
            self,
            created_by_id: uuid.UUID,
            categories_ids: Optional[list[int]] = None
    ) -> list[Category]:
        return await self._repo.get_categories(created_by_id, categories_ids)

    async def add_category(self, category: CategoryInDB) -> Category:
        # TODO: replace ValueError with ResourceAlreadyExists and handle it in exception_handler
        users_categories: list[Category] = await self.get_categories(category.created_by_id)
        users_categories_names: list[str] = [c.name for c in users_categories]
        if category.name in users_categories_names:
            raise ValueError('category name already exists')
        return await self._repo.add_category(category)

    async def delete_category(self, category_id: int, created_by_id: uuid.UUID) -> None:
        category: Optional[Category] = await self._repo.get_category(category_id)
        if not category:
            raise ResourceNotExists('category does not exist')
        if category.created_by_id != created_by_id:
            raise Forbidden('a user can not delete a category that was not created by him')
        await self._repo.delete_category(category_id)

    async def get_todos(self, created_by_id: uuid.UUID) -> list[Todo]:
        return await self._repo.get_todos(created_by_id)

    async def add_todo(self, todo: TodoInDB) -> Todo:
        todo_categories_ids: list[int] = todo.categories_ids
        todo_categories_from_db: list[Category] = await self.get_categories(todo.created_by_id, todo_categories_ids)
        are_categories_valid: bool = len(todo_categories_ids) == len(todo_categories_from_db)
        if are_categories_valid:
            try:
                return await self._repo.add_todo(todo)
            except IntegrityError:
                raise ValueError('priority is not valid')
        raise ValueError('categories are not valid')
