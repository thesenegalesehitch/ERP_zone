"""
Document Entity - Domain Layer
Represents documents in the ERP system.

Author: Alexandre Albert Ndour
"""

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Optional
import uuid


@dataclass
class Document:
    """Document entity."""
    
    id: uuid.UUID = field(default_factory=uuid.uuid4)
    
    name: str = ""
    file_name: str = ""
    file_path: str = ""
    file_size: int = 0
    mime_type: str = ""
    
    document_type: str = "general"  # invoice, order, contract, etc.
    
    reference_type: Optional[str] = None
    reference_id: Optional[uuid.UUID] = None
    
    uploaded_by: Optional[uuid.UUID] = None
    
    is_public: bool = False
    
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    
    def to_dict(self) -> dict:
        return {
            "id": str(self.id),
            "name": self.name,
            "file_name": self.file_name,
            "file_size": self.file_size,
            "mime_type": self.mime_type,
            "document_type": self.document_type,
            "reference_type": self.reference_type,
            "reference_id": str(self.reference_id) if self.reference_id else None,
            "is_public": self.is_public,
            "created_at": self.created_at.isoformat(),
        }
