from pypdf import PdfReader


def is_usable_text(text: str) -> bool:
    words = text.split()

    if len(words) < 10:
        return False

    alphabetic_chars = sum(
        char.isalpha()
        for char in text
    )

    total_chars = len(text)

    if total_chars == 0:
        return False

    alphabetic_ratio = alphabetic_chars / total_chars

    return alphabetic_ratio >= 0.30


def extract_text_from_pdf(uploaded_file):

    reader = PdfReader(uploaded_file)

    pages = []
    skipped_pages = []

    for page_number, page in enumerate(reader.pages, start=1):

        text = page.extract_text() or ""

        if is_usable_text(text):
            pages.append(text)
        else:
            skipped_pages.append(page_number)

    print(
        f"Kept {len(pages)} pages."
    )

    print(
        f"Skipped {len(skipped_pages)} pages."
    )

    return "\n\n".join(pages)
