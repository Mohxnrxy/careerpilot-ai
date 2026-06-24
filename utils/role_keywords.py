import os
import json
from google import genai
from dotenv import load_dotenv

load_dotenv()

client = None

if os.getenv("GEMINI_API_KEY"):
    client = genai.Client(
        api_key=os.getenv("GEMINI_API_KEY")
    )

MODELS = [
    "gemini-2.5-flash-lite",
    "gemini-2.5-flash",
    "gemini-2.0-flash",
    "gemini-flash-latest"
]

def get_role_keywords(role):

    if not client:
        return [
            "Python",
            "SQL",
            "Git"
        ]

    prompt = f"""
    Give the top 20 technical skills,
    tools, technologies,
    certifications and keywords
    recruiters expect for:

    {role}

    Return ONLY a JSON array.

    Example:

    ["Python","SQL","Docker"]
    """

    for model_name in MODELS:

        try:

            response = client.models.generate_content(
                model=model_name,
                contents=prompt
            )

            text = response.text.strip()

            try:
                return json.loads(text)

            except:
                pass

        except Exception as e:

            print(
                f"Failed {model_name}: {e}"
            )

    return [
        "Python",
        "SQL",
        "Git",
        "Docker",
        "AWS",
        "Communication",
        "Leadership"
    ]