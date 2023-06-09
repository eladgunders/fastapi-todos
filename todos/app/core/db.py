from collections.abc import AsyncGenerator
from typing import Any

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, AsyncEngine
from sqlalchemy.orm import sessionmaker

from app.core.config import get_config

config = get_config()

engine: AsyncEngine = create_async_engine(config.POSTGRES_URI, echo=True)

Session = sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)


async def get_async_session() -> AsyncGenerator[AsyncSession, Any]:
    async with Session() as session:
        yield session
