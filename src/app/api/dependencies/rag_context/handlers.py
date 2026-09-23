# 

from typing import Annotated, Awaitable,Callable
from uuid import UUID

from fastapi import Depends, BackgroundTasks

from app.api.dependencies.rag_context.usecases import upload_document_usecase, get_document_status_usecase
from app.usecases.get_document_status import GetDocumentStatusUseCase
from app.usecases.upload_document import (
    UploadDocumentUseCase,
    UploadDocumentResponse,
)
from app.tasks.documents import process_document_task


async def upload_document_handler(
    use_case: UploadDocumentUseCase = Depends(upload_document_usecase),
    background_tasks: BackgroundTasks = None,
) -> Callable[[str, str, UUID], UploadDocumentResponse]:
    """Dependency provider that returns the handler function."""

    async def handler(
        file_content: str, file_name: str, session_id: UUID
    ) -> UploadDocumentResponse:
        # Execute use case
        result = await use_case.execute(
            file_content=file_content,
            file_name=file_name,
            session_id=session_id,
        )

        # Queue background processing
        background_tasks.add_task(
            process_document_task,
            document_id=result.document_id,
            file_path=result.file_path,
            session_id=session_id,
        )

        return result

    return handler

async def get_document_status_handler(
    use_case: GetDocumentStatusUseCase = Depends(get_document_status_usecase),
) -> Callable[[UUID], Awaitable[dict]]:
    """Dependency provider that returns the handler function."""

    async def handler(document_id: UUID) -> dict:
        document = await use_case.execute(document_id)

        if not document:
            raise HTTPException(status_code=404, detail="Document not found")

        return {
            "document_id": str(document.id),
            "status": document.status.value,
            "file_name": document.file_name,
            "chunk_count": document.chunk_count,
            "error_message": document.error_message,
        }

    return handler


GetDocumentStatusHandler = Annotated[
    Callable[[UUID], Awaitable[dict]],
    Depends(get_document_status_handler),
]


UploadDocumentHandler = Annotated[
    Callable[[str, str, UUID], UploadDocumentResponse],
    Depends(upload_document_handler),
]