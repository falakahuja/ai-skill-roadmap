def get_community_resources(skill: str) -> list:
    """Returns relevant community resources"""
    skill_lower = skill.lower().replace(' ', '')
    return [
        {
            "type": "Subreddit",
            "name": f"r/{skill_lower}",
            "url": f"https://reddit.com/r/{skill_lower}"
        },
        {
            "type": "Discord",
            "name": f"{skill} Community",
            "url": "https://discord.com"
        },
        {
            "type": "Stack Overflow",
            "name": f"{skill} Questions",
            "url": f"https://stackoverflow.com/questions/tagged/{skill_lower}"
        }
    ]