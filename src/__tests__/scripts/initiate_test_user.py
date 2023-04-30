import asyncio
import contextlib

from fastapi_users.exceptions import UserAlreadyExists

from app.api.auth.deps import get_async_session, get_user_db, get_user_manager
from app.schemas import UserCreate
from __tests__.constants import TEST_USER_EMAIL, TEST_USER_PASSWORD


get_async_session_context = contextlib.asynccontextmanager(get_async_session)
get_user_db_context = contextlib.asynccontextmanager(get_user_db)
get_user_manager_context = contextlib.asynccontextmanager(get_user_manager)


async def create_user(email: str, password: str = None) -> None:
    try:
        async with get_async_session_context() as session:
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
        email=TEST_USER_EMAIL,
        password=TEST_USER_PASSWORD
    ))
