import os

from dotenv import load_dotenv
from google import genai
from pydantic import BaseModel


load_dotenv()

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)


class Question(BaseModel):
    type: str
    concept: str
    question: str
    options: list[str]
    correct_answer: int
    explanation: str


class Quiz(BaseModel):
    questions: list[Question]


def generate_quiz(passage: str) -> Quiz:

    prompt = f"""
Analyze ONLY the passage provided below.

IMPORTANT RULES:
- Use only information explicitly contained in the passage.
- Do not use knowledge from the broader book.
- Do not use outside knowledge.
- Do not introduce characters, events, arguments, or examples that are not present in the passage.
- Every question must be answerable using only the passage.
- The goal is to test whether the reader understood the author's reasoning, not whether they know the subject.

Generate exactly 5 questions.

The questions must test understanding, not simple memory.

1. Core argument
2. Conceptual distinction
3. Reasoning
4. Interpretation
5. Application

PASSAGE:
{passage}
"""

    response = client.models.generate_content(
        model="gemini-3.1-flash-lite",
        contents=prompt,
        config={
            "response_mime_type": "application/json",
            "response_schema": Quiz,
        },
    )

    return Quiz.model_validate_json(response.text)

