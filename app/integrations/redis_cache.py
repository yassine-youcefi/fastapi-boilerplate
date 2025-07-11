# Redis integration module (migrated from app/utils/redis_cache.py)
# ...existing code from app/utils/redis_cache.py will be moved here...

from typing import Any

import redis.asyncio as redis


class RedisCache:
    def __init__(self, url: str, max_connections: int = 10, timeout: int = 5):
        self.url = url
        self.max_connections = max_connections
        self.timeout = timeout
        self.redis = None
        self._connected = False

    async def connect(self):
        self.redis = await redis.from_url(
            self.url,
            decode_responses=True,
            max_connections=self.max_connections,
            socket_connect_timeout=self.timeout,
            socket_timeout=self.timeout,
        )
        self._connected = True

    async def close(self):
        if self.redis:
            await self.redis.close()
            self._connected = False

    async def get(self, key: str) -> Any:
        return await self.redis.get(key)

    async def set(self, key: str, value: Any, expire: int = 300):
        await self.redis.set(key, value, ex=expire)

    async def delete(self, key: str):
        await self.redis.delete(key)

    async def ping(self) -> bool:
        if self.redis:
            try:
                return await self.redis.ping()
            except Exception:
                return False
        return False

    @property
    def connected(self) -> bool:
        return self._connected
