# 人生星途 LifeStarway

> 数据沉淀迭代式 · AI 全生命周期职业生涯规划系统

围绕 **「注册 → 建档 → AI 诊断 → 规划生成 → 星图可视化」** 的完整闭环，帮助用户沉淀个人成长数据、获取 AI 驱动的职业健康度评估与短/中/长期规划，并以星空风格的「人生星图」可视化成长路径。

## 在线体验

| | 地址 |
|---|---|
| 前端 | https://lifestarway-frontend.onrender.com |
| 后端 API | https://lifestarway-backend.onrender.com |
| API 文档 (Swagger) | https://lifestarway-backend.onrender.com/docs |

**测试账号**：`test@lifestarway.com` / `Test123!@`

> ⚠️ 免费实例闲置 15 分钟后会休眠，首次访问需等待几十秒冷启动。
> AI 相关功能（诊断 / 规划 / 简历解析 / What-If）需配置大模型 API Key 后才可用，其余功能不受影响。

## 核心功能

| 模块 | 说明 |
|------|------|
| 用户系统 | 注册 / 登录、JWT 认证 |
| 人生档案 | 个人信息、学历、工作履历、技能矩阵录入；简历文本 / 文件（PDF、Word）导入解析；公开链接（GitHub 等）采集；档案多版本沉淀 |
| AI 诊断引擎 | 五维度职业健康度评估 |
| 规划生成 | 1 年短期 + 3 年中期 + 5 年长期职业规划 |
| 人生星图 | 里程碑星空可视化、成长路径连线、达成概率 |
| What-If 沙盒 | 假设不同选择，模拟职业轨迹变化 |

## 技术栈

**后端**：FastAPI · Uvicorn · SQLAlchemy 2.0 (async) · Alembic · Pydantic v2 · python-jose (JWT) · passlib (bcrypt) · openai SDK · Redis

**前端**：Vue 3 · Vite · Vue Router · Pinia · Element Plus · ECharts · TailwindCSS · Axios

**数据 / 基础设施**：PostgreSQL（生产）/ SQLite（本地零配置）· Redis · Docker · Render

**大模型**：通过 OpenAI 兼容接口对接，支持多提供商切换 —— 阿里云百炼 DashScope（默认 `qwen-plus`）、火山引擎豆包、Google Gemini。

## 架构概览

```
┌──────────────────────────────────────────────┐
│  前端  Vue 3 + Vite + ECharts + TailwindCSS   │
└───────────────────────┬──────────────────────┘
                        │ HTTP (REST)
┌───────────────────────▼──────────────────────┐
│  后端  FastAPI + Uvicorn                      │
│  api → services → models（认证/档案/诊断/规划/星图/What-If）│
│  ┌────────────────────────────────────────┐  │
│  │  AI 层：LLM 统一调用 + Prompt 模板       │  │
│  │  （OpenAI 兼容，多模型切换）             │  │
│  └────────────────────────────────────────┘  │
└──────────────┬─────────────────┬─────────────┘
              │                 │
      ┌────────▼──────┐   ┌──────▼──────┐
      │  PostgreSQL   │   │    Redis     │
      │  (SQLite本地) │   │  (缓存/限流) │
      └───────────────┘   └─────────────┘
```

## 项目结构

```
LifeStarway/
├── backend/                 # FastAPI 后端
│   ├── app/
│   │   ├── main.py          # 应用入口（含 /health、CORS、日志中间件）
│   │   ├── config.py        # Pydantic Settings 配置 + LLM 多提供商预设
│   │   ├── database.py      # 异步数据库连接（自动规范化 Postgres URL）
│   │   ├── models/          # SQLAlchemy 模型
│   │   ├── schemas/         # Pydantic 请求/响应模型
│   │   ├── api/             # 路由层（auth/profile/diagnosis/plan/starmap/whatif/user）
│   │   ├── services/        # 业务逻辑层
│   │   ├── ai/              # LLM 客户端、Prompt 模板、解析器
│   │   └── utils/           # 缓存等工具
│   ├── alembic/             # 数据库迁移
│   ├── requirements.txt
│   └── Dockerfile
├── frontend/                # Vue 3 前端
│   ├── src/
│   │   ├── api/             # Axios 封装
│   │   ├── stores/          # Pinia 状态
│   │   ├── router/          # 路由（history 模式）
│   │   └── ...
│   ├── package.json
│   └── Dockerfile
├── docs/                    # 技术方案与分析文档
├── docker-compose.yml       # 一键启动 db + redis + backend + frontend
└── render.yaml              # Render Blueprint 部署配置
```

