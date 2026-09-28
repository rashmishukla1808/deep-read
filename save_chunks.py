import json
from pypdf import PdfReader


def extract_text_from_pdf(filename):
    reader = PdfReader(filename)

    text = ""

    for page in reader.pages:
        page_text = page.extract_text()

        if page_text:
            text += page_text + "\n\n"

    return text


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


text = extract_text_from_pdf("book.pdf")
chunks = chunk_text(text)

chunk_data = []

for i, chunk in enumerate(chunks):
    chunk_data.append({
        "id": f"chunk_{i + 1}",
        "text": chunk
    })


with open("chunks.json", "w") as file:
    json.dump(chunk_data, file, indent=2)


print(f"Saved {len(chunk_data)} chunks to chunks.json")
