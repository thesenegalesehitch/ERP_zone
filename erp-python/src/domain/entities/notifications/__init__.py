"""
Notification Entity - Domain Layer
Represents notifications in the ERP system.

Author: Alexandre Albert Ndour
"""

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Optional
import uuid


@dataclass
class Notification:
    """Notification entity."""
    
    id: uuid.UUID = field(default_factory=uuid.uuid4)
    user_id: uuid.UUID = None  # type: ignore
    
    title: str = ""
    message: str = ""
    type: str = "info"  # info, success, warning, error
    
    is_read: bool = False
    read_at: Optional[datetime] = None
    
    action_url: Optional[str] = None
    
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    
    def mark_as_read(self) -> None:
        self.is_read = True
        self.read_at = datetime.now(timezone.utc)
    
    def to_dict(self) -> dict:
        return {
            "id": str(self.id),
            "user_id": str(self.user_id),
            "title": self.title,
            "message": self.message,
            "type": self.type,
            "is_read": self.is_read,
            "action_url": self.action_url,
            "created_at": self.created_at.isoformat(),
        }
