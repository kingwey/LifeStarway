from pydantic_settings import BaseSettings, SettingsConfigDict
from dotenv import load_dotenv

load_dotenv()

# 各提供商的默认配置
PROVIDER_PRESETS = {
    "dashscope": {
        "api_key_env": "DASHSCOPE_API_KEY",
        "api_base": "https://dashscope.aliyuncs.com/compatible-mode/v1",
        "model": "qwen-plus",
    },
    "doubao": {
        "api_key_env": "DOUBAO_API_KEY",
        "api_base": "https://ark.cn-beijing.volces.com/api/v3",
        "model": "doubao-pro-32k",
    },
    "gemini": {
        "api_key_env": "GEMINI_API_KEY",
        "api_base": "https://generativelanguage.googleapis.com/v1beta/openai",
        "model": "gemini-2.0-flash",
    },
}


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    DATABASE_URL: str = "sqlite:///./lifestarway.db"

    REDIS_URL: str = "redis://localhost:6379/0"

    # LLM 提供商选择: dashscope / doubao / gemini
    LLM_PROVIDER: str = "dashscope"

    # 各提供商 API Key
    DASHSCOPE_API_KEY: str = ""
    DOUBAO_API_KEY: str = ""
    GEMINI_API_KEY: str = ""

    # Tavily 搜索
    TAVILY_API_KEY: str = ""

    # GitHub API Token
    GITHUB_TOKEN: str = ""

    # LLM 连接参数（留空则由 LLM_PROVIDER 自动推导）
    LLM_API_KEY: str = ""
    LLM_API_BASE: str = ""
    LLM_MODEL: str = ""

    CORS_ORIGINS: str = "http://localhost:5173,http://localhost:3000,http://localhost:5175,http://localhost:8080"

    def get_llm_config(self) -> tuple[str, str, str]:
        """返回 (api_key, api_base, model)，支持手动覆盖和自动推导。"""
        # 手动覆盖：三个参数都有值时直接使用
        if self.LLM_API_KEY and self.LLM_API_BASE and self.LLM_MODEL:
            return self.LLM_API_KEY, self.LLM_API_BASE, self.LLM_MODEL

        # 自动推导：根据 LLM_PROVIDER 选择预设
        provider = self.LLM_PROVIDER.lower()
        if provider not in PROVIDER_PRESETS:
            raise ValueError(
                f"不支持的 LLM_PROVIDER: {provider}，可选: {list(PROVIDER_PRESETS.keys())}"
            )

        preset = PROVIDER_PRESETS[provider]
        api_key = getattr(self, preset["api_key_env"]) or self.LLM_API_KEY
        if not api_key:
            raise ValueError(f"未配置 {preset['api_key_env']}，请检查 .env 文件")

        api_base = self.LLM_API_BASE or preset["api_base"]
        model = self.LLM_MODEL or preset["model"]
        return api_key, api_base, model


settings = Settings()
