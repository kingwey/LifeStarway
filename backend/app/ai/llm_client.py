import asyncio
import hashlib
import logging

from openai import AsyncOpenAI, OpenAI
from app.config import settings

logger = logging.getLogger("lifestarway.llm")

# 根据配置自动推导 API Key、Base URL 和模型
_api_key, _api_base, _model = settings.get_llm_config()

client = AsyncOpenAI(
    api_key=_api_key,
    base_url=_api_base,
    timeout=30.0,
    max_retries=2,
)

sync_client = OpenAI(
    api_key=_api_key,
    base_url=_api_base,
    timeout=30.0,
    max_retries=2,
)

LLM_RETRIES = 3
LLM_RETRY_DELAY = 1.0  # 秒
LLM_CACHE_TTL = 3600  # 缓存 1 小时

SYSTEM_PROMPT = "你是一位资深职业规划师，精通职业发展路径分析、行业趋势预测、技能成长规划。请严格按照要求的JSON格式输出结果。"


def _cache_key(prompt: str) -> str:
    h = hashlib.md5(prompt.encode()).hexdigest()
    return f"lifestarway:llm:{h}"


async def call_llm(prompt: str, max_tokens: int = 4096, use_cache: bool = True) -> str:
    # 尝试从缓存读取
    if use_cache:
        try:
            from app.utils.cache import cache_get, cache_set
            cached = await cache_get(_cache_key(prompt))
            if cached:
                logger.info("LLM缓存命中")
                return cached
        except Exception:
            pass  # Redis 不可用时降级为无缓存

    last_error = None
    for attempt in range(1, LLM_RETRIES + 1):
        try:
            response = await client.chat.completions.create(
                model=_model,
                messages=[
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=max_tokens,
                temperature=0.7
            )
            result = response.choices[0].message.content.strip()

            # 写入缓存
            if use_cache:
                try:
                    from app.utils.cache import cache_set
                    await cache_set(_cache_key(prompt), result, LLM_CACHE_TTL)
                except Exception:
                    pass

            return result
        except Exception as e:
            last_error = e
            logger.warning(f"LLM调用第{attempt}次失败: {e}")
            if attempt < LLM_RETRIES:
                await asyncio.sleep(LLM_RETRY_DELAY * attempt)
    raise RuntimeError(f"LLM调用失败(重试{LLM_RETRIES}次): {str(last_error)}")
