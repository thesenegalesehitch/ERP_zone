"""
Audit Log Entity for ERP System.

This module provides the AuditLog entity for tracking system changes
following Clean Architecture principles.
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional, Dict, Any
from enum import Enum


class AuditAction(str, Enum):
    """Enumeration of all possible audit actions."""
    CREATE = "create"
    UPDATE = "update"
    DELETE = "delete"
    READ = "read"
    LOGIN = "login"
    LOGOUT = "logout"
    EXPORT = "export"
    IMPORT = "import"
    APPROVE = "approve"
    REJECT = "reject"
    CUSTOM = "custom"


class AuditLevel(str, Enum):
    """Audit log severity levels."""
    DEBUG = "debug"
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"
    CRITICAL = "critical"


@dataclass(frozen=True)
class AuditLog:
    """
    AuditLog entity representing a single audit entry in the system.
    
    This entity follows Clean Architecture principles and is immutable.
    It tracks all changes made to the system for compliance and debugging.
    
    Attributes:
        id: Unique identifier for the audit log entry
        entity_type: Type of entity that was modified
        entity_id: ID of the entity that was modified
        action: The action that was performed
        level: Severity level of the audit entry
        user_id: ID of the user who performed the action
        user_email: Email of the user who performed the action
        description: Human-readable description of the action
        changes: Dictionary of field changes (old_value -> new_value)
        ip_address: IP address from which the action was performed
        user_agent: User agent string of the client
        request_id: Request ID for tracing
        metadata: Additional metadata about the action
        created_at: Timestamp when the audit log was created
    """
    id: str
    entity_type: str
    entity_id: str
    action: AuditAction
    level: AuditLevel
    user_id: str
    user_email: str
    description: str
    changes: Dict[str, tuple[Any, Any]] = field(default_factory=dict)
    ip_address: Optional[str] = None
    user_agent: Optional[str] = None
    request_id: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)
    created_at: datetime = field(default_factory=datetime.utcnow)
    
    def __post_init__(self):
        """Validate audit log after initialization."""
        if not self.entity_type:
            raise ValueError("entity_type cannot be empty")
        if not self.entity_id:
            raise ValueError("entity_id cannot be empty")
        if not self.description:
            raise ValueError("description cannot be empty")
        if not self.user_id:
            raise ValueError("user_id cannot be empty")
    
    @property
    def is_critical(self) -> bool:
        """Check if this audit log is critical."""
        return self.level == AuditLevel.CRITICAL
    
    @property
    def has_changes(self) -> bool:
        """Check if this audit log contains field changes."""
        return bool(self.changes)
    
    def get_field_change(self, field_name: str) -> Optional[tuple[Any, Any]]:
        """Get the change for a specific field."""
        return self.changes.get(field_name)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert audit log to dictionary."""
        return {
            "id": self.id,
            "entity_type": self.entity_type,
            "entity_id": self.entity_id,
            "action": self.action.value,
            "level": self.level.value,
            "user_id": self.user_id,
            "user_email": self.user_email,
            "description": self.description,
            "changes": {
                field: {"old": old, "new": new} 
                for field, (old, new) in self.changes.items()
            },
            "ip_address": self.ip_address,
            "user_agent": self.user_agent,
            "request_id": self.request_id,
            "metadata": self.metadata,
            "created_at": self.created_at.isoformat()
        }


class AuditLogBuilder:
    """Builder for creating AuditLog instances."""
    
    def __init__(self):
        self._id: Optional[str] = None
        self._entity_type: Optional[str] = None
        self._entity_id: Optional[str] = None
        self._action: Optional[AuditAction] = None
        self._level: AuditLevel = AuditLevel.INFO
        self._user_id: Optional[str] = None
        self._user_email: Optional[str] = None
        self._description: Optional[str] = None
        self._changes: Dict[str, tuple[Any, Any]] = {}
        self._ip_address: Optional[str] = None
        self._user_agent: Optional[str] = None
        self._request_id: Optional[str] = None
        self._metadata: Dict[str, Any] = {}
    
    def with_id(self, audit_id: str) -> "AuditLogBuilder":
        self._id = audit_id
        return self
    
    def for_entity(self, entity_type: str, entity_id: str) -> "AuditLogBuilder":
        self._entity_type = entity_type
        self._entity_id = entity_id
        return self
    
    def with_action(self, action: AuditAction) -> "AuditLogBuilder":
        self._action = action
        return self
    
    def with_level(self, level: AuditLevel) -> "AuditLogBuilder":
        self._level = level
        return self
    
    def by_user(self, user_id: str, user_email: str) -> "AuditLogBuilder":
        self._user_id = user_id
        self._user_email = user_email
        return self
    
    def with_description(self, description: str) -> "AuditLogBuilder":
        self._description = description
        return self
    
    def with_changes(self, changes: Dict[str, tuple[Any, Any]]) -> "AuditLogBuilder":
        self._changes = changes
        return self
    
    def with_ip(self, ip_address: str) -> "AuditLogBuilder":
        self._ip_address = ip_address
        return self
    
    def with_user_agent(self, user_agent: str) -> "AuditLogBuilder":
        self._user_agent = user_agent
        return self
    
    def with_request_id(self, request_id: str) -> "AuditLogBuilder":
        self._request_id = request_id
        return self
    
    def with_metadata(self, metadata: Dict[str, Any]) -> "AuditLogBuilder":
        self._metadata = metadata
        return self
    
    def build(self) -> AuditLog:
        if not self._id:
            from uuid import uuid4
            self._id = str(uuid4())
        if not self._entity_type:
            raise ValueError("entity_type is required")
        if not self._entity_id:
            raise ValueError("entity_id is required")
        if not self._action:
            raise ValueError("action is required")
        if not self._user_id:
            raise ValueError("user_id is required")
        if not self._description:
            raise ValueError("description is required")
        
        return AuditLog(
            id=self._id,
            entity_type=self._entity_type,
            entity_id=self._entity_id,
            action=self._action,
            level=self._level,
            user_id=self._user_id,
            user_email=self._user_email or "",
            description=self._description,
            changes=self._changes,
            ip_address=self._ip_address,
            user_agent=self._user_agent,
            request_id=self._request_id,
            metadata=self._metadata
        )


# Factory functions for common audit scenarios
def create_audit_log(
    entity_type: str,
    entity_id: str,
    action: AuditAction,
    user_id: str,
    user_email: str,
    description: str,
    **kwargs
) -> AuditLog:
    """Factory function to create an audit log entry."""
    builder = AuditLogBuilder()
    builder.with_id(kwargs.get("id"))
    builder.for_entity(entity_type, entity_id)
    builder.with_action(action)
    builder.with_level(kwargs.get("level", AuditLevel.INFO))
    builder.by_user(user_id, user_email)
    builder.with_description(description)
    
    if changes := kwargs.get("changes"):
        builder.with_changes(changes)
    if ip_address := kwargs.get("ip_address"):
        builder.with_ip(ip_address)
    if user_agent := kwargs.get("user_agent"):
        builder.with_user_agent(user_agent)
    if request_id := kwargs.get("request_id"):
        builder.with_request_id(request_id)
    if metadata := kwargs.get("metadata"):
        builder.with_metadata(metadata)
    
    return builder.build()
