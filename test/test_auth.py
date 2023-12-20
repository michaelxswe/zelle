from httpx import AsyncClient
from main import app
import pytest

base_url = "http://test"


@pytest.mark.asyncio
async def test_invalid_credentials():
    async with AsyncClient(app=app, base_url=base_url) as client:
        response = await client.post(
            "/api/auth/sign-in",
            json={
                "username": "test",
                "password": "test",
            },
        )

        assert response.status_code == 401
