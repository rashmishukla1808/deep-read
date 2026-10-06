import streamlit as st
import chromadb
from sentence_transformers import SentenceTransformer

from pdf_parser import extract_text_from_pdf
from book_chunker import chunk_text
from rag_generator import answer_question


# -----------------------------
# Models and database
# -----------------------------

embedding_model = SentenceTransformer(
    "BAAI/bge-small-en-v1.5"
)

chroma_client = chromadb.PersistentClient(
    path="./chroma_db"
)


def get_collection():
    return chroma_client.get_or_create_collection(
        name="deep_read"
    )


# -----------------------------
# Page
# -----------------------------

st.title("Deep Read 📖")

st.write(
    "Upload a book and test whether you actually understood what you read."
)


# -----------------------------
# Upload book
# -----------------------------

uploaded_file = st.file_uploader(
    "Upload your book",
    type=["pdf"]
)


if uploaded_file is not None:

    st.success(
        f"Uploaded: {uploaded_file.name}"
    )

    # -----------------------------
    # Process book
    # -----------------------------

    if st.button("Process Book"):

        with st.spinner(
            "Extracting text from your book..."
        ):

            text = extract_text_from_pdf(
                uploaded_file
            )

        if not text.strip():

            st.error(
                "No text could be extracted from this PDF. "
                "It may be a scanned/image-based PDF."
            )

            st.stop()

        st.success(
            f"Extracted approximately "
            f"{len(text.split()):,} words."
        )


        # -----------------------------
        # Chunk book
        # -----------------------------

        with st.spinner(
            "Splitting book into chunks..."
        ):

            chunks = chunk_text(text)

        st.success(
            f"Created {len(chunks):,} chunks."
        )


        # -----------------------------
        # Create embeddings
        # -----------------------------

        with st.spinner(
            "Creating local embeddings..."
        ):

            embeddings = embedding_model.encode(
                chunks,
                normalize_embeddings=True,
                show_progress_bar=False
            )


        # -----------------------------
        # Create fresh Chroma index
        # -----------------------------

        try:

            chroma_client.delete_collection(
                name="deep_read"
            )

        except Exception:

            pass


        collection = chroma_client.create_collection(
            name="deep_read"
        )


        # -----------------------------
        # Store chunks
        # -----------------------------

        with st.spinner(
            "Indexing your book..."
        ):

            ids = [
                f"{uploaded_file.name}_{i}"
                for i in range(len(chunks))
            ]

            metadatas = [
                {
                    "book": uploaded_file.name,
                    "chunk_id": i
                }
                for i in range(len(chunks))
            ]

            collection.add(
                ids=ids,
                documents=chunks,
                embeddings=embeddings.tolist(),
                metadatas=metadatas
            )


        st.success(
            f"Book indexed successfully! "
            f"{len(chunks):,} chunks stored."
        )


        # -----------------------------
        # Preview extracted text
        # -----------------------------

        with st.expander(
            "Preview extracted text"
        ):

            st.text(
                text[:5000]
            )


        # -----------------------------
        # Preview chunks
        # -----------------------------

        with st.expander(
            "Preview chunks"
        ):

            for i, chunk in enumerate(
                chunks[:3]
            ):

                st.write(
                    f"### Chunk {i + 1}"
                )

                st.write(chunk)


# -----------------------------
# Ask questions
# -----------------------------

st.divider()

st.subheader(
    "Ask a question about the book"
)

question = st.text_input(
    "What would you like to understand?"
)


if st.button("Ask") and question:

    with st.spinner(
        "Thinking..."
    ):

        answer = answer_question(
            question
        )

    st.subheader(
        "Answer"
    )

    st.write(
        answer
    )
