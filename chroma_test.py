import chromadb


# Create a local Chroma database
client = chromadb.PersistentClient(
    path="./chroma_db"
)


# Create a collection
collection = client.get_or_create_collection(
    name="deep_read"
)


# Add our book chunks
collection.upsert(
    ids=["chunk_1", "chunk_2", "chunk_3"],

    documents=[
        "People do not respond directly to events. Instead, they respond to the meaning they give to those events.",

        "This distinction helps explain why two people can experience the same event but react very differently.",

        "Past experiences therefore do not determine a person's future. What matters is how the person interprets those experiences."
    ],

    metadatas=[
        {"chapter": 1, "page": 1},
        {"chapter": 1, "page": 1},
        {"chapter": 1, "page": 2}
    ]
)


# Search the collection
results = collection.query(
    query_texts=[
        "Why can two people react differently to the same event?"
    ],
    n_results=2
)


print("\nRetrieved chunks:")

for document, distance, metadata in zip(
    results["documents"][0],
    results["distances"][0],
    results["metadatas"][0]
):

    print(f"\nDistance: {distance:.3f}")
    print(f"Text: {document}")
    print(f"Chapter: {metadata['chapter']}")
    print(f"Page: {metadata['page']}")
