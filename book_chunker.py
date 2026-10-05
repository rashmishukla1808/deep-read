def chunk_text(text, chunk_size=500, overlap=100):

    paragraphs = text.strip().split("\n\n")

    chunks = []

    for paragraph in paragraphs:

        words = paragraph.split()

        if len(words) <= chunk_size:

            chunks.append(paragraph)

        else:

            start = 0

            while start < len(words):

                end = start + chunk_size

                chunk = words[start:end]

                chunks.append(" ".join(chunk))

                start += chunk_size - overlap

    return chunks
