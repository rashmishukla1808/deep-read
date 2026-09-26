import os

from dotenv import load_dotenv
from google import genai
from pydantic import BaseModel


load_dotenv()

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)


class GroundednessResult(BaseModel):
    grounded: bool


def evaluate_groundedness(passage, question):

    prompt = f"""
You are evaluating whether a quiz question is grounded in a passage.

A question is GROUNDED if a careful reader can answer it using
only information contained in the passage.

A question is NOT GROUNDED if answering it requires:
- outside knowledge
- information not present in the passage
- knowledge about the author, theory, person, or historical context
  that is not stated in the passage

PASSAGE:
{passage}

QUESTION:
{question}

Return whether the question is grounded.
"""

    response = client.models.generate_content(
        model="gemini-3.1-flash-lite",
        contents=prompt,
        config={
            "response_mime_type": "application/json",
            "response_schema": GroundednessResult,
        },
    )

    result = GroundednessResult.model_validate_json(response.text)

    print(f"Judge response: {result.grounded}")

    return result.grounded
