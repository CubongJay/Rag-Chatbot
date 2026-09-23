# import chromadb
# from chromadb.utils import embedding_functions
# from fastapi import APIRouter, UploadFile, status
# from langchain_openai import OpenAIEmbeddings

# from app.api.dependencies.rag_context.handlers import UploadDocumentHandler
# from app.config.chroma_client import get_chroma_client
# from app.config.settings import get_settings

# router = APIRouter(prefix="/rag-context", tags=["rag-context"])
# settings = get_settings()


# @router.post("/documents/upload", status_code=status.HTTP_201_CREATED)
# async def upload_document(
#     file: UploadFile,
#     handler: UploadDocumentHandler,
# ):
#     return await handler(file)


# @router.get("/documents/check", status_code=status.HTTP_200_OK)
# async def check_document_endpoint():
#     client = get_chroma_client()
#     # open_ai_embeddings = embedding_functions.OpenAIEmbeddingFunction(
#     #     model_name="text-embedding-3-small",
#     #     api_key=settings.openai_api_key,
#     # )

#     open_ai_embeddings = OpenAIEmbeddings(
#         model="text-embedding-3-small",
#         openai_api_key=settings.openai_api_key,
#     )
#     collection = client.get_collection(name="documents")
#     query_text = "Climate change impact"
#     query_vector = open_ai_embeddings.embed_query(query_text)
#     results = collection.query(query_embeddings=[query_vector], n_results=2)
#     return {"results": results}
from fastapi import APIRouter, UploadFile, File, Depends, HTTPException, status
from uuid import UUID
import os

from app.api.dependencies.rag_context.handlers import UploadDocumentHandler, GetDocumentStatusHandler

router = APIRouter()


@router.post("/documents/upload", status_code=status.HTTP_201_CREATED)
async def upload_document(
    session_id: UUID,
    file: UploadFile = File(...),
    handler: UploadDocumentHandler = Depends(),
):
    allowed = {".txt", ".pdf"}
    ext = os.path.splitext(file.filename)[1].lower()
    if ext not in allowed:
        raise HTTPException(400, f"Only {', '.join(allowed)} files supported")

    content = await file.read()
    try:
        text = content.decode("utf-8")
    except UnicodeDecodeError:
        raise HTTPException(400, "File must be valid UTF-8 text")

    return await handler(text, file.filename, session_id)


@router.get("/documents/status/{document_id}", status_code=status.HTTP_200_OK)
async def get_document_status(
    document_id: UUID,
    handler: GetDocumentStatusHandler = Depends(),
):
    return await handler(document_id)