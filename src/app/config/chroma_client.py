import os

import chromadb

# from sentence_transformers import SentenceTransformer

CHROMA_HOST = os.getenv("CHROMA_HOST")
CHROMA_PORT = os.getenv("CHROMA_PORT")

os.environ["TRANSFORMERS_CACHE"] = "/tmp/huggingface_cache"

# embedding_model = SentenceTransformer("all-MiniLM-L6-v2")


def get_chroma_client() -> chromadb.HttpClient:
    """Create and return a ChromaDB client."""
    # client = Client(
    #     Settings(
    #         chroma_api_impl="rest",
    #         chroma_server_host=CHROMA_HOST,
    #         chroma_server_http_port=int(CHROMA_PORT),
    #     )
    # )
    client = chromadb.HttpClient(host="chroma", port=8000)
    return client
