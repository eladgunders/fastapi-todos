import uuid
from typing import Any
from collections.abc import AsyncGenerator

from fastapi import Depends
from fastapi_users import FastAPIUsers
from fastapi_users.db import SQLAlchemyUserDatabase
from fastapi_users.authentication import AuthenticationBackend, BearerTransport
from sqlalchemy.ext.asyncio import AsyncSession

from app.users.security import get_jwt_strategy
from app.users.manager import UserManager
from app.models.tables import User
from app.core.db import get_async_session


bearer_transport = BearerTransport(tokenUrl='auth/login')

auth_backend = AuthenticationBackend(
    name='jwt',
    transport=bearer_transport,
    get_strategy=get_jwt_strategy,
)


async def get_user_db(session: AsyncSession = Depends(get_async_session)) -> \
        AsyncGenerator[SQLAlchemyUserDatabase, User]:
    yield SQLAlchemyUserDatabase(session, User)


async def get_user_manager(user_db: SQLAlchemyUserDatabase = Depends(get_user_db)) ->\
        AsyncGenerator[UserManager, Any]:
    yield UserManager(user_db)


fast_api_users = FastAPIUsers[User, uuid.UUID](get_user_manager, [auth_backend])

current_logged_user = fast_api_users.current_user(active=True, verified=False, superuser=False)
