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

print(f"Total chunks: {len(chunks)}")

for i, chunk in enumerate(chunks[:5]):
    print(f"\n--- Chunk {i + 1} ---")
    print(chunk[:1000])
