# roadmap_generator.py

import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

model = genai.GenerativeModel(model_name="models/gemini-2.0-flash")

def generate_roadmap(role: str, experience: str, weeks: int) -> str:
    prompt = f"""
You are a professional tech mentor.

Create a **{weeks}-week skill development roadmap** for someone aiming to become a **{role}**. The person is currently at a **{experience}** level.

Break the roadmap week-wise, with clear tasks, technologies, and learning goals. Ensure each week is practical and builds upon the previous.

Include:
- Tools/Technologies to learn
- Concepts to master
- Project ideas (as milestones)
- Optional resources or certifications

The response should be well-structured like:

### Week 1
- Task 1
- Task 2

### Week 2
- Task 1
...

Make it skimmable, engaging, and professional.
"""
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"❌ Error generating roadmap: {e}"
