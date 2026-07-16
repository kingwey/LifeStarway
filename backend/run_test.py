import httpx
import json
import uuid

print('=' * 60)
print('LifeStarway 项目测试报告')
print('=' * 60)

results = []

# 1. 基础服务检查
print('\n--- 基础服务检查 ---')
try:
    r = httpx.get('http://localhost:8000/health', timeout=5)
    results.append({'test': '健康检查', 'status': 'PASS' if r.status_code == 200 else 'FAIL', 'detail': f'Status: {r.status_code}, Body: {r.text}'})
    print(f'✓ 健康检查: {r.status_code}')
except Exception as e:
    results.append({'test': '健康检查', 'status': 'FAIL', 'detail': str(e)})
    print(f'✗ 健康检查: {e}')

# 2. API 路由测试
print('\n--- API 路由测试 ---')
endpoints = [
    ('GET', '/api/auth/me'),
    ('POST', '/api/auth/register'),
    ('POST', '/api/auth/login'),
    ('GET', '/api/profiles'),
    ('POST', '/api/profiles'),
    ('POST', '/api/diagnoses'),
    ('GET', '/api/diagnoses/latest'),
    ('GET', '/api/diagnoses'),
    ('POST', '/api/plans/generate'),
    ('GET', '/api/plans'),
    ('GET', '/api/starmap'),
    ('POST', '/api/simulations'),
    ('GET', '/api/simulations'),
]

for method, path in endpoints:
    try:
        if method == 'GET':
            r = httpx.get(f'http://localhost:8000{path}', timeout=5)
        else:
            r = httpx.post(f'http://localhost:8000{path}', json={}, timeout=5)
        
        status = 'PASS' if r.status_code in [200, 201, 401, 422] else 'FAIL'
        detail = f'{method} {path}: Status {r.status_code}'
        if r.status_code == 401:
            detail += ' (需要认证，正常)'
        elif r.status_code == 422:
            detail += ' (参数验证失败，正常)'
        results.append({'test': detail, 'status': status, 'detail': r.text[:100]})
        print(f'{"✓" if status == "PASS" else "✗"} {method} {path}: {r.status_code}')
    except Exception as e:
        results.append({'test': f'{method} {path}', 'status': 'ERROR', 'detail': str(e)})
        print(f'✗ {method} {path}: {e}')

# 3. 注册登录流程
print('\n--- 认证流程测试 ---')
test_email = f'test_{uuid.uuid4().hex[:8]}@test.com'
test_password = 'Test123!@'
test_nickname = 'testuser'

try:
    r = httpx.post('http://localhost:8000/api/auth/register', 
                   json={'email': test_email, 'password': test_password, 'nickname': test_nickname}, 
                   timeout=10)
    reg_status = r.status_code
    reg_body = r.text[:80]
    results.append({'test': '用户注册', 'status': 'PASS' if reg_status == 200 else 'FAIL', 'detail': f'Status: {reg_status}, Body: {reg_body}'})
    print(f'用户注册: {reg_status} - {reg_body}')
    
    r2 = httpx.post('http://localhost:8000/api/auth/login', 
                    json={'email': test_email, 'password': test_password}, 
                    timeout=10)
    login_status = r2.status_code
    login_body = r2.text[:80]
    results.append({'test': '用户登录', 'status': 'PASS' if login_status == 200 else 'FAIL', 'detail': f'Status: {login_status}, Body: {login_body}'})
    print(f'用户登录: {login_status} - {login_body}')
    
    try:
        token_data = r2.json()
        token = token_data.get('access_token')
        if token:
            r3 = httpx.get('http://localhost:8000/api/auth/me', 
                           headers={'Authorization': f'Bearer {token}'}, 
                           timeout=5)
            auth_status = r3.status_code
            results.append({'test': '认证获取用户信息', 'status': 'PASS' if auth_status == 200 else 'FAIL', 'detail': f'Status: {auth_status}, Body: {r3.text[:80]}'})
            print(f'认证获取用户信息: {auth_status}')
            
            r4 = httpx.post('http://localhost:8000/api/profiles', 
                           headers={'Authorization': f'Bearer {token}'},
                           json={'education': '本科', 'major': '计算机科学', 'skills': [{'name': 'Python', 'level': '中级', 'years': 3}, {'name': 'FastAPI', 'level': '初级', 'years': 1}]},
                           timeout=10)
            profile_status = r4.status_code
            results.append({'test': '创建人生档案', 'status': 'PASS' if profile_status in [200, 201] else 'FAIL', 'detail': f'Status: {profile_status}, Body: {r4.text[:80]}'})
            print(f'创建人生档案: {profile_status}')
            
            r5 = httpx.get('http://localhost:8000/api/profiles', 
                           headers={'Authorization': f'Bearer {token}'},
                           timeout=5)
            profile_get_status = r5.status_code
            results.append({'test': '获取人生档案', 'status': 'PASS' if profile_get_status == 200 else 'FAIL', 'detail': f'Status: {profile_get_status}'})
            print(f'获取人生档案: {profile_get_status}')
            
            r6 = httpx.get('http://localhost:8000/api/starmap', 
                           headers={'Authorization': f'Bearer {token}'},
                           timeout=5)
            starmap_status = r6.status_code
            results.append({'test': '获取人生星途图', 'status': 'PASS' if starmap_status == 200 else 'FAIL', 'detail': f'Status: {starmap_status}'})
            print(f'获取人生星途图: {starmap_status}')
            
    except Exception as e:
        results.append({'test': '认证后操作', 'status': 'ERROR', 'detail': str(e)})
        print(f'认证后操作异常: {e}')
        
except Exception as e:
    results.append({'test': '认证流程', 'status': 'ERROR', 'detail': str(e)})
    print(f'认证流程异常: {e}')

# 4. 汇总
print('\n' + '=' * 60)
pass_count = sum(1 for r in results if r['status'] == 'PASS')
fail_count = sum(1 for r in results if r['status'] == 'FAIL')
error_count = sum(1 for r in results if r['status'] == 'ERROR')
total = len(results)

print(f'测试结果: {pass_count}/{total} 通过, {fail_count} 失败, {error_count} 错误')
print('=' * 60)

report = {
    'date': '2026-07-15',
    'total_tests': total,
    'passed': pass_count,
    'failed': fail_count,
    'errors': error_count,
    'results': results
}

with open('test_report.json', 'w', encoding='utf-8') as f:
    json.dump(report, f, ensure_ascii=False, indent=2)

print('\n测试报告已保存到: test_report.json')