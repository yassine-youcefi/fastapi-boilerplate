import os

import pytest
from fastapi import status
from httpx import AsyncClient

from app.main import app


@pytest.mark.asyncio
async def test_get_user_details():
    async with AsyncClient(
        app=app, base_url=os.getenv("BASE_URL", "http://localhost:8000")
    ) as ac:
        # First, create a user
        signup_data = {
            "full_name": "User Details",
            "email": "userdetails@example.com",
            "password": "strongpassword123",
        }
        resp = await ac.post("/user/auth/signup", json=signup_data)
        assert resp.status_code == status.HTTP_201_CREATED
        user_id = resp.json()["user"]["id"]

        # Get user details
        resp = await ac.get(f"/user/details/{user_id}")
        assert resp.status_code == status.HTTP_200_OK
        data = resp.json()
        assert data["email"] == signup_data["email"]
