import os
import shutil

import chromadb

from dotenv import load_dotenv
from openai import OpenAI
from pypdf import PdfReader


# ==========================================
# ENVIRONMENT
# ==========================================

load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")

if not api_key:
    raise RuntimeError(
        "OPENAI_API_KEY is missing from .env file"
    )

client = OpenAI(api_key=api_key)


# ==========================================
# PATHS
# ==========================================

KNOWLEDGE_DIR = os.getenv(
    "KNOWLEDGE_DIR",
    os.path.abspath(
        os.path.join(os.path.dirname(__file__), "../knowledge")
    )
)
CHROMA_DIR = "./chroma_db"


# ==========================================
# TEXT EXTRACTION
# ==========================================

def read_txt(file_path):

    with open(
        file_path,
        "r",
        encoding="utf-8"
    ) as file:

        return file.read()


def read_pdf(file_path):

    reader = PdfReader(file_path)

    pages = []

    for page in reader.pages:

        text = page.extract_text()

        if text:
            pages.append(text)

    return "\n".join(pages)


def read_document(file_path):

    extension = os.path.splitext(
        file_path
    )[1].lower()

    if extension == ".txt":

        return read_txt(file_path)

    if extension == ".pdf":

        return read_pdf(file_path)

    return ""


# ==========================================
# CHUNKING
# ==========================================

def create_chunks(
    text,
    chunk_size=1000,
    overlap=200
):

    text = text.strip()

    if not text:
        return []

    chunks = []

    start = 0

    while start < len(text):

        end = start + chunk_size

        chunk = text[start:end].strip()

        if chunk:
            chunks.append(chunk)

        start += chunk_size - overlap

    return chunks


# ==========================================
# EMBEDDINGS
# ==========================================

def create_embeddings(texts):

    response = client.embeddings.create(
        model="text-embedding-3-small",
        input=texts
    )

    return [
        item.embedding
        for item in response.data
    ]


# ==========================================
# INGEST
# ==========================================

def ingest_documents():

    if not os.path.exists(KNOWLEDGE_DIR):

        print(
            "Knowledge folder does not exist."
        )

        return


    files = [
        file
        for file in os.listdir(KNOWLEDGE_DIR)
        if file.lower().endswith(
            (".txt", ".pdf")
        )
    ]


    if not files:

        print(
            "No .txt or .pdf files found "
            "inside knowledge folder."
        )

        return


    # --------------------------------------
    # DELETE OLD DATABASE
    # --------------------------------------

    if os.path.exists(CHROMA_DIR):

        shutil.rmtree(CHROMA_DIR)


    # --------------------------------------
    # CREATE DATABASE
    # --------------------------------------

    chroma_client = chromadb.PersistentClient(
        path=CHROMA_DIR
    )

    collection = chroma_client.get_or_create_collection(
        name="brainstorming_knowledge"
    )


    total_chunks = 0


    # --------------------------------------
    # PROCESS EACH FILE
    # --------------------------------------

    for file in files:

        file_path = os.path.join(
            KNOWLEDGE_DIR,
            file
        )

        print()
        print(
            f"Processing: {file}"
        )


        text = read_document(
            file_path
        )


        if not text.strip():

            print(
                "No readable text found."
            )

            continue


        chunks = create_chunks(text)


        print(
            f"Created {len(chunks)} chunks."
        )


        # ----------------------------------
        # EMBEDDINGS
        # ----------------------------------

        embeddings = create_embeddings(
            chunks
        )


        # ----------------------------------
        # IDS
        # ----------------------------------

        ids = [
            f"chunk_{total_chunks + i}"
            for i in range(len(chunks))
        ]


        # ----------------------------------
        # METADATA
        # ----------------------------------

        metadatas = [
            {
                "source": file
            }
            for _ in chunks
        ]


        # ----------------------------------
        # STORE
        # ----------------------------------

        collection.add(
            ids=ids,
            documents=chunks,
            embeddings=embeddings,
            metadatas=metadatas
        )


        total_chunks += len(chunks)


        print(
            f"Stored {len(chunks)} chunks."
        )


    print()
    print(
        "======================================"
    )
    print(
        "RAG INGESTION COMPLETE"
    )
    print(
        "======================================"
    )

    print(
        f"Total chunks stored: {total_chunks}"
    )


# ==========================================
# MAIN
# ==========================================

if __name__ == "__main__":

    ingest_documents()