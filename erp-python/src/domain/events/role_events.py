"""
Domain Events - Role Module
Events that occur within the role domain.

Author: Alexandre Albert Ndour
"""

from dataclasses import dataclass
from datetime import datetime
from typing import Optional, List
import uuid


@dataclass
class RoleCreatedEvent:
    """Event fired when a new role is created."""
    
    event_id: uuid.UUID
    occurred_at: datetime
    event_type: str
    role_id: uuid.UUID
    role_name: str
    created_by: Optional[uuid.UUID] = None
    
    def __init__(
        self,
        role_id: uuid.UUID,
        role_name: str,
        created_by: Optional[uuid.UUID] = None
    ):
        self.event_id = uuid.uuid4()
        self.occurred_at = datetime.now()
        self.event_type = "role.created"
        self.role_id = role_id
        self.role_name = role_name
        self.created_by = created_by


@dataclass
class RoleAssignedEvent:
    """Event fired when a role is assigned to a user."""
    
    event_id: uuid.UUID
    occurred_at: datetime
    event_type: str
    user_id: uuid.UUID
    role_id: uuid.UUID
    assigned_by: Optional[uuid.UUID] = None
    
    def __init__(
        self,
        user_id: uuid.UUID,
        role_id: uuid.UUID,
        assigned_by: Optional[uuid.UUID] = None
    ):
        self.event_id = uuid.uuid4()
        self.occurred_at = datetime.now()
        self.event_type = "role.assigned"
        self.user_id = user_id
        self.role_id = role_id
        self.assigned_by = assigned_by


@dataclass
class RoleRevokedEvent:
    """Event fired when a role is revoked from a user."""
    
    event_id: uuid.UUID
    occurred_at: datetime
    event_type: str
    user_id: uuid.UUID
    role_id: uuid.UUID
    revoked_by: Optional[uuid.UUID] = None
    
    def __init__(
        self,
        user_id: uuid.UUID,
        role_id: uuid.UUID,
        revoked_by: Optional[uuid.UUID] = None
    ):
        self.event_id = uuid.uuid4()
        self.occurred_at = datetime.now()
        self.event_type = "role.revoked"
        self.user_id = user_id
        self.role_id = role_id
        self.revoked_by = revoked_by


@dataclass
class PermissionAddedEvent:
    """Event fired when a permission is added to a role."""
    
    event_id: uuid.UUID
    occurred_at: datetime
    event_type: str
    role_id: uuid.UUID
    permission: str
    added_by: Optional[uuid.UUID] = None
    
    def __init__(
        self,
        role_id: uuid.UUID,
        permission: str,
        added_by: Optional[uuid.UUID] = None
    ):
        self.event_id = uuid.uuid4()
        self.occurred_at = datetime.now()
        self.event_type = "permission.added"
        self.role_id = role_id
        self.permission = permission
        self.added_by = added_by


@dataclass
class PermissionRemovedEvent:
    """Event fired when a permission is removed from a role."""
    
    event_id: uuid.UUID
    occurred_at: datetime
    event_type: str
    role_id: uuid.UUID
    permission: str
    removed_by: Optional[uuid.UUID] = None
    
    def __init__(
        self,
        role_id: uuid.UUID,
        permission: str,
        removed_by: Optional[uuid.UUID] = None
    ):
        self.event_id = uuid.uuid4()
        self.occurred_at = datetime.now()
        self.event_type = "permission.removed"
        self.role_id = role_id
        self.permission = permission
        self.removed_by = removed_by
