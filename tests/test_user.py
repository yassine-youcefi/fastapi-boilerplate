import pytest
from fastapi import status


@pytest.mark.asyncio
async def test_get_user_details(async_client):
    # First, create a user
    signup_data = {
        "full_name": "User Details",
        "email": "userdetails@example.com",
        "password": "strongpassword123",
    }
    resp = await async_client.post("/user/auth/signup", json=signup_data)
    if resp.status_code != status.HTTP_201_CREATED:
        print("Signup error:", resp.text)
    assert resp.status_code == status.HTTP_201_CREATED
    user_id = resp.json()["user"]["id"]

    # Get user details
    resp = await async_client.get(f"/user/details/{user_id}")
    assert resp.status_code == status.HTTP_200_OK
    data = resp.json()
    assert data["email"] == signup_data["email"]
