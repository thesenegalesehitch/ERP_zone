"""
ActivityLog Entity - Domain Layer
Represents activity logs in the ERP system.

Author: Alexandre Albert Ndour
"""

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Optional
import uuid


@dataclass
class ActivityLog:
    """Activity log entity."""
    
    id: uuid.UUID = field(default_factory=uuid.uuid4)
    
    user_id: Optional[uuid.UUID] = None
    action: str = ""
    entity_type: str = ""
    entity_id: Optional[uuid.UUID] = None
    
    details: dict = field(default_factory=dict)
    ip_address: Optional[str] = None
    
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    
    def to_dict(self) -> dict:
        return {
            "id": str(self.id),
            "user_id": str(self.user_id) if self.user_id else None,
            "action": self.action,
            "entity_type": self.entity_type,
            "entity_id": str(self.entity_id) if self.entity_id else None,
            "details": self.details,
            "ip_address": self.ip_address,
            "created_at": self.created_at.isoformat(),
        }
