/**
 * 前端 API 层测试
 * 测试 src/api/index.js 中各 API 模块的方法定义和调用方式
 */

// ── 测试工具 ──────────────────────────────────────────────────

let passCount = 0;
let failCount = 0;
const results = [];

function assert(condition, message) {
    if (condition) {
        passCount++;
        results.push({ test: message, status: 'PASS' });
        console.log(`  ✓ ${message}`);
    } else {
        failCount++;
        results.push({ test: message, status: 'FAIL' });
        console.log(`  ✗ ${message}`);
    }
}

function assertEqual(actual, expected, message) {
    assert(actual === expected, `${message} (期望: ${expected}, 实际: ${actual})`);
}

// ── API 模块定义验证 ──────────────────────────────────────────

console.log('\n── 前端 API 模块定义测试 ──\n');

// 由于无法在 Node.js 中直接 import .vue 和 ESM 带 env 的模块，
// 这里通过读取源文件内容进行静态验证
const fs = require('fs');
const path = require('path');

const apiSource = fs.readFileSync(
    path.join(__dirname, '..', '..', 'frontend', 'src', 'api', 'index.js'),
    'utf-8'
);

// 测试 authApi 定义
assert(apiSource.includes('authApi'), 'authApi 模块已定义');
assert(apiSource.includes('register: (data) => api.post'), 'authApi.register 方法已定义');
assert(apiSource.includes('login: (data) => api.post'), 'authApi.login 方法已定义');
assert(apiSource.includes('me: () => api.get'), 'authApi.me 方法已定义');

// 测试 profileApi 定义
assert(apiSource.includes('profileApi'), 'profileApi 模块已定义');
assert(apiSource.includes("get: () => api.get('/profiles')"), 'profileApi.get 方法已定义');
assert(apiSource.includes("update: (data) => api.post('/profiles'"), 'profileApi.update 方法已定义');
assert(apiSource.includes('importResume'), 'profileApi.importResume 方法已定义');
assert(apiSource.includes('uploadResume'), 'profileApi.uploadResume 方法已定义');
assert(apiSource.includes('versions'), 'profileApi.versions 方法已定义');

// 测试 diagnosisApi 定义
assert(apiSource.includes('diagnosisApi'), 'diagnosisApi 模块已定义');
assert(apiSource.includes('create: (data) => api.post'), 'diagnosisApi.create 方法已定义');
assert(apiSource.includes('latest: () => api.get'), 'diagnosisApi.latest 方法已定义');
assert(apiSource.includes('list: () => api.get'), 'diagnosisApi.list 方法已定义');

// 测试 planApi 定义
assert(apiSource.includes('planApi'), 'planApi 模块已定义');
assert(apiSource.includes('generate: (data) => api.post'), 'planApi.generate 方法已定义');
assert(apiSource.includes("list: () => api.get('/plans')"), 'planApi.list 方法已定义');
assert(apiSource.includes("get: (id) => api.get(`/plans/${id}`)"), 'planApi.get 方法已定义');

// 测试 starmapApi 定义
assert(apiSource.includes('starmapApi'), 'starmapApi 模块已定义');
assert(apiSource.includes("get: () => api.get('/starmap')"), 'starmapApi.get 方法已定义');

// 测试 simulationApi 定义
assert(apiSource.includes('simulationApi'), 'simulationApi 模块已定义');
assert(apiSource.includes('create: (data) => api.post'), 'simulationApi.create 方法已定义');
assert(apiSource.includes('list: () => api.get'), 'simulationApi.list 方法已定义');
assert(apiSource.includes('get: (id) => api.get'), 'simulationApi.get 方法已定义');

// 测试拦截器
assert(apiSource.includes('interceptors.request.use'), '请求拦截器已配置');
assert(apiSource.includes('Authorization'), '请求拦截器注入 Authorization 头');
assert(apiSource.includes('interceptors.response.use'), '响应拦截器已配置');
assert(apiSource.includes('401'), '响应拦截器处理 401 状态码');
assert(apiSource.includes("window.location.href = '/login'"), '401 时跳转登录页');

// 测试 FormData 上传
assert(apiSource.includes('FormData'), '文件上传使用 FormData');
assert(apiSource.includes('multipart/form-data'), '文件上传设置 multipart header');
assert(apiSource.includes('120000'), '文件上传超时 120 秒');


// ── Router 路由守卫测试 ───────────────────────────────────────

console.log('\n── 路由守卫测试 ──\n');

const routerSource = fs.readFileSync(
    path.join(__dirname, '..', '..', 'frontend', 'src', 'router', 'index.js'),
    'utf-8'
);

assert(routerSource.includes("path: '/login'"), '登录路由已定义');
assert(routerSource.includes("path: '/'"), '首页路由已定义');
assert(routerSource.includes("path: '/profile'"), '档案路由已定义');
assert(routerSource.includes("path: '/diagnosis'"), '诊断路由已定义');
assert(routerSource.includes("path: '/plan'"), '规划路由已定义');
assert(routerSource.includes("path: '/starmap'"), '星图路由已定义');
assert(routerSource.includes("path: '/whatif'"), 'WhatIf 路由已定义');

