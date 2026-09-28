import os
import json
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
            "task_type": "RETRIEVAL_DOCUMENT"
        }
    )

    return response.embeddings[0].values


# Load chunks
with open("chunks.json", "r") as file:
    chunks = json.load(file)


# Connect to Chroma
chroma = chromadb.PersistentClient(
    path="./book_chroma_db"
)

collection = chroma.get_or_create_collection(
    name="pride_and_prejudice"
)


# Process chunks one at a time
for chunk in chunks:

    chunk_id = chunk["id"]

    # Skip chunks already stored
    existing = collection.get(
        ids=[chunk_id]
    )

    if existing["ids"]:
        print(f"Skipping {chunk_id} — already stored")
        continue

    print(f"Embedding {chunk_id}...")

    embedding = get_embedding(
        chunk["text"]
    )

    collection.upsert(
        ids=[chunk_id],
        documents=[chunk["text"]],
        embeddings=[embedding]
    )

    print(f"Stored {chunk_id}")


print("\nDone!")
print(
    f"Chunks in Chroma: {collection.count()}"
)
