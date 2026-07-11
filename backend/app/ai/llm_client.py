from openai import AsyncOpenAI, OpenAI
from app.config import settings

client = AsyncOpenAI(
    api_key=settings.LLM_API_KEY,
    base_url=settings.LLM_API_BASE
)

sync_client = OpenAI(
    api_key=settings.LLM_API_KEY,
    base_url=settings.LLM_API_BASE
)

async def call_llm(prompt: str, max_tokens: int = 4096) -> str:
    try:
        response = await client.chat.completions.create(
            model=settings.LLM_MODEL,
            messages=[
                {"role": "system", "content": "你是一位资深职业规划师，精通职业发展路径分析、行业趋势预测、技能成长规划。请严格按照要求的JSON格式输出结果。"},
                {"role": "user", "content": prompt}
            ],
            max_tokens=max_tokens,
            temperature=0.7
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        raise RuntimeError(f"LLM调用失败: {str(e)}")
