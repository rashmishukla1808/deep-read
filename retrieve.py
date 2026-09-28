import os
import json
import math

from dotenv import load_dotenv
from google import genai


# Load GEMINI_API_KEY from .env
load_dotenv()

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)


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


# Load our stored vector store

with open("vector_store.json", "r") as file:

    chunks = json.load(file)


# User's question

query = "Why can two people react differently to the same event?"


# Convert the question into an embedding

query_embedding = get_embedding(query)


# Compare the question with every stored chunk

results = []

for chunk in chunks:

    similarity = cosine_similarity(
        query_embedding,
        chunk["embedding"]
    )

    results.append({
        "text": chunk["text"],
        "chapter": chunk["chapter"],
        "page": chunk["page"],
        "similarity": similarity
    })


# Highest similarity first

results.sort(
    key=lambda x: x["similarity"],
    reverse=True
)


# Show the top 2 results

print("\nQuery:")
print(query)

print("\nRetrieved chunks:")

for result in results[:2]:

    print(
        f"\n{result['similarity']:.3f} → "
        f"{result['text']}"
    )

    print(
        f"Chapter: {result['chapter']}, "
        f"Page: {result['page']}"
    )
