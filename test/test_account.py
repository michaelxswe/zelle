from httpx import AsyncClient
import pytest

# test creating an account
@pytest.mark.anyio
async def test_create_account(client: AsyncClient):
    res = await client.post(
        "/api/account",
        json={"username": "michael", "password": "1234", "phone": "123456789"},
    )

    assert res.status_code == 201

    res_json = res.json()
    del res_json["created_at"]
    assert res_json == {"id": 1, "username": "michael", "password": "1234", "phone": "123456789", "balance": "0.00"}
