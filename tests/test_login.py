from fastapi import status
from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


def test_invalid_credentials():
    response = client.post(
        "/api/login",
        json={
            "username": "test",
            "password": "test",
        },
    )

    assert response.status_code == status.HTTP_401_UNAUTHORIZED
