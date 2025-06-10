import requests
from bs4 import BeautifulSoup
from typing import List, Dict
from urllib.parse import quote

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
    'Accept-Language': 'en-US,en;q=0.9'
}

def get_community_resources(skill: str) -> List[Dict]:
    try:
        encoded_skill = quote(skill.lower().replace(' ', '-'))
        resources = []
        
        github_resources = scrape_github_topics(encoded_skill)
        resources.extend(github_resources)
        
        unique_resources = []
        seen_urls = set()
        for res in resources:
            if res['url'] not in seen_urls:
                unique_resources.append(res)
                seen_urls.add(res['url'])
        
        return unique_resources[:4]
    
    except Exception as e:
        print(f"Resource scraping error: {e}")
        return get_fallback_resources(skill)

def scrape_github_topics(skill: str) -> List[Dict]:
    try:
        url = f"https://github.com/topics/{skill}"
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        resources = []
        
        topic_title = soup.select_one('h1')
        if topic_title and 'topics' in response.url:
            resources.append({
                'type': 'GitHub Topic',
                'name': topic_title.text.strip(),
                'url': response.url
            })
        
        for repo in soup.select('article.my-4'):
            if len(resources) >= 4:
                break
            title = repo.select_one('h3').text.strip()
            url = "https://github.com" + repo.select_one('a')['href']
            resources.append({
                'type': 'GitHub Repo',
                'name': title,
                'url': url
            })
        
        return resources
    except Exception as e:
        print(f"GitHub scraping failed: {e}")
        return []

def get_fallback_resources(skill: str) -> List[Dict]:
    encoded_skill = quote(skill.lower().replace(' ', '-'))
    return [
        {
            'type': 'Stack Overflow',
            'name': f"{skill} Questions",
            'url': f"https://stackoverflow.com/questions/tagged/{encoded_skill}"
        },
        {
            'type': 'GitHub',
            'name': f"{skill} Topics",
            'url': f"https://github.com/topics/{encoded_skill}"
        }
    ]
