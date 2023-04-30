import asyncio
import json
from typing import Union

import pytest
import pytest_asyncio
from asgi_lifespan import LifespanManager
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncConnection, AsyncSession

from app.api.auth.deps import get_async_session
from app.core.db import engine
from main import app
from __tests__.constants import TEST_USER_EMAIL, TEST_USER_PASSWORD, INITIAL_DATA_FILE_PATH

with open(INITIAL_DATA_FILE_PATH, 'r') as f:
    initial_data_dict: dict[str, list[dict]] = json.load(f)


@pytest_asyncio.fixture()
async def connection():
    async with engine.begin() as conn:
        yield conn
        await conn.rollback()


@pytest_asyncio.fixture()
async def async_session(connection: AsyncConnection):
    async with AsyncSession(connection, expire_on_commit=False) as async_session_:
        yield async_session_


@pytest_asyncio.fixture(autouse=True)
async def override_dependency(async_session: AsyncSession):
    app.dependency_overrides[get_async_session] = lambda: async_session


@pytest_asyncio.fixture(scope='session', autouse=True)
def event_loop():
    event_loop_policy = asyncio.get_event_loop_policy()
    loop = event_loop_policy.new_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture()
async def client():
    async with AsyncClient(app=app, base_url='http://test') as ac, LifespanManager(app):
        yield ac


@pytest_asyncio.fixture()
async def user_token_headers(client: AsyncClient) -> dict[str, str]:
    login_data = {
        'username': TEST_USER_EMAIL,
        'password': TEST_USER_PASSWORD,
    }
    res = await client.post('/auth/login', data=login_data)
    print(res.json())
    access_token = res.json()['access_token']
    return {'Authorization': f'Bearer {access_token}'}


@pytest.fixture()
def get_initial_priorities() -> list[dict[str, Union[int, str]]]:
    return initial_data_dict['priorities']


@pytest.fixture()
def get_initial_categories() -> list[dict[str, Union[int, str]]]:
    return initial_data_dict['categories']
