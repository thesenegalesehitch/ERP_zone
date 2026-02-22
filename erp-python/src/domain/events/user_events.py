"""
Domain Events - User Module
Events that occur within the user domain.

Author: Alexandre Albert Ndour
"""

from dataclasses import dataclass
from datetime import datetime
from typing import Optional
import uuid


@dataclass
class DomainEvent:
    """Base class for all domain events."""
    event_id: uuid.UUID
    occurred_at: datetime
    event_type: str
    
    def __post_init__(self):
        if self.occurred_at is None:
            self.occurred_at = datetime.now()


@dataclass
class UserCreatedEvent(DomainEvent):
    """Event fired when a new user is created."""
    
    user_id: uuid.UUID
    email: str
    first_name: str
    last_name: str
    created_by: Optional[uuid.UUID] = None
    
    def __init__(
        self,
        user_id: uuid.UUID,
        email: str,
        first_name: str,
        last_name: str,
        created_by: Optional[uuid.UUID] = None
    ):
        super().__init__(
            event_id=uuid.uuid4(),
            occurred_at=datetime.now(),
            event_type="user.created"
        )
        self.user_id = user_id
        self.email = email
        self.first_name = first_name
        self.last_name = last_name
        self.created_by = created_by
    
    def to_dict(self) -> dict:
        return {
            "event_id": str(self.event_id),
            "event_type": self.event_type,
            "occurred_at": self.occurred_at.isoformat(),
            "user_id": str(self.user_id),
            "email": self.email,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "created_by": str(self.created_by) if self.created_by else None,
        }


@dataclass
class UserUpdatedEvent(DomainEvent):
    """Event fired when a user is updated."""
    
    user_id: uuid.UUID
    updated_fields: list[str]
    updated_by: Optional[uuid.UUID] = None
    
    def __init__(
        self,
        user_id: uuid.UUID,
        updated_fields: list[str],
        updated_by: Optional[uuid.UUID] = None
    ):
        super().__init__(
            event_id=uuid.uuid4(),
            occurred_at=datetime.now(),
            event_type="user.updated"
        )
        self.user_id = user_id
        self.updated_fields = updated_fields
        self.updated_by = updated_by
    
    def to_dict(self) -> dict:
        return {
            "event_id": str(self.event_id),
            "event_type": self.event_type,
            "occurred_at": self.occurred_at.isoformat(),
            "user_id": str(self.user_id),
            "updated_fields": self.updated_fields,
            "updated_by": str(self.updated_by) if self.updated_by else None,
        }


@dataclass
class UserDeletedEvent(DomainEvent):
    """Event fired when a user is deleted."""
    
    user_id: uuid.UUID
    deleted_by: Optional[uuid.UUID] = None
    
    def __init__(
        self,
        user_id: uuid.UUID,
        deleted_by: Optional[uuid.UUID] = None
    ):
        super().__init__(
            event_id=uuid.uuid4(),
            occurred_at=datetime.now(),
            event_type="user.deleted"
        )
        self.user_id = user_id
        self.deleted_by = deleted_by
    
    def to_dict(self) -> dict:
        return {
            "event_id": str(self.event_id),
            "event_type": self.event_type,
            "occurred_at": self.occurred_at.isoformat(),
            "user_id": str(self.user_id),
            "deleted_by": str(self.deleted_by) if self.deleted_by else None,
        }


@dataclass
class UserActivatedEvent(DomainEvent):
    """Event fired when a user is activated."""
    
    user_id: uuid.UUID
    
    def __init__(self, user_id: uuid.UUID):
        super().__init__(
            event_id=uuid.uuid4(),
            occurred_at=datetime.now(),
            event_type="user.activated"
        )
        self.user_id = user_id


@dataclass
class UserDeactivatedEvent(DomainEvent):
    """Event fired when a user is deactivated."""
    
    user_id: uuid.UUID
    
    def __init__(self, user_id: uuid.UUID):
        super().__init__(
            event_id=uuid.uuid4(),
            occurred_at=datetime.now(),
            event_type="user.deactivated"
        )
        self.user_id = user_id


@dataclass
class UserLockedEvent(DomainEvent):
    """Event fired when a user account is locked."""
    
    user_id: uuid.UUID
    reason: str = "Too many failed login attempts"
    
    def __init__(self, user_id: uuid.UUID, reason: str = "Too many failed login attempts"):
        super().__init__(
            event_id=uuid.uuid4(),
            occurred_at=datetime.now(),
            event_type="user.locked"
        )
        self.user_id = user_id
        self.reason = reason


@dataclass
class PasswordChangedEvent(DomainEvent):
    """Event fired when a user's password is changed."""
    
    user_id: uuid.UUID
    changed_by: Optional[uuid.UUID] = None
    
    def __init__(
        self,
        user_id: uuid.UUID,
        changed_by: Optional[uuid.UUID] = None
    ):
        super().__init__(
            event_id=uuid.uuid4(),
            occurred_at=datetime.now(),
            event_type="user.password_changed"
        )
        self.user_id = user_id
        self.changed_by = changed_by
