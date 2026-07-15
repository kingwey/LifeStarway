import json
import logging
from typing import Optional

import redis.asyncio as redis

from app.config import settings

logger = logging.getLogger("lifestarway.cache")

_redis: Optional[redis.Redis] = None


async def get_redis() -> redis.Redis:
    global _redis
    if _redis is None:
        _redis = redis.from_url(
            settings.REDIS_URL,
            decode_responses=True,
            socket_connect_timeout=5,
        )
    return _redis


async def close_redis():
    global _redis
    if _redis:
        await _redis.close()
        _redis = None


async def cache_get(key: str) -> Optional[str]:
    try:
        r = await get_redis()
        return await r.get(key)
    except Exception as e:
        logger.warning(f"缓存读取失败: {e}")
        return None


async def cache_set(key: str, value: str, ttl: int = 3600) -> None:
    try:
        r = await get_redis()
        await r.setex(key, ttl, value)
    except Exception as e:
        logger.warning(f"缓存写入失败: {e}")


async def cache_delete(key: str) -> None:
    try:
        r = await get_redis()
        await r.delete(key)
    except Exception as e:
        logger.warning(f"缓存删除失败: {e}")


def make_cache_key(prefix: str, **kwargs) -> str:
    sorted_items = sorted(kwargs.items())
    params = "&".join(f"{k}={v}" for k, v in sorted_items)
    return f"lifestarway:{prefix}:{params}"
