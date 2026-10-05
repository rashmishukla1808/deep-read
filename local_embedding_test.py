from sentence_transformers import SentenceTransformer


model = SentenceTransformer(
    "BAAI/bge-small-en-v1.5"
)


texts = [
    "A dog is running through a park.",
    "A puppy is playing outside.",
    "The stock market closed higher today."
]


embeddings = model.encode(texts)


for text, embedding in zip(texts, embeddings):

    print("\nText:")
    print(text)

    print("Embedding dimensions:")
    print(len(embedding))

    print("First 5 values:")
    print(embedding[:5])
