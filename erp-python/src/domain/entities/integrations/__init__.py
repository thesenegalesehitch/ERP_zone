"""
Integration Entity for ERP System.

This module provides the Integration entity for managing third-party integrations
following Clean Architecture principles.
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional, Dict, Any, List
from enum import Enum


class IntegrationStatus(str, Enum):
    """Integration status enumeration."""
    DISCONNECTED = "disconnected"
    CONNECTED = "connected"
    ACTIVE = "active"
    ERROR = "error"
    SUSPENDED = "suspended"


class IntegrationType(str, Enum):
    """Integration type enumeration."""
    PAYMENT = "payment"
    SHIPPING = "shipping"
    ACCOUNTING = "accounting"
    CRM = "crm"
    MARKETING = "marketing"
    STORAGE = "storage"
    COMMUNICATION = "communication"
    ANALYTICS = "analytics"
    CUSTOM = "custom"


@dataclass(frozen=True)
class IntegrationCredential:
    """
    Value Object representing integration credentials.
    Immutable and validated.
    """
    key: str
    value: str
    is_encrypted: bool = True
    
    def __post_init__(self):
        if not self.key:
            raise ValueError("key cannot be empty")
        if not self.value:
            raise ValueError("value cannot be empty")
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "key": self.key,
            "value": "****" if self.is_encrypted else self.value,
            "is_encrypted": self.is_encrypted
        }


@dataclass(frozen=True)
class Integration:
    """
    Integration entity representing a third-party integration.
    
    This entity follows Clean Architecture principles and is immutable.
    
    Attributes:
        id: Unique identifier for the integration
        name: Integration name
        description: Integration description
        integration_type: Type of integration
        status: Current status
        base_url: Integration API base URL
        credentials: List of integration credentials
        webhook_url: Webhook URL for callbacks
        webhook_secret: Webhook secret for verification
        settings: Integration-specific settings
        last_sync_at: Last synchronization timestamp
        metadata: Additional metadata
        created_at: Timestamp when created
        updated_at: Timestamp when last updated
    """
    id: str
    name: str
    description: str
    integration_type: IntegrationType
    status: IntegrationStatus
    base_url: Optional[str] = None
    credentials: List[IntegrationCredential] = field(default_factory=list)
    webhook_url: Optional[str] = None
    webhook_secret: Optional[str] = None
    settings: Dict[str, Any] = field(default_factory=dict)
    last_sync_at: Optional[datetime] = None
    metadata: Dict[str, Any] = field(default_factory=dict)
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime = field(default_factory=datetime.utcnow)
    
    def __post_init__(self):
        """Validate integration after initialization."""
        if not self.name:
            raise ValueError("name cannot be empty")
        if not self.description:
            raise ValueError("description cannot be empty")
    
    @property
    def is_connected(self) -> bool:
        """Check if integration is connected."""
        return self.status in [IntegrationStatus.CONNECTED, IntegrationStatus.ACTIVE]
    
    @property
    def is_active(self) -> bool:
        """Check if integration is active."""
        return self.status == IntegrationStatus.ACTIVE
    
    @property
    def has_error(self) -> bool:
        """Check if integration has error."""
        return self.status == IntegrationStatus.ERROR
    
    @property
    def credential_count(self) -> int:
        """Get number of credentials."""
        return len(self.credentials)
    
    def to_dict(self, include_secrets: bool = False) -> Dict[str, Any]:
        """Convert integration to dictionary."""
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "integration_type": self.integration_type.value,
            "status": self.status.value,
            "base_url": self.base_url,
            "credentials": [c.to_dict() for c in self.credentials] if include_secrets else ["****"] * len(self.credentials),
            "webhook_url": self.webhook_url,
            "settings": self.settings,
            "last_sync_at": self.last_sync_at.isoformat() if self.last_sync_at else None,
            "metadata": self.metadata,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
            "is_connected": self.is_connected,
            "is_active": self.is_active,
            "has_error": self.has_error,
            "credential_count": self.credential_count
        }


class IntegrationBuilder:
    """Builder for creating Integration instances."""
    
    def __init__(self):
        self._id: Optional[str] = None
        self._name: Optional[str] = None
        self._description: Optional[str] = None
        self._integration_type: IntegrationType = IntegrationType.CUSTOM
        self._status: IntegrationStatus = IntegrationStatus.DISCONNECTED
        self._base_url: Optional[str] = None
        self._credentials: List[IntegrationCredential] = []
        self._webhook_url: Optional[str] = None
        self._webhook_secret: Optional[str] = None
        self._settings: Dict[str, Any] = {}
        self._metadata: Dict[str, Any] = {}
    
    def with_id(self, integration_id: str) -> "IntegrationBuilder":
        self._id = integration_id
        return self
    
    def with_name(self, name: str) -> "IntegrationBuilder":
        self._name = name
        return self
    
    def with_description(self, description: str) -> "IntegrationBuilder":
        self._description = description
        return self
    
    def with_type(self, integration_type: IntegrationType) -> "IntegrationBuilder":
        self._integration_type = integration_type
        return self
    
    def with_status(self, status: IntegrationStatus) -> "IntegrationBuilder":
        self._status = status
        return self
    
    def with_base_url(self, base_url: str) -> "IntegrationBuilder":
        self._base_url = base_url
        return self
    
    def with_credentials(self, credentials: List[IntegrationCredential]) -> "IntegrationBuilder":
        self._credentials = credentials
        return self
    
    def add_credential(self, credential: IntegrationCredential) -> "IntegrationBuilder":
        self._credentials.append(credential)
        return self
    
    def with_webhook(self, webhook_url: str, webhook_secret: Optional[str] = None) -> "IntegrationBuilder":
        self._webhook_url = webhook_url
        self._webhook_secret = webhook_secret
        return self
    
    def with_settings(self, settings: Dict[str, Any]) -> "IntegrationBuilder":
        self._settings = settings
        return self
    
    def with_metadata(self, metadata: Dict[str, Any]) -> "IntegrationBuilder":
        self._metadata = metadata
        return self
    
    def build(self) -> Integration:
        from uuid import uuid4
        
        if not self._id:
            self._id = str(uuid4())
        if not self._name:
            raise ValueError("name is required")
        if not self._description:
            raise ValueError("description is required")
        
        return Integration(
            id=self._id,
            name=self._name,
            description=self._description,
            integration_type=self._integration_type,
            status=self._status,
            base_url=self._base_url,
            credentials=self._credentials,
            webhook_url=self._webhook_url,
            webhook_secret=self._webhook_secret,
            settings=self._settings,
            metadata=self._metadata
        )


# Factory functions
def create_integration_credential(
    key: str,
    value: str,
    is_encrypted: bool = True
) -> IntegrationCredential:
    """Factory function to create an integration credential."""
    return IntegrationCredential(
        key=key,
        value=value,
        is_encrypted=is_encrypted
    )


def create_integration(
    name: str,
    description: str,
    **kwargs
) -> Integration:
    """Factory function to create an integration."""
    builder = IntegrationBuilder()
    builder.with_name(name)
    builder.with_description(description)
    
    if integration_type := kwargs.get("integration_type"):
        builder.with_type(integration_type)
    if status := kwargs.get("status"):
        builder.with_status(status)
    if base_url := kwargs.get("base_url"):
        builder.with_base_url(base_url)
    if credentials := kwargs.get("credentials"):
        builder.with_credentials(credentials)
    if webhook_url := kwargs.get("webhook_url"):
        webhook_secret = kwargs.get("webhook_secret")
        builder.with_webhook(webhook_url, webhook_secret)
    if settings := kwargs.get("settings"):
        builder.with_settings(settings)
    if metadata := kwargs.get("metadata"):
        builder.with_metadata(metadata)
    
    return builder.build()
