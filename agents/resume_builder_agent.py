from google import genai
from dotenv import load_dotenv
import os

load_dotenv()

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)

def build_resume(resume_text, target_role):

    prompt = f"""
You are an expert Resume Writer.

Target Role:
{target_role}

Resume:
{resume_text}

Create a professional ATS-friendly resume.

Include:

1. Professional Summary
2. Technical Skills
3. Projects
4. Certifications
5. Education
6. Achievements

Return clean markdown.
"""

    response = client.models.generate_content(
        model="gemini-2.5-flash-lite",
        contents=prompt
    )

    return response.text