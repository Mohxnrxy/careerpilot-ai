from google import genai
from dotenv import load_dotenv
import os
import json
import re

load_dotenv()

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)

# -----------------------------
# MODELS (TRY IN ORDER)
# -----------------------------

MODELS = [
    "gemini-2.5-flash",
    "gemini-2.5-flash-lite",
    "gemini-2.5-pro",

    "gemini-3.5-flash",

    "gemini-3.1-flash-lite",
    "gemini-3.1-pro-preview",

    "gemini-3-flash-preview",
    "gemini-3-pro-preview",

    "gemini-2.0-flash",
    "gemini-2.0-flash-lite",

    "gemini-flash-latest",
    "gemini-flash-lite-latest",
    "gemini-pro-latest"
]


def generate_with_fallback(prompt):

    last_error = None

    for model_name in MODELS:

        try:

            print(f"Trying model: {model_name}")

            response = client.models.generate_content(
                model=model_name,
                contents=prompt
            )

            if hasattr(response, "text") and response.text:

                print(f"Success: {model_name}")
                return response.text

        except Exception as e:

            print(f"Failed: {model_name}")
            print(str(e))

            last_error = e

    raise last_error


def analyze_resume(resume_text, target_role):

    prompt = f"""
You are an Expert ATS Resume Analyzer and Career Coach.

Target Role:
{target_role}

Resume:
{resume_text}

Return ONLY valid JSON.

{{
    "ats_score": 0,
    "skills_found": [],
    "missing_skills": [],
    "strengths": [],
    "recommendations": [],
    "interview_questions": [],
    "jobs": [],
    "roadmap": {{
        "week1": {{
            "goal": "",
            "topics": [],
            "daily_tasks": [],
            "project": ""
        }},
        "week2": {{
            "goal": "",
            "topics": [],
            "daily_tasks": [],
            "project": ""
        }},
        "week3": {{
            "goal": "",
            "topics": [],
            "daily_tasks": [],
            "project": ""
        }},
        "week4": {{
            "goal": "",
            "topics": [],
            "daily_tasks": [],
            "project": "",
            "interview_prep": "",
            "linkedin_tasks": "",
            "github_tasks": "",
            "internship_applications": ""
        }}
    }}
}}

Instructions:

1. ATS score out of 100.
2. Top 15 skills found.
3. Top 10 missing skills.
4. Top 5 strengths.
5. Top 5 recommendations.
6. Generate exactly 20 interview questions tailored to:
   - The user's resume
   - The selected target role
   - Missing skills identified
   - Projects mentioned in the resume
   Mix:
   - Technical questions
   - Scenario-based questions
   - Project-based questions
   - Behavioral questions
   Return exactly 20 interview questions.
7. Top 5 matching job titles.
8. Create a detailed 30-day roadmap.

Return ONLY JSON.
"""

    try:

        text = generate_with_fallback(prompt).strip()

        print("\n========== GEMINI RESPONSE ==========")
        print(text)
        print("=====================================\n")

        text = re.sub(
            r"```json",
            "",
            text,
            flags=re.IGNORECASE
        )

        text = re.sub(
            r"```",
            "",
            text
        )

        text = text.strip()

        match = re.search(
            r"\{.*\}",
            text,
            re.DOTALL
        )

        if not match:
            raise ValueError(
                "No valid JSON found."
            )

        text = match.group()

        return json.loads(text)

    except Exception as e:

        print("\nResume Agent Error")
        print(str(e))

        return {
            "ats_score": 70,
            "skills_found": [],
            "missing_skills": [],
            "strengths": [],
            "recommendations": [
                "AI quota exceeded.",
                "Try again later.",
                "Add billing to Gemini API.",
                "Use another Gemini API key.",
                "Switch to Groq/OpenRouter."
            ],
            "interview_questions": [],
            "jobs": [],
            "roadmap": {
                "week1": {
                    "goal": "Learn Fundamentals",
                    "topics": [],
                    "daily_tasks": [],
                    "project": ""
                },
                "week2": {
                    "goal": "Build Core Skills",
                    "topics": [],
                    "daily_tasks": [],
                    "project": ""
                },
                "week3": {
                    "goal": "Advanced Concepts",
                    "topics": [],
                    "daily_tasks": [],
                    "project": ""
                },
                "week4": {
                    "goal": "Interview Preparation",
                    "topics": [],
                    "daily_tasks": [],
                    "project": "",
                    "interview_prep": "",
                    "linkedin_tasks": "",
                    "github_tasks": "",
                    "internship_applications": ""
                }
            }
        }