import uuid
from typing import Optional
from fastapi import Depends, Request
from fastapi_users import BaseUserManager, FastAPIUsers, UUIDIDMixin
from fastapi_users.authentication import AuthenticationBackend, JWTStrategy, BearerTransport
from fastapi_users.db import SQLAlchemyUserDatabase
from fastapi_users.jwt import SecretType, generate_jwt

from config import get_config
from db.tables import User
from db.user_db import get_user_db

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


async def get_user_manager(user_db: SQLAlchemyUserDatabase = Depends(get_user_db)):
    yield UserManager(user_db)


bearer_transport = BearerTransport(tokenUrl='auth/login')


class TodosJWTStrategy(JWTStrategy):
    def __init__(
            self,
            secret: SecretType,
            lifetime_seconds: Optional[int],
            token_audience=None,
            algorithm: str = 'HS256',
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
        lifetime_seconds=config.jwt_token_lifetime_seconds
    )


auth_backend = AuthenticationBackend(
    name='cookies_with_db',
    transport=bearer_transport,
    get_strategy=get_jwt_strategy,
)

fastapi_users = FastAPIUsers[User, uuid.UUID](get_user_manager, [auth_backend])

current_logged_user = fastapi_users.current_user(active=True, verified=False, superuser=False)
