from fastapi import FastAPI
from httpx import AsyncClient
from main import create_app, lifespan
from pytest import fixture
import pytest


# required fixture for async testing
@pytest.fixture(scope="session")
def anyio_backend():
    return "asyncio"


@fixture(scope="session")
async def app():
    app = create_app()
    await app.state.database_client.drop_tables()
    await app.state.database_client.create_tables()
    yield app
    await app.state.database_client.drop_tables()


@pytest.fixture(scope="session")
async def client(app: FastAPI):
    async with lifespan(app):
        async with AsyncClient(app=app, base_url="http://localhost") as client:
            yield client
