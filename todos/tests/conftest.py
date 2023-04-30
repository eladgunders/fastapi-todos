import asyncio
import json
from typing import Union

import pytest
from httpx import AsyncClient  # pylint: disable=import-error
from asgi_lifespan import LifespanManager  # pylint: disable=import-error
import pytest_asyncio  # pylint: disable=import-error
from sqlalchemy.ext.asyncio import AsyncConnection, AsyncSession

from app.api.auth.deps import get_async_session
from app.core.db import engine
from app.main import app
from tests.constants import TEST_USER_EMAIL, TEST_USER_PASSWORD, TEST_BASE_URL, INITIAL_DATA_FILE_PATH


with open(INITIAL_DATA_FILE_PATH, 'r', encoding='utf-8') as f:
    initial_data: dict[str, list[dict[str, Union[int, str]]]] = json.load(f)


@pytest_asyncio.fixture()
async def connection():
    async with engine.begin() as conn:
        yield conn
        await conn.rollback()


@pytest_asyncio.fixture()
async def async_session(connection: AsyncConnection):  # pylint: disable=redefined-outer-name
    async with AsyncSession(connection, expire_on_commit=False) as async_session_:
        yield async_session_


@pytest_asyncio.fixture(autouse=True)
async def override_dependency(async_session: AsyncSession):  # pylint: disable=redefined-outer-name
    app.dependency_overrides[get_async_session] = lambda: async_session


@pytest_asyncio.fixture(scope='session', autouse=True)
def event_loop():
    event_loop_policy = asyncio.get_event_loop_policy()
    loop = event_loop_policy.new_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture()
async def client():
    async with AsyncClient(app=app, base_url=TEST_BASE_URL) as ac, LifespanManager(app):
        yield ac


@pytest_asyncio.fixture()
async def user_token_headers(client: AsyncClient) -> dict[str, str]:  # pylint: disable=redefined-outer-name
    login_data = {
        'username': TEST_USER_EMAIL,
        'password': TEST_USER_PASSWORD,
    }
    res = await client.post('/auth/login', data=login_data)
    print(res.json())
    access_token = res.json()['access_token']
    return {'Authorization': f'Bearer {access_token}'}


@pytest.fixture()
def initial_priorities() -> list[dict[str, Union[int, str]]]:
    return initial_data['priorities']


@pytest.fixture()
def initial_categories() -> list[dict[str, Union[int, str]]]:
    return initial_data['categories']