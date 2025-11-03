import chromadb
from chromadb.utils import embedding_functions
from fastapi import APIRouter, UploadFile, status
from langchain_openai import OpenAIEmbeddings

from app.api.dependencies.rag_context.handlers import UploadDocumentHandler
from app.config.chroma_client import get_chroma_client
from app.config.settings import get_settings

router = APIRouter(prefix="/rag-context", tags=["rag-context"])
settings = get_settings()


@router.post("/documents/upload", status_code=status.HTTP_201_CREATED)
async def upload_document(
    file: UploadFile,
    handler: UploadDocumentHandler,
):
    return await handler(file)


@router.get("/documents/check", status_code=status.HTTP_200_OK)
async def check_document_endpoint():
    client = get_chroma_client()
    # open_ai_embeddings = embedding_functions.OpenAIEmbeddingFunction(
    #     model_name="text-embedding-3-small",
    #     api_key=settings.openai_api_key,
    # )

    open_ai_embeddings = OpenAIEmbeddings(
        model="text-embedding-3-small",
        openai_api_key=settings.openai_api_key,
    )
    collection = client.get_collection(name="documents")
    query_text = "Climate change impact"
    query_vector = open_ai_embeddings.embed_query(query_text)
    results = collection.query(query_embeddings=[query_vector], n_results=2)
    return {"results": results}
