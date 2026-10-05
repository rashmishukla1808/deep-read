import os

import streamlit as st
import chromadb

from dotenv import load_dotenv
from google import genai

from pdf_parser import extract_text_from_pdf
from book_chunker import chunk_text


# Load environment variables
load_dotenv()

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)


# Chroma database
chroma_client = chromadb.PersistentClient(
    path="./chroma_db"
)

collection = chroma_client.get_or_create_collection(
    name="deep_read"
)


def get_embedding(text):

    response = client.models.embed_content(
        model="gemini-embedding-001",
        contents=text
    )

    return response.embeddings[0].values


# -------------------------
# UI
# -------------------------

st.title("Deep Read 📖")

st.write(
    "Upload a book and test whether you actually understood what you read."
)


uploaded_file = st.file_uploader(
    "Upload your book",
    type=["pdf"]
)


if uploaded_file is not None:

    st.success(f"Uploaded: {uploaded_file.name}")


    if st.button("Process Book"):

        # 1. Extract text

        with st.spinner("Extracting text from your book..."):

            text = extract_text_from_pdf(uploaded_file)


        if not text.strip():

            st.error(
                "No text could be extracted from this PDF. "
                "It may be a scanned/image-based PDF."
            )

            st.stop()


        st.success(
            f"Extracted approximately {len(text.split()):,} words."
        )


        # 2. Chunk the book

        with st.spinner("Splitting book into chunks..."):

            chunks = chunk_text(text)


        st.success(
            f"Created {len(chunks):,} chunks."
        )


        # 3. Generate embeddings and store in Chroma

        with st.spinner(
            "Creating embeddings and indexing your book..."
        ):

            for i, chunk in enumerate(chunks):

                embedding = get_embedding(chunk)

                collection.add(
                    ids=[f"{uploaded_file.name}_{i}"],
                    documents=[chunk],
                    embeddings=[embedding],
                    metadatas=[
                        {
                            "book": uploaded_file.name,
                            "chunk_id": i
                        }
                    ]
                )


        st.success(
            f"Book indexed successfully! "
            f"{len(chunks):,} chunks stored."
        )


        # 4. Preview extracted text

        with st.expander("Preview extracted text"):

            st.text(text[:5000])


        # 5. Preview chunks

        with st.expander("Preview chunks"):

            for i, chunk in enumerate(chunks[:3]):

                st.write(f"### Chunk {i + 1}")

                st.write(chunk)
