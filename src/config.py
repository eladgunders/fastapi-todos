import os
from functools import lru_cache
from dotenv import load_dotenv
from pydantic import BaseSettings

from app.constants.auth import JWT_TOKEN_LIFETIME_SECONDS, JWT_HASHING_ALGORITHM


class Config(BaseSettings):
    db_conn_str: str
    origins: str
    jwt_secret_key: str
    jwt_token_lifetime_seconds: int

    class Config:
        load_dotenv()

        db_conn_str: str = os.environ['DB_CONN_STR']
        origins: list[str] = os.environ['ORIGINS'].split(';')
        jwt_secret_key: str = os.environ['JWT_SECRET_KEY']
        try:
            jwt_token_lifetime_seconds = int(os.getenv('JWT_TOKEN_LIFETIME_SECONDS', JWT_TOKEN_LIFETIME_SECONDS))
        except ValueError:
            jwt_token_lifetime_seconds = JWT_TOKEN_LIFETIME_SECONDS


@lru_cache()
def get_config():
    return Config()
