from google import genai
from dotenv import load_dotenv
import os
import json
import re

load_dotenv()

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)

MODELS = [
    "gemini-2.5-flash",
    "gemini-2.5-flash-lite",
    "gemini-2.5-pro",

    "gemini-3.5-flash",

    "gemini-3.1-pro-preview",
    "gemini-3.1-flash-lite",

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

            response = client.models.generate_content(
                model=model_name,
                contents=prompt
            )

            if response.text:
                return response.text

        except Exception as e:

            print(f"Failed: {model_name}")
            print(e)

            last_error = e

    raise Exception(
        f"All models failed: {last_error}"
    )


def extract_keywords(text):

    words = re.findall(r"\b[A-Za-z][A-Za-z0-9+#.-]+\b", text)

    ignore = {
        "and", "or", "the", "for", "with", "from",
        "that", "this", "have", "will", "your",
        "you", "our", "are", "into", "using",
        "years", "year", "experience", "ability",
        "required", "preferred"
    }

    keywords = []

    for word in words:
        if len(word) > 2 and word.lower() not in ignore:
            keywords.append(word)

    return list(set(keywords))


def match_jd(resume_text, job_description):

    resume_lower = resume_text.lower()

    jd_keywords = extract_keywords(
        job_description
    )

    matched = []
    missing = []

    for keyword in jd_keywords:

        if keyword.lower() in resume_lower:
            matched.append(keyword)
        else:
            missing.append(keyword)

    if len(jd_keywords) == 0:
        score = 0
    else:
        score = int(
            (len(matched) / len(jd_keywords)) * 100
        )

    prompt = f"""
You are an ATS recruiter.

Resume:
{resume_text}

Job Description:
{job_description}

Match Score: {score}

Matched Skills:
{matched[:25]}

Missing Skills:
{missing[:25]}

Return ONLY JSON:

{{
"suggestions":[
"...",
"...",
"..."
]
}}
"""

    suggestions = []

    try:

        text = generate_with_fallback(prompt).strip()

        text = text.replace("```json", "")
        text = text.replace("```", "")

        ai_result = json.loads(text)

        suggestions = ai_result.get(
            "suggestions",
            []
        )

    except Exception:

        suggestions = [
            "Add more keywords from the job description.",
            "Improve project descriptions.",
            "Include measurable achievements."
        ]

    return {
        "match_score": score,
        "score": score,
        "matching_skills": matched[:25],
        "matched": matched[:25],
        "missing_keywords": missing[:25],
        "missing": missing[:25],
        "suggestions": suggestions
    }