import os
import json

import chromadb
from dotenv import load_dotenv
from google import genai


# Load environment variables
load_dotenv()

gemini = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)


# Create query embedding
def get_embedding(text):

    response = gemini.models.embed_content(
        model="gemini-embedding-001",
        contents=text,
        config={
            "task_type": "RETRIEVAL_QUERY"
        }
    )

    return response.embeddings[0].values


# Load Chroma
chroma = chromadb.PersistentClient(
    path="./chroma_rag_db"
)

collection = chroma.get_collection(
    name="deep_read_rag"
)


# Load evaluation cases
with open("evals/retrieval_cases.json", "r") as file:
    test_cases = json.load(file)


K = 2

recall_hits = 0
precision_scores = []


# Run evaluation
for test in test_cases:

    query = test["query"]

    expected = set(
        test["expected_chunk_ids"]
    )

    query_embedding = get_embedding(query)

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=K
    )

    retrieved_ids = set(
        results["ids"][0]
    )

    relevant_retrieved = expected.intersection(
        retrieved_ids
    )

    # Recall@K
    if relevant_retrieved:
        recall_hits += 1
        result = "PASS"
    else:
        result = "FAIL"

    # Precision@K
    precision = len(relevant_retrieved) / K

    precision_scores.append(precision)

    print(f"\n{test['id']}")
    print(f"Query: {query}")
    print(f"Expected: {expected}")
    print(f"Retrieved: {retrieved_ids}")
    print(f"Relevant retrieved: {relevant_retrieved}")
    print(f"Precision@{K}: {precision:.0%}")
    print(f"Result: {result}")


# Calculate final metrics
recall_at_k = recall_hits / len(test_cases)

precision_at_k = sum(
    precision_scores
) / len(precision_scores)


print(
    f"\nRecall@{K}: "
    f"{recall_at_k:.0%}"
)

print(
    f"Precision@{K}: "
    f"{precision_at_k:.0%}"
)
