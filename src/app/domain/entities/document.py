from dataclasses import dataclass
from typing import Dict, Optional
from uuid import UUID
from datetime import datetime

from app.infrastructure.db.models import DocumentStatus



@dataclass
class Document:
    content: str
    metadata: Optional[Dict] = None


@dataclass
class DocumentRecord:
    id: UUID
    session_id: UUID
    file_name: str
    file_path: str
    status: DocumentStatus
    chunk_count: int = 0
    error_message: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


@dataclass
class DocumentChunk:
    content: str
    metadata: Dict