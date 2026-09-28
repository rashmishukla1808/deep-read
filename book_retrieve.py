import os
import chromadb

from dotenv import load_dotenv
from google import genai

load_dotenv()

gemini = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)


def get_embedding(text):
    response = gemini.models.embed_content(
        model="gemini-embedding-001",
        contents=text,
        config={
            "task_type": "RETRIEVAL_QUERY"
        }
    )

    return response.embeddings[0].values


chroma = chromadb.PersistentClient(
    path="./book_chroma_db"
)

collection = chroma.get_collection(
    name="pride_and_prejudice"
)


query = "Why does Elizabeth initially dislike Mr. Darcy?"

query_embedding = get_embedding(query)


results = collection.query(
    query_embeddings=[query_embedding],
    n_results=5
)


print("\nQuery:")
print(query)

print("\nRetrieved passages:")

for document, distance in zip(
    results["documents"][0],
    results["distances"][0]
):
    print(f"\nDistance: {distance:.3f}")
    print(document[:1000])
