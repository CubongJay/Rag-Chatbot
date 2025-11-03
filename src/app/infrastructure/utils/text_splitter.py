from typing import Dict, List, Optional

from app.domain.entities.document import Document


def split_text_into_documents(
    text: str,
    chunk_size: int = 500,
    overlap: int = 50,
    metadata: Optional[Dict] = None,
):
    """
    Splits a given text into smaller document chunks with specified size and overlap.
    """
    documents = []
    start = 0
    text_length = len(text)

    while start < text_length:
        end = min(start + chunk_size, text_length)
        chunk_text = text[start:end]
        documents.append(Document(content=chunk_text, metadata=metadata))
        start += chunk_size - overlap

    return documents
