from google import genai
from dotenv import load_dotenv
import os

load_dotenv()

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)

def generate_roadmap(resume_text, target_role):

    prompt = f"""
You are an expert career coach.

Target Role:
{target_role}

Resume:
{resume_text}

Create a detailed 30-day roadmap.

Format:

Week 1:
- Topics
- Skills
- Resources

Week 2:
- Topics
- Skills
- Resources

Week 3:
- Topics
- Skills
- Resources

Week 4:
- Topics
- Skills
- Resources

Final Project:
- Project idea
- Technologies
- Portfolio tips
"""

    try:

        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )

        return response.text

    except Exception as e:

        return f"""
# ⚠️ Roadmap Service Temporarily Busy

Google Gemini is currently experiencing high demand.

Error:

{str(e)}

Please wait a few minutes and try again.

Meanwhile you can:
- Analyze another resume
- Generate interview questions
- Explore career recommendations
"""