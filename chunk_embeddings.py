import os
import math
from ingest_book import chunk_text
from dotenv import load_dotenv
from google import genai

load_dotenv()

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)
text = """
People do not respond directly to events. Instead, they respond
to the meaning they give to those events. This distinction helps
explain why two people can experience the same event but react
very differently.

Past experiences therefore do not determine a person's future.
What matters is how the person interprets those experiences.
"""

chunks = chunk_text(text)

def get_embedding(text):

    response = client.models.embed_content(
        model="gemini-embedding-001",
        contents=text
    )

    return response.embeddings[0].values


def cosine_similarity(vector_a, vector_b):

    dot_product = sum(
        a * b
        for a, b in zip(vector_a, vector_b)
    )

    magnitude_a = math.sqrt(
        sum(a * a for a in vector_a)
    )

    magnitude_b = math.sqrt(
        sum(b * b for b in vector_b)
    )

    return dot_product / (magnitude_a * magnitude_b)


# Create embeddings for all chunks

chunk_embeddings = []

for chunk in chunks:

    embedding = get_embedding(chunk)

    chunk_embeddings.append({
        "text": chunk,
        "embedding": embedding
    })


# Search query

query = "Why can two people react differently to the same event?"

query_embedding = get_embedding(query)


# Compare query with every chunk

results = []

for item in chunk_embeddings:

    similarity = cosine_similarity(
        query_embedding,
        item["embedding"]
    )

    results.append({
        "text": item["text"],
        "similarity": similarity
    })


# Most relevant first

results.sort(
    key=lambda x: x["similarity"],
    reverse=True
)


print("\nQuery:")
print(query)

print("\nRetrieved chunks:")

for result in results:

    print(
        f"\n{result['similarity']:.3f} → "
        f"{result['text']}"
    )

# Retrieve the top 2 chunks

top_chunks = results[:2]

context = "\n\n".join(
    result["text"]
    for result in top_chunks
)


# Ask Gemini to answer using ONLY the retrieved context

prompt = f"""
Answer the question using ONLY the context provided below.

Do not use outside knowledge.
If the answer cannot be determined from the context, say:
"I don't have enough information."

CONTEXT:
{context}

QUESTION:
{query}
"""


response = client.models.generate_content(
    model="gemini-3.1-flash-lite",
    contents=prompt
)


print("\n\nGenerated answer:")
print(response.text)
