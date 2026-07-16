import logging
import time
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.api import routers
from app.database import engine, Base
from app.config import settings

# 日志配置
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)-7s | %(name)s | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger("lifestarway")


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    # Shutdown
    from app.utils.cache import close_redis
    await close_redis()


app = FastAPI(
    title="人生星途 LifeStarway API",
    description="""
    数据沉淀迭代式AI全生命周期职业生涯规划系统后端API。

    ## 核心模块
    - **认证**: 用户注册、登录、JWT Token 管理
    - **人生档案**: 个人信息、教育背景、职业履历、技能矩阵
    - **职业诊断**: AI 驱动的五维度职业健康度评估
    - **规划方案**: 短/中/长期职业规划生成
    - **人生星图**: 职业发展路径可视化
    - **What-If 沙盒**: 假设场景模拟分析
    - **公开信息采集**: GitHub、LinkedIn、博客等来源导入

    ## 使用说明
    1. 先调用 `/api/auth/register` 注册账号
    2. 使用 `/api/auth/login` 获取 access_token
    3. 在请求头中携带 `Authorization: Bearer <token>`
    """,
    version="1.0.0",
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc",
)


# 全局异常处理
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"未处理异常: {exc}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={"code": 500, "message": "服务器内部错误", "detail": str(exc)}
    )


# 纯 ASGI 请求日志中间件（避免 BaseHTTPMiddleware 性能问题）
class LoggingMiddleware:
    def __init__(self, app):
        self.app = app

    async def __call__(self, scope, receive, send):
        if scope["type"] != "http":
            await self.app(scope, receive, send)
            return

        start_time = time.time()
        method = scope.get("method", "")
        path = scope.get("path", "")

        status_code = 200

        async def wrapped_send(message):
            nonlocal status_code
            if message["type"] == "http.response.start":
                status_code = message.get("status", 200)
            await send(message)

        try:
            await self.app(scope, receive, wrapped_send)
        except Exception as exc:
            logger.error(f"{method} {path} - 500 - 异常: {exc}")
            raise
        finally:
            duration_ms = (time.time() - start_time) * 1000
            level = logging.WARNING if status_code >= 400 else logging.INFO
            logger.log(level, f"{method} {path} - {status_code} - {duration_ms:.0f}ms")


app.add_middleware(LoggingMiddleware)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[origin.strip() for origin in settings.CORS_ORIGINS.split(",")],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

for router in routers:
    app.include_router(router, prefix="/api")


@app.get("/")
async def root():
    return {"message": "人生星途 API 服务运行中"}


@app.get("/health")
async def health_check():
    checks = {"status": "healthy", "database": "ok", "redis": "unknown"}

    # 检查 Redis 连接
    try:
        from app.utils.cache import get_redis
        r = await get_redis()
        await r.ping()
        checks["redis"] = "ok"
    except Exception as e:
        checks["redis"] = f"error: {e}"
        checks["status"] = "degraded"

    return checks


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
