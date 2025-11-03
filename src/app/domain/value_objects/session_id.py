import uuid
from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class SessionId:
    value: Optional[str] = None

    def __post_init__(self):
        try:
            uuid.UUID(self.value)
        except ValueError:
            raise ValueError("Invalid session ID format.")
