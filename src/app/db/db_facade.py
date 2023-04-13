import threading

from app.db.sql_manager import SQLManager
from config import get_config


class DBFacade:
    instance = None
    _lock = threading.Lock()
    repo: SQLManager

    def __init__(self):
        raise RuntimeError('Call get_instance() instead')

    @classmethod
    def get_instance(cls):
        if cls.instance:
            return cls.instance
        with cls._lock:
            if cls.instance is None:
                cls.instance = cls.__new__(cls)
                cls.instance.config = get_config()
                cls.instance.repo = SQLManager()
                cls.instance.repo.connect_to_database(cls.instance.config.db_conn_str)
            return cls.instance

    async def disconnect_from_databases(self) -> None:
        await self.repo.close_database_connection()
