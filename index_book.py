import os

import chromadb
from dotenv import load_dotenv
from google import genai

from book_chunker import chunk_text


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


# Chroma database

chroma_client = chromadb.PersistentClient(
    path="./chroma_db"
)


collection = chroma_client.get_or_create_collection(
    name="deep_read"
)


# For now, use a text file as our book input

with open("book.txt", "r") as file:

    text = file.read()


# Chunk the book

chunks = chunk_text(text)


# Create embeddings and store them

for i, chunk in enumerate(chunks):

    embedding = get_embedding(chunk)

    collection.add(
        ids=[f"chunk_{i}"],
        documents=[chunk],
        embeddings=[embedding],
        metadatas=[
            {
                "chunk_id": i
            }
        ]
    )


print(f"Indexed {len(chunks)} chunks.")

print("Chroma database saved to ./chroma_db")
