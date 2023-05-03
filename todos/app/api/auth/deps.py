from collections.abc import AsyncGenerator
from typing import Any

from fastapi import Depends
from fastapi_users.db import SQLAlchemyUserDatabase
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import Session
from app.core.security import UserManager
from app.models.tables import User


async def get_async_session():
    async with Session() as session:
        yield session


async def get_user_db(session: AsyncSession = Depends(get_async_session)) -> \
        AsyncGenerator[SQLAlchemyUserDatabase, User]:
    yield SQLAlchemyUserDatabase(session, User)


async def get_user_manager(user_db: SQLAlchemyUserDatabase = Depends(get_user_db)) ->\
        AsyncGenerator[UserManager, Any]:
    yield UserManager(user_db)
