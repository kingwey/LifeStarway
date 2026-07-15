"""pytest 公共配置与 fixtures"""
import asyncio
import os
import sys
import uuid
from typing import AsyncGenerator

# 将 backend 目录加入 sys.path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "backend"))

import pytest
import pytest_asyncio
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker

# 在导入 app 之前设置测试环境变量
os.environ.setdefault("SECRET_KEY", "test_secret_key_for_testing_only")
os.environ.setdefault("DATABASE_URL", "sqlite+aiosqlite:///:memory:")
os.environ.setdefault("REDIS_URL", "redis://localhost:6379/0")
os.environ.setdefault("LLM_PROVIDER", "dashscope")
os.environ.setdefault("DASHSCOPE_API_KEY", "test_key")

from app.database import Base, get_db
from app.main import app
from app.models.user import User
from app.utils.deps import get_password_hash, create_access_token


# ── 基础 fixtures ──────────────────────────────────────────────

@pytest.fixture(scope="session")
def event_loop():
    """全局事件循环"""
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture(scope="function")
async def db_engine():
    """每个测试函数使用独立的内存数据库"""
    engine = create_async_engine(
        "sqlite+aiosqlite:///:memory:",
        echo=False,
        connect_args={"check_same_thread": False},
    )
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield engine
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
    await engine.dispose()


@pytest_asyncio.fixture(scope="function")
async def db_session(db_engine) -> AsyncGenerator[AsyncSession, None]:
    """数据库会话"""
    session_factory = async_sessionmaker(db_engine, class_=AsyncSession, expire_on_commit=False)
    async with session_factory() as session:
        yield session


@pytest_asyncio.fixture(scope="function")
async def client(db_engine) -> AsyncGenerator[AsyncSession, None]:
    """HTTP 测试客户端，使用独立内存数据库"""
    session_factory = async_sessionmaker(db_engine, class_=AsyncSession, expire_on_commit=False)

    async def override_get_db():
        async with session_factory() as session:
            yield session

    app.dependency_overrides[get_db] = override_get_db

    # 确保表已创建
    async with db_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac

    app.dependency_overrides.clear()


# ── 认证辅助 fixtures ──────────────────────────────────────────

@pytest_asyncio.fixture
async def test_user(db_session) -> User:
    """创建测试用户"""
    user = User(
        id=uuid.uuid4(),
        email="test@example.com",
        nickname="测试用户",
        hashed_password=get_password_hash("Test123456"),
    )
    db_session.add(user)
    await db_session.commit()
    await db_session.refresh(user)
    return user


@pytest_asyncio.fixture
async def auth_token(test_user) -> str:
    """生成测试用户的 JWT token"""
    return create_access_token(data={"sub": str(test_user.id)})


@pytest_asyncio.fixture
async def auth_client(client, test_user, auth_token) -> AsyncClient:
    """带认证头的 HTTP 客户端"""
    client.headers["Authorization"] = f"Bearer {auth_token}"
    return client
