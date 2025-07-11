import logging

from app.config.config import settings
from app.integrations.database import AsyncSessionLocal
from app.integrations.redis_cache import RedisCache

logger = logging.getLogger(__name__)


async def get_redis_cache() -> RedisCache:
    """Dependency that provides the RedisCache instance."""
    if not hasattr(get_redis_cache, "_instance"):
        instance = RedisCache(url=settings.REDIS_URI)
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


async def get_db():
    async with AsyncSessionLocal() as session:
        try:
            yield session
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()
