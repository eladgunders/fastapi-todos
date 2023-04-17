import threading

from app.db.sql_manager import SQLManager
from config import get_config


class DBFacade:
    _instance = None
    _lock = threading.Lock()
    _repo: SQLManager

    def __init__(self):
        raise RuntimeError('Call get_instance() instead')

    @classmethod
    def get_instance(cls):
        if cls._instance:
            return cls._instance
        with cls._lock:
            if cls._instance is None:
                cls._instance = cls.__new__(cls)
                cls._instance.config = get_config()
                cls._instance.repo = SQLManager()
                cls._instance.repo.connect_to_database(cls._instance.config.db_conn_str)
            return cls._instance

    async def disconnect_from_databases(self) -> None:
        await self._repo.close_database_connection()
