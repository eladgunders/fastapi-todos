import asyncio
import contextlib

from sqlalchemy.ext.asyncio import AsyncSession, AsyncConnection
from fastapi_users.db import SQLAlchemyUserDatabase
from fastapi_users.exceptions import UserAlreadyExists

from app.core.db import Session
from app.core.security import UserManager
from app.models.tables import User
from app.api.auth.deps import get_async_session, get_user_db, get_user_manager
from app.schemas import UserCreate


# async def get_async_session():
#     async with Session() as async_session_:
#         yield async_session_
#
#
# async def get_user_db(async_session: AsyncSession):
#     yield SQLAlchemyUserDatabase(async_session, User)
#
#
# async def get_user_manager(user_db: SQLAlchemyUserDatabase):
#     yield UserManager(user_db)


get_async_session_context = contextlib.asynccontextmanager(get_async_session)
get_user_db_context = contextlib.asynccontextmanager(get_user_db)
get_user_manager_context = contextlib.asynccontextmanager(get_user_manager)


async def create_user(email: str, password: str = None) -> None:
    try:
        async with get_async_session_context(conn) as session:
            async with get_user_db_context(session) as user_db:
                async with get_user_manager_context(user_db) as user_manager:
                    await user_manager.create(
                        UserCreate(email=email, password=password)
                    )
    except UserAlreadyExists:
        print('User with {user_name} mail address already exists')


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(create_user(
        email='user@todos.com',
        password='password'
    ))
