import os
from dotenv import load_dotenv
import google.generativeai as genai
from typing import Optional

load_dotenv()

def generate_roadmap(role: str, experience: str, weeks: int) -> str:
    """
    Generates a skill development roadmap using Gemini API
    """
    try:
        genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
        model = genai.GenerativeModel(model_name="models/gemini-2.0-flash")

        prompt = f"""
You are an expert curriculum designer.

Create a structured {weeks}-week skill development roadmap for a person learning to become a **{role}** at **{experience}** level.

Format it **exactly like this** using Markdown:

### Week 1
**Topic**: [Topic Title]

**Concepts**:
- Concept 1
- Concept 2

**Practice**:
- Practice Task 1
- Practice Task 2

**Resources**:
- Resource Title 1 - (https://resource-link.com)
- Resource Title 2

Rules to follow:
1. Each week must begin with `### Week X` followed by `**Topic**: ...` on the next line.
2. Write section headers exactly as: `**Concepts**:`, `**Practice**:`, `**Resources**:` — bold, colon, new line.
3. Use `-` (dash) for bullet points with no extra spacing or indentation.
4. Do not include extra markdown like blockquotes, headers (##, ### inside sections), tables, or inline code.
5. Keep formatting simple and consistent across all weeks.

Your output should be clean and directly renderable in a web UI.
"""

        response = model.generate_content(prompt)
        return response.text

    except Exception as e:
        return f"Error generating roadmap: {str(e)}"
