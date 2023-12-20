from httpx import AsyncClient
from main import app
import pytest

base_url = "http://test"


@pytest.mark.asyncio
async def test_invalid_username():
    async with AsyncClient(app=app, base_url=base_url) as client:
        response = await client.post(
            "/api/accounts",
            json={"username": "mike", "password": "mike", "test": "test"},
        )

        assert response.status_code == 400


@pytest.mark.asyncio
async def test_invalid_token():
    async with AsyncClient(app=app, base_url=base_url) as client:
        response = await client.get(
            "/api/accounts",
            headers={"Authorization": "Bearer 123"},
        )

        assert response.status_code == 401
