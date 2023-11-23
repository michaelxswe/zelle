from fastapi import status
from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


def test_invalid_username():
    response = client.post(
        "/api/users",
        json={"username": "mike", "password": "mike", "phone": "9175205546"},
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST


def test_invalid_token():
    response = client.get(
        "/api/users",
        headers={"Authorization": "Bearer 123"},
    )

    assert response.status_code == status.HTTP_401_UNAUTHORIZED
