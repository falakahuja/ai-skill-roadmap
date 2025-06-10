import os
from typing import List
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()

def get_project_ideas(skill: str, level: str) -> List[str]:
    """Get AI-generated project ideas using Gemini API with strict formatting"""
    try:
        genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        prompt = f"""
        Generate exactly 3 project ideas for {skill} at {level} level.

        RULES:
        1. Format each idea EXACTLY like this:
            [Project Name]: [1-sentence description] (Main Technology)

        2. Requirements:
           - Must include concrete technologies/frameworks
           - Must match {level} difficulty
           - No Markdown formatting (plain text only)

        3. Example Output:
           - E-Commerce API: Build REST endpoints for products (Node.js, Express)
           - Weather Dashboard: Display forecasts with charts (React, Chart.js)
           - PDF Analyzer: Extract text and keywords (Python, PyPDF2)

        Generate for {skill} at ({level}) level:
        """

        response = model.generate_content(
            prompt,
            generation_config={
                "temperature": 0.7,
                "max_output_tokens": 300
            }
        )


        raw_response = response.text.strip()
        print("[DEBUG] Gemini Response:\n", raw_response)

        ideas = []
        for line in raw_response.split('\n'):
            line = line.strip()
            if ':' in line and any(char.isalpha() for char in line):
                ideas.append(line)
                if len(ideas) >= 3:
                    break

        return ideas if ideas else get_fallback_projects(skill, level)

    except Exception as e:
        print(f"Project generation error: {str(e)}")
        return get_fallback_projects(skill, level)

def get_fallback_projects(skill: str, level: str) -> List[str]:
    return [
        f"- {skill} Portfolio: Showcase your work (HTML, CSS)",
        f"- API Integration: Connect to a public API ({skill}, Requests)",
        f"- Data Analyzer: Process sample datasets ({skill}, Pandas)"
    ]
