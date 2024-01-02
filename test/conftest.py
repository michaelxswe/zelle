from fastapi import FastAPI
from httpx import AsyncClient
from main import create_app, lifespan
from pytest import fixture
import pytest

# required fixture for async testing
@pytest.fixture(scope="session")
def anyio_backend():
    return "asyncio"

# make sure to be in test environment
@fixture(scope="session")
async def app():
    app = create_app()
    await app.state.database_client.create_tables() #create all the tabes for testing
    yield app
    await app.state.database_client.drop_tables() #tear down


@pytest.fixture(scope="session")
async def client(app: FastAPI):
    async with lifespan(app): #test start up event as well
        async with AsyncClient(app=app, base_url="http://localhost") as client:
            yield client
