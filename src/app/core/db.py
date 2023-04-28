from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, AsyncEngine
from sqlalchemy.orm import sessionmaker

from app.core.config import get_config
from app.models.tables import Base

config = get_config()

engine: AsyncEngine = create_async_engine(config.db_conn_str, echo=True)

Session = sessionmaker(bind=engine, class_=AsyncSession, autoflush=True, expire_on_commit=False,
                       autocommit=False)


# creates a table to all classes that inherits from Base
async def create_all_entities():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
