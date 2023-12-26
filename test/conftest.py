from database.model import Base
from httpx import AsyncClient
from main import app, lifespan
from pytest import fixture
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
import pytest


@pytest.fixture(scope="session")
def anyio_backend():
    return "asyncio"


class Settings:
    def __init__(self):
        self.ENV = "Test"
        self.DATABASE_URL = "postgresql+asyncpg://postgres:0000@localhost:5432/test"
        self.SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
        self.ALGORITHM = "HS256"


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


@fixture(scope="session")
def mock_settings():
    return Settings()


@fixture(scope="session")
async def mock_database_manager(mock_settings: Settings):
    database_manager = DatabaseManager(mock_settings)
    await database_manager.create_all()
    yield database_manager
    await database_manager.drop_all()


@pytest.fixture(scope="session")
async def client(mock_database_manager: DatabaseManager):
    async with lifespan(app):
        original_database_manager = app.state.database_manager
        try:
            app.state.database_manager = mock_database_manager
            async with AsyncClient(app=app, base_url="http://localhost") as client:
                yield client
        finally:
            app.state.database_manager = original_database_manager
