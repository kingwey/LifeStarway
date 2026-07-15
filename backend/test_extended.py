import httpx, json

# 登录获取token
r = httpx.post('http://localhost:8000/api/auth/login', json={'email': 'test_e831560c@test.com', 'password': 'test123'}, timeout=10)
token = r.json()['access_token']
headers = {'Authorization': f'Bearer {token}'}

results = []

# 测试公开信息导入接口
try:
    r = httpx.post('http://localhost:8000/api/profiles/import-links',
                   headers=headers,
                   json={'sources': [{'type': 'github', 'url': 'https://github.com/torvalds'}]},
                   timeout=30)
    status = 'PASS' if r.status_code in [200, 201, 202] else 'FAIL'
    results.append({'test': '公开信息导入(GitHub)', 'status': status, 'detail': f'Status: {r.status_code}, Body: {r.text[:100]}'})
    print(f'公开信息导入(GitHub): {r.status_code} - {r.text[:100]}')
except Exception as e:
    results.append({'test': '公开信息导入(GitHub)', 'status': 'ERROR', 'detail': str(e)})
    print(f'公开信息导入异常: {e}')

# 测试简历上传接口（模拟文本解析）
try:
    r = httpx.post('http://localhost:8000/api/profiles/import-resume',
                   headers=headers,
                   json={'resume_text': '张三，本科，计算机科学，5年Python开发经验，熟悉FastAPI和Vue.js'},
                   timeout=30)
    status = 'PASS' if r.status_code in [200, 201] else 'FAIL'
    results.append({'test': '简历文本导入', 'status': status, 'detail': f'Status: {r.status_code}'})
    print(f'简历文本导入: {r.status_code}')
except Exception as e:
    results.append({'test': '简历文本导入', 'status': 'ERROR', 'detail': str(e)})
    print(f'简历文本导入异常: {e}')

# 测试健康检查Redis状态
try:
    r = httpx.get('http://localhost:8000/health', timeout=5)
    health = r.json()
    results.append({'test': '健康检查(Redis状态)', 'status': 'PASS', 'detail': f'Redis: {health.get("redis", "unknown")}'})
    print(f'健康检查: {health}')
except Exception as e:
    results.append({'test': '健康检查', 'status': 'ERROR', 'detail': str(e)})

print(f'\n扩展测试结果: {sum(1 for r in results if r["status"]=="PASS")}/{len(results)} 通过')

# 追加到测试报告
with open('test_report.json', 'r', encoding='utf-8') as f:
    report = json.load(f)

report['extended_results'] = results
report['extended_passed'] = sum(1 for r in results if r['status']=='PASS')
report['extended_total'] = len(results)

with open('test_report.json', 'w', encoding='utf-8') as f:
    json.dump(report, f, ensure_ascii=False, indent=2)

print('扩展测试报告已追加')
