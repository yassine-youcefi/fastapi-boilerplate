import logging

from app.config.config import settings as app_settings
from app.integrations.database import AsyncSessionLocal
from app.integrations.redis_cache import RedisCache
from app.integrations.s3 import AsyncS3Client

logger = logging.getLogger(__name__)


async def get_redis_cache() -> RedisCache:
    """Dependency that provides the RedisCache instance."""
    if not hasattr(get_redis_cache, "_instance"):
        instance = RedisCache(url=app_settings.REDIS_URI)
        try:
            await instance.connect()
            if not await instance.ping():
                logger.error("Redis connection established but ping failed.")
                raise RuntimeError("Redis ping failed after connection.")
            logger.info("Redis connection established and ping successful.")
        except Exception as e:
            logger.error(f"Failed to connect to Redis: {e}")
            raise RuntimeError("Could not connect to Redis.") from e
        get_redis_cache._instance = instance
    return get_redis_cache._instance


async def get_s3_client():
    """
    Dependency that provides an async S3 client (AsyncS3Client) as an async context manager.
    Usage:
        async def route(s3=Depends(get_s3_client)):
            async with s3 as client:
                ...
    """
    return AsyncS3Client()


def get_settings():
    """Dependency that provides the app settings (for testability/overrides)."""
    return app_settings


async def get_db():
    async with AsyncSessionLocal() as session:
        try:
            yield session
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()
