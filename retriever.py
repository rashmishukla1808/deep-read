import chromadb

from sentence_transformers import (
    SentenceTransformer,
    CrossEncoder
)


embedding_model = SentenceTransformer(
    "BAAI/bge-small-en-v1.5"
)

reranker = CrossEncoder(
    "BAAI/bge-reranker-base"
)

chroma_client = chromadb.PersistentClient(
    path="./chroma_db"
)


def retrieve_chunks(
    query,
    top_k=3,
    candidate_k=10
):

    # Get the current collection
    collection = chroma_client.get_collection(
        name="deep_read"
    )

    # Create query embedding
    query_embedding = embedding_model.encode(
        query,
        normalize_embeddings=True
    ).tolist()

    # Retrieve candidate chunks
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=candidate_k
    )

    candidates = results["documents"][0]

    # Rerank candidates
    pairs = [
        [query, document]
        for document in candidates
    ]

    scores = reranker.predict(pairs)

    ranked_results = list(
        zip(candidates, scores)
    )

    ranked_results.sort(
        key=lambda x: x[1],
        reverse=True
    )

    return ranked_results[:top_k]
