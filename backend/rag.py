import os

import chromadb

from dotenv import load_dotenv
from openai import OpenAI


# ==========================================
# ENVIRONMENT
# ==========================================

load_dotenv(os.path.join(os.path.dirname(__file__), ".env"))

api_key = os.getenv("OPENAI_API_KEY")

if not api_key:
    raise RuntimeError(
        "OPENAI_API_KEY is missing from .env file"
    )


client = OpenAI(
    api_key=api_key
)


# ==========================================
# CHROMA DATABASE
# ==========================================

chroma_client = chromadb.PersistentClient(
    path=os.getenv(
        "CHROMA_DB_PATH",
        os.path.join(os.path.dirname(__file__), "chroma_db")
    )
)


collection = chroma_client.get_or_create_collection(
    name="brainstorming_knowledge"
)


# ==========================================
# EMBEDDING
# ==========================================

def create_embedding(text):

    response = client.embeddings.create(
        model="text-embedding-3-small",
        input=text
    )

    return response.data[0].embedding


# ==========================================
# RETRIEVE
# ==========================================

def retrieve_knowledge(
    query,
    top_k=5
):

    if collection.count() == 0:

        return []


    query_embedding = create_embedding(
        query
    )


    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k
    )


    documents = results.get(
        "documents",
        [[]]
    )[0]


    return documents