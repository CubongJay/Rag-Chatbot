from dataclasses import dataclass
from typing import Dict, Optional


@dataclass
class Document:
    content: str
    metadata: Optional[Dict] = None
