from functools import lru_cache
from typing import Any, Optional

from pydantic import BaseSettings, PostgresDsn, AnyHttpUrl, validator, SecretStr


class Settings(BaseSettings):

    JWT_SECRET_KEY: SecretStr

    # 60 seconds by 60 minutes (1 hour) and then by 12 (for 12 hours total)
    JWT_LIFETIME_SECONDS: int = 60 * 60 * 12

    # CORS_ORIGINS is a string of ';' separated origins.
    # e.g:  'http://localhost:8080;http://localhost:3000'
    CORS_ORIGINS: list[AnyHttpUrl]

    POSTGRES_DB: str
    POSTGRES_HOST: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: SecretStr
    POSTGRES_URI: Optional[PostgresDsn] = None

    @validator('POSTGRES_URI', pre=True)
    def assemble_db_connection(cls, _: str, values: dict[str, Any]) -> str:
        postgres_password: SecretStr = values.get('POSTGRES_PASSWORD', SecretStr(''))
        return PostgresDsn.build(
            scheme='postgresql+asyncpg',
            user=values.get('POSTGRES_USER'),
            password=postgres_password.get_secret_value(),
            host=values.get('POSTGRES_HOST'),
            path=f'/{values.get("POSTGRES_DB")}',
        )

    class Config:
        env_file = '.env'
        case_sensitive = True

        @classmethod
        def parse_env_var(cls, field_name: str, raw_val: str) -> Any:
            if field_name == 'CORS_ORIGINS':
                return [origin for origin in raw_val.split(';')]
            # The following line is ignored by mypy because:
            # error: Type'[Config]' has no attribute 'json_loads',
            # even though it is like the documentation: https://docs.pydantic.dev/latest/usage/settings/
            return cls.json_loads(raw_val)  # type: ignore[attr-defined]


@lru_cache()
def get_config() -> Settings:
    # TODO: remove 'type: ignore[call-arg]' once https://github.com/pydantic/pydantic/issues/3072 is closed
    return Settings()  # type: ignore[call-arg]
