text = """
People do not respond directly to events. Instead, they respond
to the meaning they give to those events. This distinction helps
explain why two people can experience the same event but react
very differently.

Past experiences therefore do not determine a person's future.
What matters is how the person interprets those experiences.
"""


chunk_size = 20
overlap = 5


words = text.split()

chunks = []

start = 0

while start < len(words):

    end = start + chunk_size

    chunk = words[start:end]

    chunks.append(" ".join(chunk))

    start += chunk_size - overlap


for i, chunk in enumerate(chunks):

    print(f"\n--- Chunk {i + 1} ---")
    print(chunk)
