from google import genai
from dotenv import load_dotenv
import os

load_dotenv()

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)

def generate_cover_letter(resume_text, target_role):

    prompt = f"""
Create a professional cover letter.

Target Role:
{target_role}

Resume:
{resume_text}

Requirements:
- Professional format
- 300-400 words
- Mention candidate strengths
- Mention relevant skills
- Explain why candidate is suitable
- End with a professional closing
"""

    response = client.models.generate_content(
        model="gemini-2.5-flash-lite",
        contents=prompt
    )

    return response.text