## 本地开发

### 方式一：Docker Compose（推荐，一键起全套）

```bash
# 在 backend/.env 中填入大模型 API Key（见下方环境变量）
docker compose up --build
```

启动后：前端 http://localhost · 后端 http://localhost:8000 · API 文档 http://localhost:8000/docs

### 方式二：分别启动

**后端**（Python 3.12）：

```bash
cd backend
python -m venv .venv && source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env   # 若无则手动创建，参考下方环境变量
uvicorn app.main:app --reload
```

未配置 `DATABASE_URL` 时默认使用本地 SQLite，零配置即可启动。

**前端**（Node 18+）：

```bash
cd frontend
npm install
npm run dev        # 默认 http://localhost:5173，已通过 Vite proxy 转发 /api 到 8000
```

## 环境变量

后端（`backend/.env`）：

| 变量 | 说明 | 默认 |
|------|------|------|
| `SECRET_KEY` | JWT 签名密钥 | 必填 |
| `ALGORITHM` | JWT 算法 | `HS256` |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | Token 有效期（分钟） | `30` |
| `DATABASE_URL` | 数据库连接串（`postgresql://` / `postgres://` 会自动转为 asyncpg 驱动） | `sqlite:///./lifestarway.db` |
| `REDIS_URL` | Redis 连接串 | `redis://localhost:6379/0` |
| `CORS_ORIGINS` | 允许的前端来源（逗号分隔） | 本地若干端口 |
| `LLM_PROVIDER` | 大模型提供商：`dashscope` / `doubao` / `gemini` | `dashscope` |
| `DASHSCOPE_API_KEY` | 通义千问 API Key（选用 dashscope 时） | — |
| `DOUBAO_API_KEY` / `GEMINI_API_KEY` | 对应提供商 Key | — |
| `LLM_MODEL` | 覆盖默认模型 | 按提供商预设 |
| `LLM_API_KEY` / `LLM_API_BASE` | 三者同时设置可完全自定义 LLM 接入 | — |

前端（`frontend/.env` / `.env.production`）：

| 变量 | 说明 |
|------|------|
| `VITE_API_BASE_URL` | 后端 API 基地址；缺省为 `/api`（本地由 Vite proxy 转发） |

## API 一览

所有接口以 `/api` 为前缀，需认证的接口在请求头携带 `Authorization: Bearer <token>`。

| 分组 | 方法 & 路径 | 说明 |
|------|------|------|
| 认证 | `POST /api/auth/register` | 注册（密码需 ≥8 位，含大小写字母、数字、特殊字符） |
| | `POST /api/auth/login` | 登录，返回 JWT |
| | `GET /api/auth/me` | 当前用户 |
| 用户 | `GET/PATCH /api/users/me`，`POST /api/users/me/password` | 用户信息 / 改密 |
| 档案 | `GET/POST /api/profiles` | 读取 / 保存档案 |
| | `POST /api/profiles/import-resume`，`/upload-resume`，`/import-links` | 简历文本 / 文件 / 链接导入 |
| | `GET /api/profiles/versions` | 档案历史版本 |
| 诊断 | `POST /api/diagnoses`，`GET /api/diagnoses`，`/latest` | 职业健康度评估 |
| 规划 | `POST /api/plans/generate`，`GET /api/plans`，`/{id}` | 规划生成 / 查询 |
| 星图 | `GET /api/starmap` | 星图数据 |
| What-If | `POST /api/simulations`，`GET /api/simulations`，`/{id}` | 情景模拟 |

完整交互式文档见 `/docs`（Swagger）与 `/redoc`。

## 部署（Render）

项目已包含 [`render.yaml`](render.yaml) Blueprint，一次创建后端 Web Service、前端静态站、PostgreSQL、Redis 四个资源。

1. 代码推送到 GitHub / GitLab
2. Render 控制台 → **New → Blueprint** → 选择本仓库 → **Apply**
3. 部署完成后，在 `lifestarway-backend` 服务的 **Environment** 中填入 `DASHSCOPE_API_KEY` 以启用 AI 功能

> 说明：`render.yaml` 已锁定 Python 3.12、将数据库连接串自动适配 asyncpg、为前端配置 SPA 重写规则与 API 基地址。默认使用免费计划（后端闲置会休眠、免费 PostgreSQL 有时效限制），正式环境建议升级为付费计划。

## License

本项目用于作品/演示用途。
