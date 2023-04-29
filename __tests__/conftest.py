import asyncio

import pytest_asyncio
from asgi_lifespan import LifespanManager
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncConnection, AsyncSession

from app.api.auth.deps import get_async_session
from app.core.config import get_config
from app.core.db import engine
from main import app


config = get_config()


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
        'username': 'user@todos.com',
        'password': 'password',
    }
    res = await client.post('/auth/login', data=login_data)
    print(res)
    access_token = res.json()["access_token"]
    return {"Authorization": f"Bearer {access_token}"}
