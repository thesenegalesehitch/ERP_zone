"""
UserRole Entity - Domain Layer
Represents the many-to-many relationship between users and roles.

Author: Alexandre Albert Ndour
"""

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Optional
import uuid


@dataclass
class UserRole:
    """
    UserRole Association Entity.
    
    Represents the assignment of a role to a user.
    Includes metadata about when the role was assigned
    and by whom.
    """
    
    # Identity
    id: uuid.UUID = field(default_factory=uuid.uuid4)
    user_id: uuid.UUID = None  # type: ignore
    role_id: uuid.UUID = None  # type: ignore
    
    # Metadata
    assigned_by: Optional[uuid.UUID] = None
    assigned_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    expires_at: Optional[datetime] = None
    
    # Status
    is_active: bool = True
    
    def __post_init__(self):
        """Validate after initialization."""
        if isinstance(self.user_id, str):
            self.user_id = uuid.UUID(self.user_id)
        if isinstance(self.role_id, str):
            self.role_id = uuid.UUID(self.role_id)
    
    # ==================== Business Methods ====================
    
    def is_expired(self) -> bool:
        """Check if role assignment has expired."""
        if self.expires_at is None:
            return False
        return datetime.now(timezone.utc) > self.expires_at
    
    def revoke(self) -> None:
        """Revoke this role assignment."""
        self.is_active = False
    
    def extend(self, days: int) -> None:
        """Extend the role assignment expiration."""
        from datetime import timedelta
        if self.expires_at is None:
            self.expires_at = datetime.now(timezone.utc) + timedelta(days=days)
        else:
            self.expires_at = self.expires_at + timedelta(days=days)
    
    # ==================== Factory Methods ====================
    
    @classmethod
    def create(
        cls,
        user_id: uuid.UUID,
        role_id: uuid.UUID,
        assigned_by: uuid.UUID = None,
        expires_in_days: int = None
    ) -> "UserRole":
        """
        Factory method to create a user-role assignment.
        
        Args:
            user_id: ID of the user
            role_id: ID of the role
            assigned_by: ID of user assigning the role
            expires_in_days: Optional expiration in days
            
        Returns:
            New UserRole instance
        """
        from datetime import timedelta
        
        expires_at = None
        if expires_in_days:
            expires_at = datetime.now(timezone.utc) + timedelta(days=expires_in_days)
        
        return cls(
            user_id=user_id,
            role_id=role_id,
            assigned_by=assigned_by,
            expires_at=expires_at,
        )
    
    # ==================== Serialization ====================
    
    def to_dict(self) -> dict:
        """Convert to dictionary."""
        return {
            "id": str(self.id),
            "user_id": str(self.user_id),
            "role_id": str(self.role_id),
            "assigned_by": str(self.assigned_by) if self.assigned_by else None,
            "assigned_at": self.assigned_at.isoformat(),
            "expires_at": self.expires_at.isoformat() if self.expires_at else None,
            "is_active": self.is_active,
            "is_expired": self.is_expired(),
        }
