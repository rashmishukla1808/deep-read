import requests


def download_archive_pdf(identifier, output_file):

    url = f"https://archive.org/download/{identifier}/{identifier}.pdf"

    print(f"Downloading from:\n{url}")

    response = requests.get(url)

    response.raise_for_status()

    with open(output_file, "wb") as file:
        file.write(response.content)

    print(f"\nSaved to: {output_file}")


identifier = "prideprejudice00aust_5"

download_archive_pdf(
    identifier,
    "book.pdf"
)
