import uuid
from typing import Optional
from fastapi import Request
from fastapi_users import BaseUserManager, UUIDIDMixin
from fastapi_users.authentication import AuthenticationBackend, JWTStrategy, BearerTransport
from fastapi_users.jwt import SecretType, generate_jwt

from app.core.config import get_config
from app.constants.auth import JWT_HASHING_ALGORITHM
from app.models.tables import User


config = get_config()


class UserManager(UUIDIDMixin, BaseUserManager[User, uuid.UUID]):
    reset_password_token_secret = config.jwt_secret_key
    verification_token_secret = config.jwt_secret_key

    async def on_after_register(self, user: User, request: Optional[Request] = None):
        print(f'User {user.id} has registered.')

    async def on_after_forgot_password(
            self, user: User, token: str, request: Optional[Request] = None
    ):
        print(f'User {user.id} has forgot their password. Reset token: {token}')

    async def on_after_request_verify(
            self, user: User, token: str, request: Optional[Request] = None
    ):
        print(f'Verification requested for user {user.id}. Verification token: {token}')


class TodosJWTStrategy(JWTStrategy):
    def __init__(
            self,
            secret: SecretType,
            lifetime_seconds: Optional[int],
            token_audience=None,
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

    def generate_jwt_data(self, user: User):
        return dict(user_id=str(user.id),
                    aud=self.token_audience,
                    email=user.email,
                    isSuperuser=user.is_superuser)


def get_jwt_strategy() -> JWTStrategy:
    return TodosJWTStrategy(
        secret=config.jwt_secret_key,
        lifetime_seconds=config.jwt_lifetime_seconds
    )


bearer_transport = BearerTransport(tokenUrl='auth/login')


auth_backend = AuthenticationBackend(
    name='jwt',
    transport=bearer_transport,
    get_strategy=get_jwt_strategy,
)
