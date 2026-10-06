import os

from dotenv import load_dotenv
from google import genai

from retriever import retrieve_chunks


load_dotenv()

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)


def answer_question(question: str) -> str:

    # 1. Retrieve + rerank relevant passages
    results = retrieve_chunks(
        question,
        top_k=3,
        candidate_k=10
    )

    # 2. Build context from the best passages
    context = "\n\n".join(
        chunk
        for chunk, score in results
    )

    # 3. Ask Gemini to answer using only the book
    prompt = f"""
You are answering a reader's question about a book.

Use ONLY the passages provided below.

Rules:
- Do not use outside knowledge.
- Do not invent information.
- If the passages do not contain enough information,
  say that the available passages are insufficient.
- Give a clear, concise answer.
- Explain your reasoning when useful.

BOOK PASSAGES:
{context}

READER QUESTION:
{question}
"""

    response = client.models.generate_content(
        model="gemini-3.1-flash-lite",
        contents=prompt
    )

    return response.text
