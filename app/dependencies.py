from app.config.config import settings
from app.utils.redis_cache import RedisCache


def get_redis_cache() -> RedisCache:
    """Dependency that provides the RedisCache instance."""
    # You may want to use a singleton/global instance, or manage via app state
    # Here, we use a global instance for simplicity
    if not hasattr(get_redis_cache, "_instance"):
        get_redis_cache._instance = RedisCache(url=settings.REDIS_URI)
    return get_redis_cache._instance
