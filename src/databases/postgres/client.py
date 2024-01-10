from databases.postgres.models import Base
from fastapi import Request
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine


class DatabaseClient:
    def __init__(self, url: str):
        self.engine = create_async_engine(url=url)
        self.Session = async_sessionmaker(self.engine)

    async def create_tables(self):
        async with self.engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

    async def drop_tables(self):
        async with self.engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)

    async def shutdown_database(self):
        await self.engine.dispose()


async def get_database_client(request: Request) -> DatabaseClient:
    return request.app.state.database_client


async def get_database_session(request: Request):
    async with request.app.state.database_client.Session() as session:
        yield session
