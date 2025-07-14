import pytest
from fastapi import status


@pytest.mark.asyncio
async def test_signup_and_login(async_client):
    # Signup
    signup_data = {
        "full_name": "Test User",
        "email": "testuser@example.com",
        "password": "strongpassword123",
    }
    resp = await async_client.post("/user/auth/signup", json=signup_data)
    assert resp.status_code == status.HTTP_201_CREATED
    data = resp.json()
    assert "access_token" in data
    assert data["user"]["email"] == signup_data["email"]

    # Login
    login_data = {
        "email": signup_data["email"],
        "password": signup_data["password"],
    }
    resp = await async_client.post("/user/auth/login", json=login_data)
    assert resp.status_code == status.HTTP_200_OK
    data = resp.json()
    assert "access_token" in data
    assert data["user"]["email"] == signup_data["email"]
