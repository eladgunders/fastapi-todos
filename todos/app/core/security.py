import uuid
from typing import Optional, Final, Union

from fastapi_users import BaseUserManager, UUIDIDMixin
from fastapi_users.authentication import AuthenticationBackend, JWTStrategy, BearerTransport
from fastapi_users.jwt import SecretType, generate_jwt

from app.core.config import get_config
from app.models.tables import User


config = get_config()


class UserManager(UUIDIDMixin, BaseUserManager[User, uuid.UUID]):
    reset_password_token_secret = config.JWT_SECRET_KEY
    verification_token_secret = config.JWT_SECRET_KEY


JWT_HASHING_ALGORITHM: Final[str] = 'HS256'


class TodosJWTStrategy(JWTStrategy):
    def __init__(
            self,
            secret: SecretType,
            lifetime_seconds: Optional[int],
            token_audience: Optional[list[str]] = None,
            algorithm: str = JWT_HASHING_ALGORITHM,
            public_key: Optional[SecretType] = None,
    ):
        if token_audience is None:
            token_audience = ['fastapi-users:auth', 'fastapi-users:verify']
        super().__init__(secret=secret, lifetime_seconds=lifetime_seconds,
                         token_audience=token_audience, algorithm=algorithm,
                         public_key=public_key)

    async def write_token(self, user: User) -> str:
        data = self.generate_jwt_data(user)
        return generate_jwt(data, self.encode_key, self.lifetime_seconds, algorithm=self.algorithm)

    def generate_jwt_data(self, user: User) -> dict[str, Union[str, list[str], bool]]:
        return dict(user_id=str(user.id),
                    aud=self.token_audience,
                    email=user.email,
                    isSuperuser=user.is_superuser)


def get_jwt_strategy() -> JWTStrategy:
    return TodosJWTStrategy(
        secret=config.JWT_SECRET_KEY,
        lifetime_seconds=config.JWT_LIFETIME_SECONDS
    )


bearer_transport = BearerTransport(tokenUrl='auth/login')


auth_backend = AuthenticationBackend(
    name='jwt',
    transport=bearer_transport,
    get_strategy=get_jwt_strategy,
)
