from google import genai
from dotenv import load_dotenv
import os

load_dotenv()

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)

def generate_interview_questions(
    resume_text,
    target_role
):

    prompt = f"""
You are an expert technical interviewer.

Generate:

1. 5 Technical Interview Questions
2. 5 HR Interview Questions
3. 5 Project-Based Questions

based on the resume.

Target Role:
{target_role}

Resume:
{resume_text}

Return clean markdown.
"""

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )

    return response.text