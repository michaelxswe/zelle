import pytest
from fastapi import status
from fastapi.testclient import TestClient
from httpx import AsyncClient

from main import app

client = TestClient(app)

base_url = "http://test"


@pytest.mark.asyncio
async def test_invalid_credentials():
    async with AsyncClient(app=app, base_url=base_url) as client:
        response = await client.post(
            "/api/login",
            json={
                "username": "test",
                "password": "test",
            },
        )

        assert response.status_code == status.HTTP_401_UNAUTHORIZED
