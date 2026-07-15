"""认证模块测试 - 注册、登录、获取当前用户"""
import uuid

import pytest


class TestRegister:
    """用户注册测试"""

    @pytest.mark.asyncio
    async def test_register_success(self, client):
        """正常注册"""
        resp = await client.post("/api/auth/register", json={
            "email": "newuser@test.com",
            "password": "Pass1234",
            "nickname": "新用户",
        })
        assert resp.status_code == 200
        data = resp.json()
        assert "id" in data
        assert data["email"] == "newuser@test.com"
        assert data["nickname"] == "新用户"

    @pytest.mark.asyncio
    async def test_register_duplicate_email(self, client, test_user):
        """重复邮箱注册应返回 400"""
        resp = await client.post("/api/auth/register", json={
            "email": "test@example.com",
            "password": "Pass1234",
            "nickname": "重复用户",
        })
        assert resp.status_code == 400
        assert "已被注册" in resp.json()["detail"]

    @pytest.mark.asyncio
    async def test_register_missing_fields(self, client):
        """缺少必填字段应返回 422"""
        resp = await client.post("/api/auth/register", json={"email": "a@b.com"})
        assert resp.status_code == 422

    @pytest.mark.asyncio
    async def test_register_invalid_email(self, client):
        """非法邮箱格式应返回 422"""
        resp = await client.post("/api/auth/register", json={
            "email": "not-an-email",
            "password": "Pass1234",
            "nickname": "test",
        })
        assert resp.status_code == 422


class TestLogin:
    """用户登录测试"""

    @pytest.mark.asyncio
    async def test_login_success(self, client, test_user):
        """正常登录"""
        resp = await client.post("/api/auth/login", json={
            "email": "test@example.com",
            "password": "Test123456",
        })
        assert resp.status_code == 200
        data = resp.json()
        assert "access_token" in data
        assert data["token_type"] == "bearer"

    @pytest.mark.asyncio
    async def test_login_wrong_password(self, client, test_user):
        """密码错误应返回 401"""
        resp = await client.post("/api/auth/login", json={
            "email": "test@example.com",
            "password": "WrongPass",
        })
        assert resp.status_code == 401
        assert "密码错误" in resp.json()["detail"]

    @pytest.mark.asyncio
    async def test_login_nonexistent_user(self, client):
        """不存在的用户应返回 401"""
        resp = await client.post("/api/auth/login", json={
            "email": "nobody@test.com",
            "password": "Pass1234",
        })
        assert resp.status_code == 401

    @pytest.mark.asyncio
    async def test_login_missing_fields(self, client):
        """缺少字段应返回 422"""
        resp = await client.post("/api/auth/login", json={"email": "a@b.com"})
        assert resp.status_code == 422


class TestGetCurrentUser:
    """获取当前用户信息测试"""

    @pytest.mark.asyncio
    async def test_get_me_with_valid_token(self, auth_client, test_user):
        """有效 token 获取用户信息"""
        resp = await auth_client.get("/api/auth/me")
        assert resp.status_code == 200
        data = resp.json()
        assert data["email"] == test_user.email
        assert data["nickname"] == test_user.nickname

    @pytest.mark.asyncio
    async def test_get_me_without_token(self, client):
        """无 token 应返回 401"""
        resp = await client.get("/api/auth/me")
        assert resp.status_code == 401

    @pytest.mark.asyncio
    async def test_get_me_with_invalid_token(self, client):
        """无效 token 应返回 401"""
        client.headers["Authorization"] = "Bearer invalid_token_here"
        resp = await client.get("/api/auth/me")
        assert resp.status_code == 401
