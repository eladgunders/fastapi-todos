from asyncio import current_task
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, AsyncEngine, \
    async_scoped_session
from sqlalchemy.orm import sessionmaker


class SQLManager:
    engine: AsyncEngine
    local_session: async_scoped_session

    def connect_to_database(self, conn_str: str) -> None:
        print('INFO:     connecting to db.')
        self.engine = create_async_engine(conn_str, echo=True)
        async_session_factory = sessionmaker(bind=self.engine, class_=AsyncSession,
                                             expire_on_commit=False)
        self.local_session = async_scoped_session(async_session_factory, scopefunc=current_task)
        print('INFO:     connected to db.')

    async def close_database_connection(self) -> None:
        print('INFO:     closing connection with db.')
        await self.local_session().close()
        await self.engine.dispose()
        print('INFO:     closed connection with db.')
