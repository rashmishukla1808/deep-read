import os
import json

from dotenv import load_dotenv
from google import genai

load_dotenv()

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)


chunks = [
    {
        "text": "People do not respond directly to events. Instead, they respond to the meaning they give to those events.",
        "chapter": 1,
        "page": 1
    },
    {
        "text": "This distinction helps explain why two people can experience the same event but react very differently.",
        "chapter": 1,
        "page": 1
    },
    {
        "text": "Past experiences therefore do not determine a person's future. What matters is how the person interprets those experiences.",
        "chapter": 1,
        "page": 2
    }
]


def get_embedding(text):

    response = client.models.embed_content(
        model="gemini-embedding-001",
        contents=text
    )

    return response.embeddings[0].values


for chunk in chunks:

    chunk["embedding"] = get_embedding(chunk["text"])


with open("vector_store.json", "w") as file:

    json.dump(
        chunks,
        file,
        indent=2
    )


print("Vector store created!")
