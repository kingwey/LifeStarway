"""诊断、规划、星图、WhatIf 模块测试"""
import uuid
import pytest


# ── 诊断模块 ───────────────────────────────────────────────────

class TestDiagnosisAuth:
    """诊断接口认证测试"""

    @pytest.mark.asyncio
    async def test_create_diagnosis_without_auth(self, client):
        resp = await client.post("/api/diagnoses", json={})
        assert resp.status_code == 401

    @pytest.mark.asyncio
    async def test_get_latest_diagnosis_without_auth(self, client):
        resp = await client.get("/api/diagnoses/latest")
        assert resp.status_code == 401

    @pytest.mark.asyncio
    async def test_list_diagnoses_without_auth(self, client):
        resp = await client.get("/api/diagnoses")
        assert resp.status_code == 401


class TestDiagnosisLogic:
    """诊断业务逻辑测试"""

    @pytest.mark.asyncio
    async def test_diagnose_without_profile(self, auth_client):
        """未创建档案时诊断应返回 400"""
        resp = await client_post(auth_client, "/api/diagnoses", {})
        assert resp.status_code == 400
        assert "档案" in resp.json()["detail"]

    @pytest.mark.asyncio
    async def test_list_diagnoses_empty(self, auth_client):
        """无诊断记录时列表为空"""
        resp = await auth_client.get("/api/diagnoses")
        assert resp.status_code == 200
        assert resp.json() == []

    @pytest.mark.asyncio
    async def test_get_latest_diagnosis_empty(self, auth_client):
        """无诊断记录时 latest 会抛出 ResponseValidationError（None 序列化失败）"""
        from fastapi.exceptions import ResponseValidationError
        with pytest.raises(ResponseValidationError):
            await auth_client.get("/api/diagnoses/latest")


# ── 规划模块 ───────────────────────────────────────────────────

class TestPlanAuth:
    """规划接口认证测试"""

    @pytest.mark.asyncio
    async def test_generate_plan_without_auth(self, client):
        resp = await client.post("/api/plans/generate", json={"plan_type": "short_term"})
        assert resp.status_code == 401

    @pytest.mark.asyncio
    async def test_list_plans_without_auth(self, client):
        resp = await client.get("/api/plans")
        assert resp.status_code == 401


class TestPlanLogic:
    """规划业务逻辑测试"""

    @pytest.mark.asyncio
    async def test_generate_plan_without_diagnosis(self, auth_client):
        """未诊断时生成规划应返回 400"""
        resp = await client_post(auth_client, "/api/plans/generate", {"plan_type": "short_term"})
        assert resp.status_code == 400
        assert "诊断" in resp.json()["detail"]

    @pytest.mark.asyncio
    async def test_list_plans_empty(self, auth_client):
        """无规划时列表为空"""
        resp = await auth_client.get("/api/plans")
        assert resp.status_code == 200
        assert resp.json() == []

    @pytest.mark.asyncio
    async def test_get_nonexistent_plan(self, auth_client):
        """获取不存在的规划应返回 404"""
        resp = await auth_client.get(f"/api/plans/{uuid.uuid4()}")
        assert resp.status_code == 404


# ── 星图模块 ───────────────────────────────────────────────────

class TestStarMap:
    """星图接口测试"""

    @pytest.mark.asyncio
    async def test_get_starmap_without_auth(self, client):
        resp = await client.get("/api/starmap")
        assert resp.status_code == 401

    @pytest.mark.asyncio
    async def test_get_starmap_empty(self, auth_client):
        """无规划数据时星图为空"""
        resp = await auth_client.get("/api/starmap")
        assert resp.status_code == 200
        data = resp.json()
        assert "nodes" in data
        assert "edges" in data
        assert data["nodes"] == []
        assert data["edges"] == []


# ── WhatIf 模拟模块 ────────────────────────────────────────────

class TestWhatIfAuth:
    """WhatIf 接口认证测试"""

    @pytest.mark.asyncio
    async def test_create_simulation_without_auth(self, client):
        resp = await client.post("/api/simulations", json={"hypothesis": {}})
        assert resp.status_code == 401

    @pytest.mark.asyncio
    async def test_list_simulations_without_auth(self, client):
        resp = await client.get("/api/simulations")
        assert resp.status_code == 401


class TestWhatIfLogic:
    """WhatIf 业务逻辑测试"""

    @pytest.mark.asyncio
    async def test_create_simulation_without_profile(self, auth_client):
        """无档案时创建模拟应返回 400"""
        resp = await client_post(auth_client, "/api/simulations", {"hypothesis": {"action": "转行"}})
        assert resp.status_code == 400
        assert "档案" in resp.json()["detail"]

    @pytest.mark.asyncio
    async def test_list_simulations_empty(self, auth_client):
        """无模拟记录时列表为空"""
        resp = await auth_client.get("/api/simulations")
        assert resp.status_code == 200
        assert resp.json() == []

    @pytest.mark.asyncio
    async def test_get_nonexistent_simulation(self, auth_client):
        """获取不存在的模拟应返回 404"""
        resp = await auth_client.get(f"/api/simulations/{uuid.uuid4()}")
        assert resp.status_code == 404


# ── 工具函数 ───────────────────────────────────────────────────

async def client_post(client, url, json_data):
    """封装 POST 请求，处理 LLM 调用异常"""
    try:
        return await client.post(url, json=json_data)
    except Exception:
        # LLM 调用失败时会抛出 RuntimeError，被全局异常处理器捕获
        # 返回一个模拟 response
        class MockResp:
            status_code = 500
            def json(self):
                return {"detail": "服务器内部错误"}
        return MockResp()
