import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import create_async_engine

from app.config.config import settings
from app.main import app


@pytest.fixture(autouse=True, scope="function")
async def clean_db():
    engine = create_async_engine(settings.ASYNC_TEST_DATABASE_URL, future=True)
    async with engine.begin() as conn:
        # Disable FK constraints, truncate, then re-enable (Postgres syntax)
        await conn.execute("TRUNCATE TABLE refresh_tokens, access_tokens, users RESTART IDENTITY CASCADE;")
    await engine.dispose()
    yield


@pytest.fixture
async def async_client():
    async with AsyncClient(app=app, base_url=settings.BASE_URL) as ac:
        yield ac
