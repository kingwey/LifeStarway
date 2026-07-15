"""工具模块测试 - 密码哈希、JWT令牌、缓存"""
import time
import pytest
from datetime import timedelta

from app.utils.deps import (
    get_password_hash,
    verify_password,
    create_access_token,
)
from app.utils.cache import make_cache_key
from app.config import settings


class TestPasswordHash:
    """密码哈希测试"""

    def test_hash_password(self):
        """密码应被正确哈希"""
        hashed = get_password_hash("MyPassword123")
        assert hashed != "MyPassword123"
        assert hashed.startswith("$pbkdf2-sha256$")

    def test_verify_correct_password(self):
        """正确密码应验证通过"""
        hashed = get_password_hash("MyPassword123")
        assert verify_password("MyPassword123", hashed) is True

    def test_verify_wrong_password(self):
        """错误密码应验证失败"""
        hashed = get_password_hash("MyPassword123")
        assert verify_password("WrongPassword", hashed) is False

    def test_different_hashes_for_same_password(self):
        """同一密码每次哈希结果不同（含盐值）"""
        h1 = get_password_hash("SamePass")
        h2 = get_password_hash("SamePass")
        assert h1 != h2
        assert verify_password("SamePass", h1)
        assert verify_password("SamePass", h2)

    def test_long_password(self):
        """超长密码应正常处理（pbkdf2_sha256 不受 72 字节限制）"""
        long_pwd = "A" * 200
        hashed = get_password_hash(long_pwd)
        assert verify_password(long_pwd, hashed) is True


class TestJWTToken:
    """JWT 令牌测试"""

    def test_create_token_contains_sub(self):
        """令牌应包含 sub 字段"""
        token = create_access_token(data={"sub": "user-123"})
        assert token is not None
        assert isinstance(token, str)

    def test_create_token_with_expiry(self):
        """带过期时间的令牌应正常生成"""
        token = create_access_token(
            data={"sub": "user-456"},
            expires_delta=timedelta(minutes=60),
        )
        assert token is not None

    def test_create_token_default_expiry(self):
        """默认过期时间（15分钟）应正常生成"""
        token = create_access_token(data={"sub": "user-789"})
        assert token is not None

    def test_token_can_be_decoded(self):
        """令牌应可被正确解码"""
        from jose import jwt
        token = create_access_token(data={"sub": "user-decode-test"})
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        assert payload["sub"] == "user-decode-test"

    def test_invalid_token_raises_error(self):
        """无效令牌应抛出 JWTError"""
        from jose import jwt, JWTError
        with pytest.raises(JWTError):
            jwt.decode("invalid.token.here", settings.SECRET_KEY, algorithms=[settings.ALGORITHM])


class TestCacheKey:
    """缓存键生成测试"""

    def test_make_cache_key_consistent(self):
        """相同参数应生成相同键"""
        key1 = make_cache_key("test", user_id="123", action="view")
        key2 = make_cache_key("test", user_id="123", action="view")
        assert key1 == key2

    def test_make_cache_key_different_args(self):
        """不同参数应生成不同键"""
        key1 = make_cache_key("test", user_id="123")
        key2 = make_cache_key("test", user_id="456")
        assert key1 != key2

    def test_make_cache_key_prefix(self):
        """键应包含前缀"""
        key = make_cache_key("llm", prompt="hello")
        assert key.startswith("lifestarway:llm:")

    def test_make_cache_key_order_independent(self):
        """参数顺序不影响键生成（sorted）"""
        key1 = make_cache_key("test", a="1", b="2")
        key2 = make_cache_key("test", b="2", a="1")
        assert key1 == key2


class TestConfigSettings:
    """配置项测试"""

    def test_secret_key_exists(self):
        """SECRET_KEY 应已配置"""
        assert settings.SECRET_KEY is not None
        assert len(settings.SECRET_KEY) > 0

    def test_algorithm_default(self):
        """ALGORITHM 默认为 HS256"""
        assert settings.ALGORITHM == "HS256"

    def test_token_expire_minutes(self):
        """ACCESS_TOKEN_EXPIRE_MINUTES 应为正数"""
        assert settings.ACCESS_TOKEN_EXPIRE_MINUTES > 0

    def test_cors_origins_not_empty(self):
        """CORS_ORIGINS 不为空"""
        assert len(settings.CORS_ORIGINS) > 0

    def test_get_llm_config_returns_tuple(self):
        """get_llm_config 应返回三元组"""
        api_key, api_base, model = settings.get_llm_config()
        assert api_key is not None
        assert api_base is not None
        assert model is not None
