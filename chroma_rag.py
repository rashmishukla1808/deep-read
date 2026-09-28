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
    path="./chroma_rag_db"
)

collection = chroma.get_or_create_collection(
    name="deep_read_rag"
)


# -------------------------
# 3. BOOK CHUNKS
# -------------------------

documents = [
    "People do not respond directly to events. Instead, they respond to the meaning they give to those events.",

    "This distinction helps explain why two people can experience the same event but react very differently.",

    "Past experiences therefore do not determine a person's future. What matters is how the person interprets those experiences."
]


# -------------------------
# 4. EMBED + STORE DOCUMENTS
# -------------------------

embeddings = []

for document in documents:

    embedding = get_embedding(
        document,
        "RETRIEVAL_DOCUMENT"
    )

    embeddings.append(embedding)


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
# 5. USER QUESTION
# -------------------------

query = "Why can two people react differently to the same event?"


# -------------------------
# 6. EMBED QUESTION
# -------------------------

query_embedding = get_embedding(
    query,
    "RETRIEVAL_QUERY"
)


# -------------------------
# 7. RETRIEVE RELEVANT CHUNKS
# -------------------------

results = collection.query(
    query_embeddings=[query_embedding],
    n_results=2
)


retrieved_documents = results["documents"][0]


# -------------------------
# 8. BUILD CONTEXT
# -------------------------

context = "\n\n".join(
    retrieved_documents
)


# -------------------------
# 9. GENERATE ANSWER
# -------------------------

prompt = f"""
Answer the question using ONLY the context below.

Do not use outside knowledge.

If the context does not contain enough information to answer,
say: "I don't have enough information."

CONTEXT:
{context}

QUESTION:
{query}
"""


response = gemini.models.generate_content(
    model="gemini-3.1-flash-lite",
    contents=prompt
)


# -------------------------
# 10. PRINT RESULT
# -------------------------

print("\nQuestion:")
print(query)

print("\nRetrieved context:")
print(context)

print("\nGenerated answer:")
print(response.text)
