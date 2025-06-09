def get_free_courses(skill: str) -> list:
    """Returns curated free courses for the skill"""
    courses = {
        "Python Developer": [
            {
                "title": "Python for Everybody",
                "platform": "Coursera",
                "url": "https://www.coursera.org/specializations/python",
                "free": True
            },
            {
                "title": "Learn Python 3",
                "platform": "Codecademy",
                "url": "https://www.codecademy.com/learn/learn-python-3",
                "free": True
            }
        ],
        "Data Analyst": [
            {
                "title": "Data Analysis with Python",
                "platform": "freeCodeCamp",
                "url": "https://www.freecodecamp.org/learn/data-analysis-with-python/",
                "free": True
            }
        ]
    }
    return courses.get(skill, [
        {
            "title": f"Introduction to {skill}",
            "platform": "Udemy",
            "url": "https://www.udemy.com",
            "free": True
        }
    ])