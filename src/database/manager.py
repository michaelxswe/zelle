from config import Settings
from fastapi import Request
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from database.model import Base


class DatabaseManager:
    def __init__(self, settings: Settings):
        self.engine = create_async_engine(url=settings.DATABASE_URL, echo=True)
        self.Session = async_sessionmaker(self.engine)

    async def create_all(self):
        async with self.engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

    async def drop_all(self):
        async with self.engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)

    async def shutdown(self):
        await self.engine.dispose()


async def get_database_manager(request: Request):
    return request.app.state.database_manager


async def get_session(request: Request):
    async with request.app.state.database_manager.Session() as session:
        yield session
