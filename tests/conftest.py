import pytest
from sqlalchemy.ext.asyncio import create_async_engine

from app.config.config import settings


@pytest.fixture(autouse=True, scope="function")
async def clean_db():
    engine = create_async_engine(settings.SQLALCHEMY_DATABASE_URI, future=True)
    async with engine.begin() as conn:
        # Disable FK constraints, truncate, then re-enable (Postgres syntax)
        await conn.execute("TRUNCATE TABLE refresh_tokens, access_tokens, users RESTART IDENTITY CASCADE;")
    await engine.dispose()
    yield
