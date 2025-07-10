import redis.asyncio as redis
from typing import Any

class RedisCache:
    def __init__(self, url: str):
        self.url = url
        self.redis = None

    async def connect(self):
        self.redis = await redis.from_url(self.url, decode_responses=True)

    async def close(self):
        if self.redis:
            await self.redis.close()

    async def get(self, key: str) -> Any:
        return await self.redis.get(key)

    async def set(self, key: str, value: Any, expire: int = 300):
        await self.redis.set(key, value, ex=expire)

    async def delete(self, key: str):
        await self.redis.delete(key)
