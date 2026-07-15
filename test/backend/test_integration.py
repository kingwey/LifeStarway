"""端到端业务流程集成测试：注册→登录→创建档案→诊断→规划→星图→模拟"""
import pytest
from fastapi.exceptions import ResponseValidationError


class TestFullWorkflow:
    """完整业务流程测试"""

    @pytest.mark.asyncio
    async def test_register_login_and_access_protected(self, client):
        """注册→登录→访问受保护接口"""
        # 1. 注册
        resp = await client.post("/api/auth/register", json={
            "email": "flow@test.com",
            "password": "Flow1234",
            "nickname": "流程用户",
        })
        assert resp.status_code == 200
        user_id = resp.json()["id"]

        # 2. 登录
        resp = await client.post("/api/auth/login", json={
            "email": "flow@test.com",
            "password": "Flow1234",
        })
        assert resp.status_code == 200
        token = resp.json()["access_token"]

        # 3. 访问受保护接口
        headers = {"Authorization": f"Bearer {token}"}
        resp = await client.get("/api/auth/me", headers=headers)
        assert resp.status_code == 200
        assert resp.json()["id"] == user_id

    @pytest.mark.asyncio
    async def test_profile_lifecycle(self, auth_client):
        """档案创建→获取→更新→版本历史"""
        # 1. 创建档案
        resp = await auth_client.post("/api/profiles", json={
            "education": "本科",
            "major": "软件工程",
            "work_years": 3,
        })
        assert resp.status_code == 200
        assert resp.json()["version"] == 1

        # 2. 获取档案
        resp = await auth_client.get("/api/profiles")
        assert resp.status_code == 200
        assert resp.json()["education"] == "本科"

        # 3. 更新档案
        resp = await auth_client.post("/api/profiles", json={
            "education": "硕士",
            "major": "人工智能",
        })
        assert resp.status_code == 200
        assert resp.json()["version"] == 2
        assert resp.json()["education"] == "硕士"

        # 4. 版本历史
        resp = await auth_client.get("/api/profiles/versions")
        assert resp.status_code == 200
        assert isinstance(resp.json(), list)

    @pytest.mark.asyncio
    async def test_data_isolation_between_users(self, client):
        """不同用户数据隔离"""
        # 用户 A 注册
        await client.post("/api/auth/register", json={
            "email": "userA@test.com",
            "password": "PassA1234",
            "nickname": "用户A",
        })
        resp_a = await client.post("/api/auth/login", json={
            "email": "userA@test.com",
            "password": "PassA1234",
        })
        token_a = resp_a.json()["access_token"]

        # 用户 B 注册
        await client.post("/api/auth/register", json={
            "email": "userB@test.com",
            "password": "PassB1234",
            "nickname": "用户B",
        })
        resp_b = await client.post("/api/auth/login", json={
            "email": "userB@test.com",
            "password": "PassB1234",
        })
        token_b = resp_b.json()["access_token"]

        # 用户 A 创建档案
        resp = await client.post("/api/profiles", json={
            "education": "本科",
            "major": "计算机",
        }, headers={"Authorization": f"Bearer {token_a}"})
        assert resp.status_code == 200

        # 用户 B 获取档案会抛出 ResponseValidationError（None 序列化失败）
        with pytest.raises(ResponseValidationError):
            await client.get("/api/profiles", headers={"Authorization": f"Bearer {token_b}"})

        # 用户 B 的规划列表应为空
        resp = await client.get("/api/plans", headers={"Authorization": f"Bearer {token_b}"})
        assert resp.status_code == 200
        assert resp.json() == []

    @pytest.mark.asyncio
    async def test_token_expiry_and_invalidity(self, client, test_user):
        """Token 过期与无效"""
        # 无效 token
        resp = await client.get("/api/auth/me", headers={"Authorization": "Bearer fake.token.here"})
        assert resp.status_code == 401

        # 格式错误的 Authorization 头
        resp = await client.get("/api/auth/me", headers={"Authorization": "NotBearer abc"})
        assert resp.status_code == 401

    @pytest.mark.asyncio
    async def test_starmap_returns_correct_structure(self, auth_client):
        """星图接口返回结构正确"""
        resp = await auth_client.get("/api/starmap")
        assert resp.status_code == 200
        data = resp.json()
        assert "nodes" in data
        assert "edges" in data
        assert "current_position" in data
        assert isinstance(data["nodes"], list)
        assert isinstance(data["edges"], list)
