import os

import chromadb
from dotenv import load_dotenv
from google import genai


# -------------------------
# 1. SET UP GEMINI
# -------------------------

load_dotenv()

gemini = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)
def get_embedding(text, task_type):

    response = gemini.models.embed_content(
        model="gemini-embedding-001",
        contents=text,
        config={
            "task_type": task_type
        }
    )

    return response.embeddings[0].values
# -------------------------
# 2. SET UP CHROMA
# -------------------------

chroma = chromadb.PersistentClient(
    path="./chroma_gemini_db"
)

collection = chroma.get_or_create_collection(
    name="deep_read_gemini"
)


# -------------------------
# 3. OUR BOOK CHUNKS
# -------------------------

documents = [
    "People do not respond directly to events. Instead, they respond to the meaning they give to those events.",

    "This distinction helps explain why two people can experience the same event but react very differently.",

    "Past experiences therefore do not determine a person's future. What matters is how the person interprets those experiences."
]


# -------------------------
# 4. CREATE EMBEDDINGS
# -------------------------

embeddings = []

for document in documents:

    embedding = get_embedding(document,"RETRIEVAL_DOCUMENT")

    embeddings.append(embedding)


# -------------------------
# 5. STORE THEM IN CHROMA
# -------------------------

collection.upsert(
    ids=[
        "chunk_1",
        "chunk_2",
        "chunk_3"
    ],

    documents=documents,

    embeddings=embeddings,

    metadatas=[
        {"chapter": 1, "page": 1},
        {"chapter": 1, "page": 1},
        {"chapter": 1, "page": 2}
    ]
)


# -------------------------
# 6. EMBED USER QUERY
# -------------------------

query = "Why can two people react differently to the same event?"

query_embedding = get_embedding(query,"RETRIEVAL_QUERY")

# -------------------------
# 7. ASK CHROMA TO SEARCH
# -------------------------

results = collection.query(
    query_embeddings=[query_embedding],
    n_results=2
)


# -------------------------
# 8. PRINT RESULTS
# -------------------------

print("\nQuery:")
print(query)

print("\nRetrieved chunks:")

for document, distance, metadata in zip(
    results["documents"][0],
    results["distances"][0],
    results["metadatas"][0]
):

    print(f"\nDistance: {distance:.3f}")
    print(f"Text: {document}")
    print(
        f"Chapter: {metadata['chapter']}, "
        f"Page: {metadata['page']}"
    )
