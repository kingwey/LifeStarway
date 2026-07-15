# LifeStarway 测试文档

## 目录结构

```
test/
├── run_all_tests.py              # 全量测试运行入口
├── test_report.json              # 汇总测试报告（自动生成）
├── backend/
│   ├── pytest.ini                # pytest 配置
│   ├── conftest.py               # 公共 fixtures（内存数据库、测试用户、认证客户端）
│   ├── test_auth.py              # 认证模块测试（11项）
│   ├── test_profile.py           # 档案模块测试（9项）
│   ├── test_business.py          # 诊断/规划/星图/WhatIf 测试（18项）
│   ├── test_utils.py             # 工具模块测试（密码哈希/JWT/缓存键/配置）
│   ├── test_infrastructure.py    # 基础设施测试（健康检查/CORS/路由注册）
│   └── test_integration.py       # 端到端集成测试（完整业务流程）
└── frontend/
    ├── test_frontend.js          # 前端测试脚本
    └── frontend_test_report.json # 前端测试报告（自动生成）
```

## 测试概览

| 测试套件 | 测试数 | 通过率 | 说明 |
|---------|--------|--------|------|
| 后端认证模块 | 11 | 100% | 注册、登录、JWT鉴权 |
| 后端档案模块 | 9 | 100% | 创建、获取、更新、版本历史 |
| 后端业务模块 | 18 | 100% | 诊断/规划/星图/WhatIf 接口 |
| 后端工具模块 | 18 | 100% | 密码哈希、JWT令牌、缓存键、配置 |
| 后端基础设施 | 22 | 100% | 健康检查、CORS、路由注册、错误处理 |
| 后端集成测试 | 5 | 100% | 完整业务流程、数据隔离 |
| 前端API层 | 32 | 100% | API模块定义、拦截器、FormData上传 |
| 前端路由 | 12 | 100% | 路由定义、守卫逻辑 |
| 前端Store | 12 | 100% | Pinia状态管理、localStorage持久化 |
| 前端配置 | 12 | 100% | Vite代理、依赖声明 |
| 前端组件 | 21 | 100% | 7个视图组件结构验证 |
| **合计** | **170** | **100%** | |

## 运行方式

### 全量测试
```bash
cd e:\chase\LifeStarway
backend\.venv\Scripts\python.exe test\run_all_tests.py
```

### 仅后端测试
```bash
cd e:\chase\LifeStarway
backend\.venv\Scripts\python.exe -m pytest test\backend -v -c test\backend\pytest.ini --rootdir test\backend
```

### 仅前端测试
```bash
cd e:\chase\LifeStarway
node test\frontend\test_frontend.js
```

## 测试覆盖范围

### 后端

#### 1. 认证模块 (test_auth.py)
- 用户注册：正常注册、重复邮箱、缺少字段、非法邮箱
- 用户登录：正常登录、密码错误、不存在用户、缺少字段
- 获取当前用户：有效token、无token、无效token

#### 2. 档案模块 (test_profile.py)
- 创建档案：完整数据、最小数据、空数据
- 获取档案：创建后获取、空状态获取
- 更新档案：版本自增、部分更新
- 认证保护：无token访问拒绝
- 版本历史：多次更新后获取版本列表

#### 3. 业务模块 (test_business.py)
- 诊断接口：认证保护、无档案时400、空列表、空latest
- 规划接口：认证保护、无诊断时400、空列表、不存在规划404
- 星图接口：认证保护、空数据结构验证
- WhatIf接口：认证保护、无档案时400、空列表、不存在模拟404

#### 4. 工具模块 (test_utils.py)
- 密码哈希：哈希生成、正确/错误密码验证、盐值唯一性、超长密码
- JWT令牌：生成、带过期、默认过期、解码、无效令牌
- 缓存键：一致性、参数差异、前缀、顺序无关性
- 配置：SECRET_KEY、ALGORITHM、TOKEN_EXPIRE、CORS、LLM配置

#### 5. 基础设施 (test_infrastructure.py)
- 健康检查：/health 和 / 端点
- CORS：预检请求头
- 错误处理：404路由、不允许的方法
- 路由注册：13个API端点参数化验证

#### 6. 集成测试 (test_integration.py)
- 完整流程：注册→登录→访问受保护接口
- 档案生命周期：创建→获取→更新→版本历史
- 数据隔离：不同用户间数据不可见
- Token安全：无效token、格式错误头
- 星图结构：返回JSON结构正确性

### 前端

#### 1. API层测试
- 6个API模块（auth/profile/diagnosis/plan/starmap/simulation）方法定义验证
- 请求拦截器：Authorization头注入
- 响应拦截器：401状态码处理、登录页跳转
- 文件上传：FormData、multipart header、120秒超时

#### 2. 路由守卫测试
- 7个路由定义（Login/Dashboard/Profile/Diagnosis/Plan/StarMap/WhatIf）
- 认证标记：登录页无需认证、其余需认证
- 守卫逻辑：beforeEach、isLoggedIn检查、重定向

#### 3. Pinia Store测试
- 状态初始化：token/user从localStorage读取
- 方法定义：login/register/fetchUser/fetchProfile/logout/isLoggedIn
- 持久化：login后存储token、logout清除token和user

#### 4. 配置测试
- Vite开发代理：/api路径代理到localhost:8000
- package.json依赖：Vue/Axios/Pinia/VueRouter/ElementPlus/ECharts/TailwindCSS
- 构建脚本：dev和build命令

#### 5. 视图组件测试
- 7个Vue组件文件存在性验证
- 每个组件包含template和script标签

## 测试策略

- **后端**：使用SQLite内存数据库隔离测试，pytest-asyncio支持异步测试，httpx.AsyncClient+ASGITransport直接测试ASGI应用
- **前端**：静态分析源文件验证模块定义、方法存在性、配置正确性（不依赖浏览器环境）
- **报告**：JSON格式自动生成，包含通过/失败/错误统计

## 已知限制

1. LLM相关接口（诊断创建、规划生成、简历导入、WhatIf模拟）因依赖外部API，仅测试前置条件校验，不测试LLM调用本身
2. 前端测试为静态分析，未覆盖运行时交互逻辑（如ECharts渲染、表单验证）
3. Redis缓存的集成测试需要Redis服务运行，单元测试仅验证键生成逻辑
