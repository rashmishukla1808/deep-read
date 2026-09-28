import os
import math

from dotenv import load_dotenv
from google import genai


load_dotenv()

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)


documents = [
    "A dog is running through a park.",
    "A puppy is playing outside.",
    "The stock market closed higher today."
]

query = "What is happening with the animal?"


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


query_embedding = get_embedding(query)


results = []

for document in documents:

    document_embedding = get_embedding(document)

    similarity = cosine_similarity(
        query_embedding,
        document_embedding
    )

    results.append(
        (document, similarity)
    )


results.sort(
    key=lambda x: x[1],
    reverse=True
)


print("Query:", query)

print("\nMost relevant documents:\n")

for document, similarity in results:

    print(
        f"{similarity:.3f} → {document}"
    )
