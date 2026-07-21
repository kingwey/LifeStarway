import asyncio
import hashlib
import logging
import random
import time

from openai import AsyncOpenAI
from app.config import settings

logger = logging.getLogger("lifestarway.llm")

# LLM 客户端懒加载：应用启动时不强制要求 API Key，
# 只有真正调用 AI 功能时才初始化。未配置 key 时给出明确错误，
# 不影响服务启动与其它非 AI 功能。
_client: AsyncOpenAI | None = None
_model: str | None = None


def _get_client() -> tuple[AsyncOpenAI, str]:
    global _client, _model
    if _client is None:
        try:
            api_key, api_base, model = settings.get_llm_config()
        except ValueError as e:
            raise RuntimeError(
                f"AI 功能不可用：未配置 LLM API Key（{e}）。"
                f"请在环境变量中设置对应的 API Key 后重试。"
            )
        _client = AsyncOpenAI(
            api_key=api_key,
            base_url=api_base,
            timeout=30.0,
            max_retries=0,
        )
        _model = model
    return _client, _model


LLM_RETRIES = 3
LLM_BASE_DELAY = 1.0
LLM_MAX_DELAY = 16.0
LLM_CACHE_TTL = 3600
LLM_RATE_LIMIT_RPM = 20

SYSTEM_PROMPT = "你是一位资深职业规划师，精通职业发展路径分析、行业趋势预测、技能成长规划。请严格按照要求的JSON格式输出结果。"

# 令牌桶限流
_rate_limit_tokens = LLM_RATE_LIMIT_RPM
_rate_limit_last = time.time()
_rate_lock = asyncio.Lock()


async def _rate_limit_acquire():
    async with _rate_lock:
        global _rate_limit_tokens, _rate_limit_last
        now = time.time()
        elapsed = now - _rate_limit_last
        _rate_limit_tokens = min(LLM_RATE_LIMIT_RPM, _rate_limit_tokens + elapsed * LLM_RATE_LIMIT_RPM / 60)
        _rate_limit_last = now

        if _rate_limit_tokens < 1:
            wait = (1 - _rate_limit_tokens) * 60 / LLM_RATE_LIMIT_RPM
            logger.warning(f"LLM限流触发，等待 {wait:.1f}s")
            await asyncio.sleep(wait)
            _rate_limit_tokens = 0
        else:
            _rate_limit_tokens -= 1


def _cache_key(prompt: str) -> str:
    h = hashlib.md5(prompt.encode()).hexdigest()
    return f"lifestarway:llm:{h}"


def _jittered_delay(base: float, attempt: int) -> float:
    delay = min(base * (2 ** (attempt - 1)), LLM_MAX_DELAY)
    return delay * (0.5 + random.random() * 0.5)


async def call_llm(prompt: str, max_tokens: int = 4096, use_cache: bool = True) -> str:
    if use_cache:
        try:
            from app.utils.cache import cache_get, cache_set
            cached = await cache_get(_cache_key(prompt))
            if cached:
                logger.info("LLM缓存命中")
                return cached
        except Exception:
            pass

    client, model = _get_client()

    await _rate_limit_acquire()
    start = time.time()
    last_error = None

    for attempt in range(1, LLM_RETRIES + 1):
        try:
            response = await client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=max_tokens,
                temperature=0.7
            )
            result = response.choices[0].message.content.strip()

            duration = time.time() - start
            tokens = response.usage.total_tokens if response.usage else 0
            logger.info(f"LLM调用成功 | 耗时: {duration:.2f}s | tokens: {tokens} | model: {model}")

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
                delay = _jittered_delay(LLM_BASE_DELAY, attempt)
                logger.info(f"{delay:.1f}s 后重试...")
                await asyncio.sleep(delay)

    raise RuntimeError(f"LLM调用失败(重试{LLM_RETRIES}次): {str(last_error)}")
