"""公开信息采集服务 - 从GitHub、LinkedIn、博客等公开来源采集职业信息"""
import asyncio
import re
from typing import Optional, Dict, Any, List

import httpx

from app.config import settings


class ProfileScraper:
    """公开信息采集器"""
    
    DEFAULT_USER_AGENT = "LifeStarway/1.0 (https://github.com/lifestarway/lifestarway)"
    
    def __init__(self):
        self.client = httpx.AsyncClient(timeout=15.0, headers={"User-Agent": self.DEFAULT_USER_AGENT})
        self.github_token = settings.GITHUB_TOKEN
    
    async def fetch_github_profile(self, username: str) -> str:
        """从GitHub获取用户信息"""
        try:
            headers = {}
            if self.github_token:
                headers['Authorization'] = f'token {self.github_token}'
            
            user_info = await self._fetch_github_user(username, headers)
            repos = await self._fetch_github_repos(username, headers)
            languages = await self._analyze_languages(repos)
            
            return self._format_github_result(user_info, repos, languages)
        except Exception as e:
            return f"GitHub采集失败: {str(e)}"
    
    async def _fetch_github_user(self, username: str, headers: dict) -> Dict:
        url = f'https://api.github.com/users/{username}'
        resp = await self.client.get(url, headers=headers)
        resp.raise_for_status()
        return resp.json()
    
    async def _fetch_github_repos(self, username: str, headers: dict) -> List[Dict]:
        url = f'https://api.github.com/users/{username}/repos'
        params = {'per_page': 20, 'sort': 'updated', 'direction': 'desc'}
        resp = await self.client.get(url, headers=headers, params=params)
        resp.raise_for_status()
        return resp.json()
    
    async def _analyze_languages(self, repos: List[Dict]) -> Dict[str, int]:
        languages = {}
        
        for repo in repos[:10]:
            if repo.get('language'):
                lang = repo['language']
                languages[lang] = languages.get(lang, 0) + 1
        
        return languages
    
    def _format_github_result(self, user_info: Dict, repos: List[Dict], languages: Dict) -> str:
        parts = []
        
        if user_info.get('name'):
            parts.append(f"姓名: {user_info['name']}")
        if user_info.get('bio'):
            parts.append(f"简介: {user_info['bio']}")
        if user_info.get('company'):
            parts.append(f"公司: {user_info['company']}")
        if user_info.get('location'):
            parts.append(f"位置: {user_info['location']}")
        if user_info.get('blog'):
            parts.append(f"博客: {user_info['blog']}")
        
        parts.append(f"\nGitHub统计:")
        parts.append(f"  仓库数: {user_info.get('public_repos', 0)}")
        parts.append(f"  Stars: {sum(repo.get('stargazers_count', 0) for repo in repos)}")
        parts.append(f"  关注者: {user_info.get('followers', 0)}")
        parts.append(f"  创建时间: {user_info.get('created_at', '')[:10]}")
        
        parts.append(f"\n主要技术栈:")
        for lang, count in sorted(languages.items(), key=lambda x: -x[1])[:5]:
            parts.append(f"  {lang}: {count}个项目")
        
        parts.append(f"\n最近项目:")
        for repo in repos[:5]:
            desc = repo.get('description', '')[:50]
            parts.append(f"  {repo['name']} - {desc}")
            parts.append(f"    语言: {repo.get('language', '未知')}, Stars: {repo.get('stargazers_count', 0)}")
        
        return "\n".join(parts)
    
    async def fetch_linkedin_profile(self, profile_url: str) -> str:
        """从LinkedIn公开页面采集信息（支持用户提供的导出内容或公开页URL）"""
        try:
            username = self._extract_linkedin_username(profile_url)
            if username:
                return f"LinkedIn用户: {username}\n（完整信息需要用户登录后导出PDF或授权API访问）\n建议：上传LinkedIn导出的PDF文件以获取完整信息"
            return f"LinkedIn链接: {profile_url}\n（建议上传LinkedIn导出的PDF文件）"
        except Exception as e:
            return f"LinkedIn采集失败: {str(e)}"
    
    def _extract_linkedin_username(self, url: str) -> Optional[str]:
        patterns = [
            r'linkedin\.com/in/([^/]+)',
            r'linkedin\.com\/profile\/view\/id=([^&]+)'
        ]
        for pattern in patterns:
            match = re.search(pattern, url)
            if match:
                return match.group(1)
        return None
    
    async def fetch_blog_posts(self, blog_url: str) -> str:
        """从博客/技术社区采集文章内容"""
        try:
            resp = await self.client.get(blog_url)
            resp.raise_for_status()
            
            content = resp.text
            title_match = re.search(r'<title>(.*?)</title>', content, re.IGNORECASE)
            title = title_match.group(1) if title_match else '未知标题'
            
            text_content = self._extract_text_from_html(content)
            text_content = text_content[:2000]
            
            return f"博客: {title}\nURL: {blog_url}\n\n{text_content}"
        except Exception as e:
            return f"博客采集失败: {str(e)}"
    
    def _extract_text_from_html(self, html: str) -> str:
        text = re.sub(r'<[^>]+>', ' ', html)
        text = re.sub(r'\s+', ' ', text)
        return text.strip()
    
    async def fetch_from_source(self, source_type: str, url_or_username: str) -> str:
        """根据类型采集对应来源"""
        if source_type == 'github':
            username = url_or_username.replace('https://github.com/', '')
            username = username.rstrip('/')
            return await self.fetch_github_profile(username)
        elif source_type == 'linkedin':
            return await self.fetch_linkedin_profile(url_or_username)
        elif source_type == 'blog':
            return await self.fetch_blog_posts(url_or_username)
        else:
            return f"不支持的来源类型: {source_type}"
    
    async def close(self):
        """关闭HTTP客户端"""
        await self.client.aclose()


async def import_from_public_sources(sources: List[Any]) -> str:
    """从多个公开来源采集信息并合并"""
    scraper = ProfileScraper()
    results = []
    
    for source in sources:
        if hasattr(source, 'model_dump'):
            source_dict = source.model_dump()
        elif isinstance(source, dict):
            source_dict = source
        else:
            continue
        
        source_type = source_dict.get('type')
        url = source_dict.get('url')
        
        if source_type and url:
            result = await scraper.fetch_from_source(source_type, url)
            results.append(result)
    
    await scraper.close()
    
    return "\n\n" + "="*60 + "\n\n".join(results)