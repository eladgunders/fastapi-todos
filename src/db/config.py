from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, AsyncEngine
from sqlalchemy.orm import sessionmaker

from config import get_config
from db.tables import Base

config = get_config()
connection_string = config.db_conn_str

engine: AsyncEngine = create_async_engine(connection_string, echo=True)

Session = sessionmaker(bind=engine, class_=AsyncSession, autoflush=True, expire_on_commit=False,
                       autocommit=False)


# creates a table to all classes that inherits from Base
async def create_all_entities():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
