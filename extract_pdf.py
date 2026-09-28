from pypdf import PdfReader

reader = PdfReader("book.pdf")

text = ""

for page in reader.pages:
    text += page.extract_text() + "\n"

print(text[:5000])
