"""
Webhook Entity for ERP System.

This module provides the Webhook entity for managing webhooks
following Clean Architecture principles.
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional, Dict, Any, List
from enum import Enum


class WebhookStatus(str, Enum):
    """Webhook status enumeration."""
    INACTIVE = "inactive"
    ACTIVE = "active"
    PAUSED = "paused"
    FAILED = "failed"


class WebhookEvent(str, Enum):
    """Webhook event enumeration."""
    USER_CREATED = "user.created"
    USER_UPDATED = "user.updated"
    USER_DELETED = "user.deleted"
    ORDER_CREATED = "order.created"
    ORDER_UPDATED = "order.updated"
    ORDER_COMPLETED = "order.completed"
    INVOICE_CREATED = "invoice.created"
    INVOICE_PAID = "invoice.paid"
    PRODUCT_CREATED = "product.created"
    PRODUCT_UPDATED = "product.updated"
    CUSTOMER_CREATED = "customer.created"
    CUSTOMER_UPDATED = "customer.updated"


@dataclass(frozen=True)
class Webhook:
    """
    Webhook entity representing a webhook endpoint.
    
    This entity follows Clean Architecture principles and is immutable.
    
    Attributes:
        id: Unique identifier for the webhook
        name: Webhook name
        url: Webhook endpoint URL
        status: Current status
        events: List of events to subscribe to
        secret: Secret for signature verification
        headers: Custom headers to send
        is_verified: Whether webhook is verified
        retry_count: Number of retry attempts on failure
        timeout: Request timeout in seconds
        metadata: Additional metadata
        created_at: Timestamp when created
        updated_at: Timestamp when last updated
    """
    id: str
    name: str
    url: str
    status: WebhookStatus
    events: List[WebhookEvent]
    secret: Optional[str] = None
    headers: Dict[str, str] = field(default_factory=dict)
    is_verified: bool = False
    retry_count: int = 3
    timeout: int = 30
    metadata: Dict[str, Any] = field(default_factory=dict)
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime = field(default_factory=datetime.utcnow)
    
    def __post_init__(self):
        """Validate webhook after initialization."""
        if not self.name:
            raise ValueError("name cannot be empty")
        if not self.url:
            raise ValueError("url cannot be empty")
        if not self.events:
            raise ValueError("events cannot be empty")
        if self.retry_count < 0:
            raise ValueError("retry_count cannot be negative")
        if self.timeout <= 0:
            raise ValueError("timeout must be positive")
    
    @property
    def is_active(self) -> bool:
        """Check if webhook is active."""
        return self.status == WebhookStatus.ACTIVE
    
    @property
    def is_paused(self) -> bool:
        """Check if webhook is paused."""
        return self.status == WebhookStatus.PAUSED
    
    @property
    def event_count(self) -> int:
        """Get number of subscribed events."""
        return len(self.events)
    
    def to_dict(self, include_secret: bool = False) -> Dict[str, Any]:
        """Convert webhook to dictionary."""
        return {
            "id": self.id,
            "name": self.name,
            "url": self.url,
            "status": self.status.value,
            "events": [e.value for e in self.events],
            "secret": self.secret if include_secret else "****",
            "headers": self.headers,
            "is_verified": self.is_verified,
            "retry_count": self.retry_count,
            "timeout": self.timeout,
            "metadata": self.metadata,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
            "is_active": self.is_active,
            "is_paused": self.is_paused,
            "event_count": self.event_count
        }


class WebhookBuilder:
    """Builder for creating Webhook instances."""
    
    def __init__(self):
        self._id: Optional[str] = None
        self._name: Optional[str] = None
        self._url: Optional[str] = None
        self._status: WebhookStatus = WebhookStatus.INACTIVE
        self._events: List[WebhookEvent] = []
        self._secret: Optional[str] = None
        self._headers: Dict[str, str] = {}
        self._is_verified: bool = False
        self._retry_count: int = 3
        self._timeout: int = 30
        self._metadata: Dict[str, Any] = {}
    
    def with_id(self, webhook_id: str) -> "WebhookBuilder":
        self._id = webhook_id
        return self
    
    def with_name(self, name: str) -> "WebhookBuilder":
        self._name = name
        return self
    
    def with_url(self, url: str) -> "WebhookBuilder":
        self._url = url
        return self
    
    def with_status(self, status: WebhookStatus) -> "WebhookBuilder":
        self._status = status
        return self
    
    def subscribed_to(self, events: List[WebhookEvent]) -> "WebhookBuilder":
        self._events = events
        return self
    
    def with_secret(self, secret: str) -> "WebhookBuilder":
        self._secret = secret
        return self
    
    def with_headers(self, headers: Dict[str, str]) -> "WebhookBuilder":
        self._headers = headers
        return self
    
    def verified(self, is_verified: bool = True) -> "WebhookBuilder":
        self._is_verified = is_verified
        return self
    
    def with_retries(self, retry_count: int) -> "WebhookBuilder":
        self._retry_count = retry_count
        return self
    
    def with_timeout(self, timeout: int) -> "WebhookBuilder":
        self._timeout = timeout
        return self
    
    def with_metadata(self, metadata: Dict[str, Any]) -> "WebhookBuilder":
        self._metadata = metadata
        return self
    
    def build(self) -> Webhook:
        from uuid import uuid4
        
        if not self._id:
            self._id = str(uuid4())
        if not self._name:
            raise ValueError("name is required")
        if not self._url:
            raise ValueError("url is required")
        if not self._events:
            raise ValueError("events is required")
        
        return Webhook(
            id=self._id,
            name=self._name,
            url=self._url,
            status=self._status,
            events=self._events,
            secret=self._secret,
            headers=self._headers,
            is_verified=self._is_verified,
            retry_count=self._retry_count,
            timeout=self._timeout,
            metadata=self._metadata
        )


# Factory function
def create_webhook(
    name: str,
    url: str,
    events: List[WebhookEvent],
    **kwargs
) -> Webhook:
    """Factory function to create a webhook."""
    builder = WebhookBuilder()
    builder.with_name(name)
    builder.with_url(url)
    builder.subscribed_to(events)
    
    if status := kwargs.get("status"):
        builder.with_status(status)
    if secret := kwargs.get("secret"):
        builder.with_secret(secret)
    if headers := kwargs.get("headers"):
        builder.with_headers(headers)
    if is_verified := kwargs.get("is_verified"):
        builder.verified(is_verified)
    if retry_count := kwargs.get("retry_count"):
        builder.with_retries(retry_count)
    if timeout := kwargs.get("timeout"):
        builder.with_timeout(timeout)
    if metadata := kwargs.get("metadata"):
        builder.with_metadata(metadata)
    
    return builder.build()
