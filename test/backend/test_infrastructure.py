"""健康检查、根路由、CORS 等基础设施测试"""
import pytest


class TestHealthCheck:
    """健康检查端点测试"""

    @pytest.mark.asyncio
    async def test_health_endpoint(self, client):
        """/health 应返回 200"""
        resp = await client.get("/health")
        assert resp.status_code == 200
        data = resp.json()
        assert "status" in data
        assert "database" in data
        assert "redis" in data

    @pytest.mark.asyncio
    async def test_root_endpoint(self, client):
        """/ 应返回服务信息"""
        resp = await client.get("/")
        assert resp.status_code == 200
        assert "message" in resp.json()


class TestCORSMiddleware:
    """CORS 中间件测试"""

    @pytest.mark.asyncio
    async def test_cors_headers(self, client):
        """OPTIONS 预检请求应返回 CORS 头"""
        resp = await client.options(
            "/api/auth/login",
            headers={
                "Origin": "http://localhost:5173",
                "Access-Control-Request-Method": "POST",
                "Access-Control-Request-Headers": "Content-Type",
            },
        )
        assert resp.status_code == 200
        assert "access-control-allow-origin" in {k.lower() for k in resp.headers.keys()}


class TestErrorHandling:
    """错误处理测试"""

    @pytest.mark.asyncio
    async def test_404_nonexistent_route(self, client):
        """不存在的路由应返回 404"""
        resp = await client.get("/api/nonexistent")
        assert resp.status_code == 404

    @pytest.mark.asyncio
    async def test_method_not_allowed(self, client):
        """不支持的 HTTP 方法应返回 405"""
        resp = await client.delete("/api/auth/login")
        assert resp.status_code in [405, 404]


class TestAPIRouting:
    """API 路由注册完整性测试"""

    @pytest.mark.asyncio
    @pytest.mark.parametrize("method,path,expected_status", [
        ("GET", "/api/auth/me", 401),
        ("POST", "/api/auth/register", 422),
        ("POST", "/api/auth/login", 422),
        ("GET", "/api/profiles", 401),
        ("POST", "/api/profiles", 401),
        ("GET", "/api/diagnoses", 401),
        ("GET", "/api/diagnoses/latest", 401),
        ("POST", "/api/diagnoses", 401),
        ("GET", "/api/plans", 401),
        ("POST", "/api/plans/generate", 401),
        ("GET", "/api/starmap", 401),
        ("GET", "/api/simulations", 401),
        ("POST", "/api/simulations", 401),
    ])
    async def test_api_routes_registered(self, client, method, path, expected_status):
        """所有 API 路由应正确注册"""
        if method == "GET":
            resp = await client.get(path)
        else:
            resp = await client.post(path, json={})
        assert resp.status_code == expected_status, f"{method} {path}: expected {expected_status}, got {resp.status_code}"
