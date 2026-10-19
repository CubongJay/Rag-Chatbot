import os
from uuid import UUID

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile, status

from app.api.dependencies.rag_context.handlers import (
    GetDocumentStatusHandler,
    UploadDocumentHandler,
)
from app.config.settings import get_settings


router = APIRouter(prefix="/rag-context", tags=["rag-context"])
settings = get_settings()


@router.post("/documents/upload", status_code=status.HTTP_201_CREATED)
async def upload_document(
    handler: UploadDocumentHandler,
    session_id: UUID,
    file: UploadFile = File(...),
):
    allowed = {".txt", ".pdf"}
    ext = os.path.splitext(file.filename)[1].lower()
    if ext not in allowed:
        raise HTTPException(400, f"Only {', '.join(allowed)} files supported")

    try:
       
        content = await file.read()
    except UnicodeDecodeError:
        raise HTTPException(400, "File must be valid UTF-8 text")

    return await handler(content, file.filename, session_id)


@router.get("/documents/status/{document_id}", status_code=status.HTTP_200_OK)
async def get_document_status(
    document_id: UUID, handler: GetDocumentStatusHandler
):
    return await handler(document_id)
