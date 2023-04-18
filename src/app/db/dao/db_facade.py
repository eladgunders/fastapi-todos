import threading
from typing import Optional
import uuid

from app.db.dao.sql_manager import SQLManager
from app.db.types.category import CategoryType
from config import get_config


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

    async def get_categories(self, user_id: Optional[uuid.UUID]) -> list[CategoryType]:
        return await self._repo.get_categories(user_id)
