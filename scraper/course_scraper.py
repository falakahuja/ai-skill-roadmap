import requests
from bs4 import BeautifulSoup
from typing import List, Dict

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
}

def get_coursera_courses(skill: str) -> List[Dict]:
    """Scrape both free and paid Coursera courses based on the given skill."""
    courses = []
    try:
        search_url = f"https://www.coursera.org/search?query={skill}"
        response = requests.get(search_url, headers=headers, timeout=10)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, 'html.parser')
        course_cards = soup.select('a[data-click-key="search.search.click.search_card"]')
        print(f"[Coursera] Found {len(course_cards)} course cards")

        for card in course_cards[:3]:  # Top 3 courses
            title_tag = card.select_one('h3')
            title = title_tag.text.strip() if title_tag else "Untitled Course"
            url = "https://www.coursera.org" + card['href']

            courses.append({
                'title': title,
                'platform': 'Coursera',
                'url': url
            })

    except Exception as e:
        print(f"[Coursera] Error: {e}")
        courses = [{
            'title': f"Explore {skill} courses on Coursera",
            'platform': 'Coursera',
            'url': f"https://www.coursera.org/search?query={skill}"
        }]

    return courses
