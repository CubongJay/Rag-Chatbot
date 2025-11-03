from typing import Annotated, Callable

from fastapi import Depends, UploadFile

from app.usecases.upload_document import UploadDocumentUseCase

from .usecases import upload_document_usecase


async def upload_document_handler(
    use_case: UploadDocumentUseCase = Depends(upload_document_usecase),
) -> Callable[[UploadFile], dict]:
    """Dependency provider that returns a handler function."""

    async def handler(file: UploadFile) -> dict:

        content = await file.read()

        text = content.decode("utf-8")

        result = await use_case.execute(
            file_content=text,
            file_name=file.filename,
        )
        return {
            "filename": file.filename,
            "status": "uploaded",
            "result": result,
        }

    return handler


UploadDocumentHandler = Annotated[
    Callable[[UploadFile], dict], Depends(upload_document_handler)
]
