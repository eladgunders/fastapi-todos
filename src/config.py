from functools import lru_cache
from pydantic import BaseSettings
from typing import Any


class Settings(BaseSettings):
    db_conn_str: str
    origins: list[str]
    jwt_secret_key: str
    jwt_token_lifetime_seconds: int

    class Config:
        env_file = '.env'

        @classmethod
        def parse_env_var(cls, field_name: str, raw_val: str) -> Any:
            if field_name == 'origins':
                return [origin for origin in raw_val.split(';')]
            return cls.json_loads(raw_val)


@lru_cache()
def get_config():
    return Settings()
