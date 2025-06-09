def get_project_ideas(skill: str, level: str) -> list:
    """Returns level-appropriate project ideas"""
    projects = {
        "Beginner": [
            f"Build a basic {skill} CLI application",
            f"Create a simple {skill} calculator",
            f"Develop a {skill} todo list manager"
        ],
        "Intermediate": [
            f"Create a {skill} web scraper",
            f"Build a {skill} REST API",
            f"Develop a {skill} data visualization dashboard"
        ],
        "Advanced": [
            f"Build a machine learning model with {skill}",
            f"Create a distributed {skill} application",
            f"Develop a {skill} performance benchmarking tool"
        ]
    }
    return projects.get(level, [
        f"Build a {skill} portfolio project",
        f"Create a {skill} tutorial for others",
        f"Develop a {skill} automation script"
    ])