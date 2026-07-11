import asyncio
import os
import requests
from playwright.async_api import async_playwright

screenshots_dir = r'f:\python_code\LifeStarway\docs\screenshots'
os.makedirs(screenshots_dir, exist_ok=True)

pages = [
    ('http://localhost:5173/', 'dashboard_page.png'),
    ('http://localhost:5173/profile', 'profile_page.png'),
    ('http://localhost:5173/diagnosis', 'diagnosis_page.png'),
    ('http://localhost:5173/plan', 'plan_page.png'),
    ('http://localhost:5173/starmap', 'starmap_page.png'),
    ('http://localhost:5173/whatif', 'whatif_page.png'),
    ('http://localhost:8000/docs', 'api_docs.png'),
]

def login_via_api():
    try:
        email = 'screenshot@test.com'
        password = '12345678'
        
        login_data = {
            'email': email,
            'password': password
        }
        response = requests.post('http://localhost:8000/api/auth/login', json=login_data, timeout=10)
        result = response.json()
        print(f'Login API response: {result}')
        
        if 'access_token' in result:
            return result['access_token']
    except Exception as e:
        print(f'API login failed: {e}')
    return None

async def main():
    token = login_via_api()
    print(f'Token obtained: {token[:20]}...' if token else 'No token')
    
    async with async_playwright() as p:
        edge_path = r'C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe'
        
        if not os.path.exists(edge_path):
            print("Edge browser not found!")
            return
        
        browser = await p.chromium.launch(
            headless=True,
            executable_path=edge_path,
            args=['--no-sandbox', '--disable-gpu']
        )
        context = await browser.new_context(viewport={'width': 1920, 'height': 1080})
        page = await context.new_page()
        
        await page.goto('http://localhost:5173/login', wait_until='domcontentloaded')
        await page.wait_for_timeout(3000)
        
        await page.screenshot(path=os.path.join(screenshots_dir, 'login_page.png'), full_page=True)
        print('Saved: login_page.png')
        
        if token:
            await page.evaluate(f"localStorage.setItem('token', '{token}')")
            await page.evaluate("""
                localStorage.setItem('user', JSON.stringify({id: '1', email: 'screenshot@test.com', nickname: '截图测试用户'}));
            """)
            print('Real token saved to localStorage')
        else:
            await page.evaluate("""
                localStorage.setItem('token', 'test-token-for-screenshot');
                localStorage.setItem('user', JSON.stringify({id: '1', email: 'test@example.com', nickname: '测试用户'}));
            """)
            print('Using mock token')
        
        await page.goto('http://localhost:5173/', wait_until='domcontentloaded')
        await page.wait_for_timeout(5000)
        
        current_url = page.url
        print(f'After navigation to / URL: {current_url}')
        
        for url, filename in pages:
            print(f'Opening {url}...')
            
            await page.goto(url, wait_until='domcontentloaded')
            await page.wait_for_timeout(5000)
            
            current_url = page.url
            print(f'Current URL: {current_url}')
            
            title = await page.title()
            print(f'Page title: {title}')
            
            path = os.path.join(screenshots_dir, filename)
            await page.screenshot(path=path, full_page=True)
            print(f'Saved: {path}')
        
        await browser.close()
    print("All screenshots saved!")

asyncio.run(main())