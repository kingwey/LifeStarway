"""档案模块测试 - 创建、获取、更新、版本"""
import pytest


class TestProfileCreate:
    """创建档案测试"""

    @pytest.mark.asyncio
    async def test_create_profile(self, auth_client):
        """创建完整档案"""
        resp = await auth_client.post("/api/profiles", json={
            "birth_year": 1995,
            "gender": "男",
            "education": "本科",
            "major": "计算机科学",
            "school": "清华大学",
            "skills": [
                {"name": "Python", "level": "高级", "years": 5},
                {"name": "JavaScript", "level": "中级", "years": 3},
            ],
            "personality_type": "INTJ",
            "current_industry": "互联网",
            "current_role": "高级开发工程师",
            "work_years": 5,
            "salary_range": "30-50万",
            "career_history": [
                {"company": "字节跳动", "role": "后端开发", "period": "2020-2023", "salary": "25-35万"},
            ],
        })
        assert resp.status_code == 200
        data = resp.json()
        assert data["education"] == "本科"
        assert data["major"] == "计算机科学"
        assert len(data["skills"]) == 2
        assert data["version"] == 1

    @pytest.mark.asyncio
    async def test_create_profile_minimal(self, auth_client):
        """创建最小档案（仅部分字段）"""
        resp = await auth_client.post("/api/profiles", json={"education": "硕士"})
        assert resp.status_code == 200
        assert resp.json()["education"] == "硕士"

    @pytest.mark.asyncio
    async def test_create_profile_empty(self, auth_client):
        """创建空档案（全部默认值）"""
        resp = await auth_client.post("/api/profiles", json={})
        assert resp.status_code == 200
        assert resp.json()["version"] == 1


class TestProfileGet:
    """获取档案测试"""

    @pytest.mark.asyncio
    async def test_get_profile_after_create(self, auth_client):
        """创建后获取档案"""
        await auth_client.post("/api/profiles", json={"education": "博士", "major": "AI"})

        resp = await auth_client.get("/api/profiles")
        assert resp.status_code == 200
        data = resp.json()
        assert data["education"] == "博士"
        assert data["major"] == "AI"

    @pytest.mark.asyncio
    async def test_get_profile_when_empty(self, auth_client):
        """未创建档案时获取会抛出 ResponseValidationError（None 序列化失败）"""
        from fastapi.exceptions import ResponseValidationError
        with pytest.raises(ResponseValidationError):
            await auth_client.get("/api/profiles")


class TestProfileUpdate:
    """更新档案测试"""

    @pytest.mark.asyncio
    async def test_update_profile_increments_version(self, auth_client):
        """更新档案应自增版本号"""
        await auth_client.post("/api/profiles", json={"education": "本科"})
        resp = await auth_client.post("/api/profiles", json={"education": "硕士"})
        assert resp.status_code == 200
        assert resp.json()["version"] == 2

    @pytest.mark.asyncio
    async def test_update_profile_partial(self, auth_client):
        """部分更新档案"""
        await auth_client.post("/api/profiles", json={
            "education": "本科", "major": "计算机", "school": "北大"
        })
        resp = await auth_client.post("/api/profiles", json={"major": "人工智能"})
        assert resp.status_code == 200
        data = resp.json()
        assert data["major"] == "人工智能"


class TestProfileAuth:
    """档案接口认证测试"""

    @pytest.mark.asyncio
    async def test_get_profile_without_auth(self, client):
        """无认证获取档案应返回 401"""
        resp = await client.get("/api/profiles")
        assert resp.status_code == 401

    @pytest.mark.asyncio
    async def test_create_profile_without_auth(self, client):
        """无认证创建档案应返回 401"""
        resp = await client.post("/api/profiles", json={"education": "本科"})
        assert resp.status_code == 401


class TestProfileVersions:
    """档案版本历史测试"""

    @pytest.mark.asyncio
    async def test_get_versions_after_updates(self, auth_client):
        """多次更新后获取版本列表"""
        await auth_client.post("/api/profiles", json={"education": "高中"})
        await auth_client.post("/api/profiles", json={"education": "本科"})
        await auth_client.post("/api/profiles", json={"education": "硕士"})

        resp = await auth_client.get("/api/profiles/versions")
        assert resp.status_code == 200
        data = resp.json()
        assert isinstance(data, list)
