import pytest
from fastapi import status
from httpx import AsyncClient

from main import app

base_url = 'http://test'


@pytest.mark.asyncio
async def test_invalid_username():
    async with AsyncClient(app=app, base_url=base_url) as client:
        response = await client.post(
            '/api/users',
            json={'username': 'mike', 'password': 'mike', 'phone': '9175205546'},
        )

        assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.asyncio
async def test_invalid_token():
    async with AsyncClient(app=app, base_url=base_url) as client:
        response = await client.get(
            '/api/users',
            headers={'Authorization': 'Bearer 123'},
        )

        assert response.status_code == status.HTTP_401_UNAUTHORIZED
