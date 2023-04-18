from functools import lru_cache
from pydantic import BaseSettings


class Settings(BaseSettings):
    db_conn_str: str
    origins: str
    jwt_secret_key: str
    jwt_token_lifetime_seconds: int

    class Config:
        env_file = '.env'


@lru_cache()
def get_config():
    return Settings()