assert(routerSource.includes('requiresAuth: false'), '登录页无需认证');
assert(routerSource.includes('requiresAuth: true'), '受保护页面需认证');
assert(routerSource.includes('beforeEach'), '全局路由守卫已配置');
assert(routerSource.includes('isLoggedIn'), '路由守卫检查登录状态');
assert(routerSource.includes("next('/login')"), '未登录时重定向到登录页');


// ── Pinia Store 测试 ──────────────────────────────────────────

console.log('\n── Pinia Store 测试 ──\n');

const storeSource = fs.readFileSync(
    path.join(__dirname, '..', '..', 'frontend', 'src', 'stores', 'user.js'),
    'utf-8'
);

assert(storeSource.includes('defineStore'), 'Pinia store 已定义');
assert(storeSource.includes("localStorage.getItem('token')"), 'token 从 localStorage 初始化');
assert(storeSource.includes("localStorage.getItem('user')"), 'user 从 localStorage 初始化');
assert(storeSource.includes('isLoggedIn'), 'isLoggedIn 方法已定义');
assert(storeSource.includes('login'), 'login 方法已定义');
assert(storeSource.includes('register'), 'register 方法已定义');
assert(storeSource.includes('fetchUser'), 'fetchUser 方法已定义');
assert(storeSource.includes('fetchProfile'), 'fetchProfile 方法已定义');
assert(storeSource.includes('logout'), 'logout 方法已定义');
assert(storeSource.includes("localStorage.setItem('token'"), 'login 后持久化 token');
assert(storeSource.includes("localStorage.removeItem('token')"), 'logout 清除 token');
assert(storeSource.includes("localStorage.removeItem('user')"), 'logout 清除 user');


// ── Vite 配置测试 ─────────────────────────────────────────────

console.log('\n── Vite 配置测试 ──\n');

const viteSource = fs.readFileSync(
    path.join(__dirname, '..', '..', 'frontend', 'vite.config.js'),
    'utf-8'
);

assert(viteSource.includes('proxy'), '开发代理已配置');
assert(viteSource.includes("'/api'"), 'API 路径代理已配置');
assert(viteSource.includes('localhost:8000'), '代理目标为后端 8000 端口');


// ── package.json 依赖测试 ─────────────────────────────────────

console.log('\n── 依赖配置测试 ──\n');

const pkgSource = JSON.parse(fs.readFileSync(
    path.join(__dirname, '..', '..', 'frontend', 'package.json'),
    'utf-8'
));

assert(pkgSource.dependencies.vue, 'Vue 依赖已声明');
assert(pkgSource.dependencies.axios, 'Axios 依赖已声明');
assert(pkgSource.dependencies.pinia, 'Pinia 依赖已声明');
assert(pkgSource.dependencies['vue-router'], 'Vue Router 依赖已声明');
assert(pkgSource.dependencies['element-plus'], 'Element Plus 依赖已声明');
assert(pkgSource.dependencies.echarts, 'ECharts 依赖已声明');
assert(pkgSource.dependencies.tailwindcss, 'TailwindCSS 依赖已声明');
assert(pkgSource.scripts.dev, 'dev 脚本已定义');
assert(pkgSource.scripts.build, 'build 脚本已定义');


// ── 视图组件结构测试 ──────────────────────────────────────────

console.log('\n── 视图组件结构测试 ──\n');

const viewsDir = path.join(__dirname, '..', '..', 'frontend', 'src', 'views');
const expectedViews = ['Login.vue', 'Dashboard.vue', 'Profile.vue', 'Diagnosis.vue', 'Plan.vue', 'StarMap.vue', 'WhatIf.vue'];

for (const view of expectedViews) {
    const viewPath = path.join(viewsDir, view);
    assert(fs.existsSync(viewPath), `${view} 组件文件存在`);

    if (fs.existsSync(viewPath)) {
        const content = fs.readFileSync(viewPath, 'utf-8');
        assert(content.includes('<template>'), `${view} 包含 template 标签`);
        assert(content.includes('<script'), `${view} 包含 script 标签`);
    }
}


// ── 汇总 ──────────────────────────────────────────────────────

console.log('\n' + '═'.repeat(60));
console.log(`前端测试结果: ${passCount}/${passCount + failCount} 通过, ${failCount} 失败`);
console.log('═'.repeat(60));

// 输出 JSON 报告
const report = {
    date: new Date().toISOString().split('T')[0],
    total_tests: passCount + failCount,
    passed: passCount,
    failed: failCount,
    results: results,
};

fs.writeFileSync(
    path.join(__dirname, 'frontend_test_report.json'),
    JSON.stringify(report, null, 2)
);

console.log('\n前端测试报告已保存到: test/frontend/frontend_test_report.json');

process.exit(failCount > 0 ? 1 : 0);
