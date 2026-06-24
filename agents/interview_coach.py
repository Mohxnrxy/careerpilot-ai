from google import genai
from dotenv import load_dotenv
import os
import json
from utils.role_keywords import get_role_keywords

load_dotenv()

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)

MODELS = [
    "gemini-2.5-flash",
    "gemini-2.5-flash-lite",
    "gemini-2.0-flash",
    "gemini-flash-latest"
]


def generate_mcq_interview(role):

    keywords = get_role_keywords(role)

    prompt = f"""
You are a senior technical interviewer.

Generate EXACTLY 10 professional multiple-choice interview questions for:

ROLE: {role}

Key Skills Expected:
{keywords}

Requirements:

- Questions must be specific to the role.
- Difficulty: Intermediate to Advanced.
- Focus on real interview topics.
- Use the skills listed above.
- 4 options per question.
- Only one correct answer.
- Return EXACTLY 10 questions.
- Return ONLY valid JSON.

Format:

[
    {{
        "question":"...",
        "options":[
            "...",
            "...",
            "...",
            "..."
        ],
        "answer":"..."
    }}
]
"""

    last_error = None

    for model_name in MODELS:

        try:

            response = client.models.generate_content(
                model=model_name,
                contents=prompt
            )

            text = response.text.strip()

            text = text.replace(
                "```json",
                ""
            )

            text = text.replace(
                "```",
                ""
            )

            print("\n===== GEMINI RESPONSE =====")
            print(text)
            print("===========================\n")

            questions = json.loads(text)

            if isinstance(
                questions,
                list
            ) and len(questions) > 0:

                return questions

        except Exception as e:

            print(
                f"Failed: {model_name}"
            )

            print(e)

            last_error = e

    print(
        "Interview Generation Error:",
        last_error
    )

    return [
        {
            "question":
            "What is Python?",

            "options": [
                "Programming Language",
                "Database",
                "Browser",
                "Operating System"
            ],

            "answer":
            "Programming Language"
        }
    ]


def calculate_score(
    questions,
    user_answers
):

    score = 0

    detailed_results = []

    for i, question in enumerate(
        questions
    ):

        user_answer = user_answers.get(
            str(i),
            ""
        )

        correct_answer = question[
            "answer"
        ]

        is_correct = (
            user_answer
            ==
            correct_answer
        )

        if is_correct:
            score += 1

        detailed_results.append(
            {
                "question":
                question["question"],

                "selected":
                user_answer,

                "correct":
                correct_answer,

                "is_correct":
                is_correct
            }
        )

    percentage = int(
        (score / len(questions))
        * 100
    )

    return {
        "score": score,
        "total": len(questions),
        "percentage": percentage,
        "details": detailed_results
    }