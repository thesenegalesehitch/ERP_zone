"""
Notification Entity for ERP System.

This module provides the Notification entity for managing notifications
following Clean Architecture principles.
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional, Dict, Any, List
from enum import Enum


class NotificationType(str, Enum):
    """Notification type enumeration."""
    INFO = "info"
    SUCCESS = "success"
    WARNING = "warning"
    ERROR = "error"
    SYSTEM = "system"


class NotificationChannel(str, Enum):
    """Notification channel enumeration."""
    IN_APP = "in_app"
    EMAIL = "email"
    SMS = "sms"
    PUSH = "push"
    WEBHOOK = "webhook"


class NotificationStatus(str, Enum):
    """Notification status enumeration."""
    PENDING = "pending"
    SENT = "sent"
    DELIVERED = "delivered"
    READ = "read"
    FAILED = "failed"


@dataclass(frozen=True)
class Notification:
    """
    Notification entity representing a notification in the ERP system.
    
    This entity follows Clean Architecture principles and is immutable.
    
    Attributes:
        id: Unique identifier for the notification
        title: Notification title
        message: Notification message
        notification_type: Type of notification
        channel: Delivery channel
        status: Current status
        user_id: ID of recipient user
        user_email: Email of recipient
        sender_id: ID of sender (optional)
        sender_name: Name of sender
        entity_type: Type of associated entity
        entity_id: ID of associated entity
        action_url: URL for action
        metadata: Additional metadata
        scheduled_at: When to send notification
        sent_at: When notification was sent
        read_at: When notification was read
        created_at: Timestamp when created
    """
    id: str
    title: str
    message: str
    notification_type: NotificationType
    channel: NotificationChannel
    status: NotificationStatus
    user_id: str
    user_email: str
    sender_id: Optional[str] = None
    sender_name: Optional[str] = None
    entity_type: Optional[str] = None
    entity_id: Optional[str] = None
    action_url: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)
    scheduled_at: Optional[datetime] = None
    sent_at: Optional[datetime] = None
    read_at: Optional[datetime] = None
    created_at: datetime = field(default_factory=datetime.utcnow)
    
    def __post_init__(self):
        """Validate notification after initialization."""
        if not self.title:
            raise ValueError("title cannot be empty")
        if not self.message:
            raise ValueError("message cannot be empty")
        if not self.user_id:
            raise ValueError("user_id cannot be empty")
    
    @property
    def is_sent(self) -> bool:
        """Check if notification was sent."""
        return self.status in [NotificationStatus.SENT, NotificationStatus.DELIVERED, NotificationStatus.READ]
    
    @property
    def is_read(self) -> bool:
        """Check if notification was read."""
        return self.status == NotificationStatus.READ
    
    @property
    def is_pending(self) -> bool:
        """Check if notification is pending."""
        return self.status == NotificationStatus.PENDING
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert notification to dictionary."""
        return {
            "id": self.id,
            "title": self.title,
            "message": self.message,
            "notification_type": self.notification_type.value,
            "channel": self.channel.value,
            "status": self.status.value,
            "user_id": self.user_id,
            "user_email": self.user_email,
            "sender_id": self.sender_id,
            "sender_name": self.sender_name,
            "entity_type": self.entity_type,
            "entity_id": self.entity_id,
            "action_url": self.action_url,
            "metadata": self.metadata,
            "scheduled_at": self.scheduled_at.isoformat() if self.scheduled_at else None,
            "sent_at": self.sent_at.isoformat() if self.sent_at else None,
            "read_at": self.read_at.isoformat() if self.read_at else None,
            "created_at": self.created_at.isoformat(),
            "is_sent": self.is_sent,
            "is_read": self.is_read,
            "is_pending": self.is_pending
        }


class NotificationBuilder:
    """Builder for creating Notification instances."""
    
    def __init__(self):
        self._id: Optional[str] = None
        self._title: Optional[str] = None
        self._message: Optional[str] = None
        self._notification_type: NotificationType = NotificationType.INFO
        self._channel: NotificationChannel = NotificationChannel.IN_APP
        self._status: NotificationStatus = NotificationStatus.PENDING
        self._user_id: Optional[str] = None
        self._user_email: Optional[str] = None
        self._sender_id: Optional[str] = None
        self._sender_name: Optional[str] = None
        self._entity_type: Optional[str] = None
        self._entity_id: Optional[str] = None
        self._action_url: Optional[str] = None
        self._metadata: Dict[str, Any] = {}
        self._scheduled_at: Optional[datetime] = None
    
    def with_id(self, notification_id: str) -> "NotificationBuilder":
        self._id = notification_id
        return self
    
    def with_title(self, title: str) -> "NotificationBuilder":
        self._title = title
        return self
    
    def with_message(self, message: str) -> "NotificationBuilder":
        self._message = message
        return self
    
    def with_type(self, notification_type: NotificationType) -> "NotificationBuilder":
        self._notification_type = notification_type
        return self
    
    def via_channel(self, channel: NotificationChannel) -> "NotificationBuilder":
        self._channel = channel
        return self
    
    def with_status(self, status: NotificationStatus) -> "NotificationBuilder":
        self._status = status
        return self
    
    def to_user(self, user_id: str, user_email: str) -> "NotificationBuilder":
        self._user_id = user_id
        self._user_email = user_email
        return self
    
    def from_sender(self, sender_id: str, sender_name: str) -> "NotificationBuilder":
        self._sender_id = sender_id
        self._sender_name = sender_name
        return self
    
    def for_entity(self, entity_type: str, entity_id: str) -> "NotificationBuilder":
        self._entity_type = entity_type
        self._entity_id = entity_id
        return self
    
    def with_action_url(self, action_url: str) -> "NotificationBuilder":
        self._action_url = action_url
        return self
    
    def with_metadata(self, metadata: Dict[str, Any]) -> "NotificationBuilder":
        self._metadata = metadata
        return self
    
    def scheduled_for(self, scheduled_at: datetime) -> "NotificationBuilder":
        self._scheduled_at = scheduled_at
        return self
    
    def build(self) -> Notification:
        from uuid import uuid4
        
        if not self._id:
            self._id = str(uuid4())
        if not self._title:
            raise ValueError("title is required")
        if not self._message:
            raise ValueError("message is required")
        if not self._user_id:
            raise ValueError("user_id is required")
        
        return Notification(
            id=self._id,
            title=self._title,
            message=self._message,
            notification_type=self._notification_type,
            channel=self._channel,
            status=self._status,
            user_id=self._user_id,
            user_email=self._user_email or "",
            sender_id=self._sender_id,
            sender_name=self._sender_name,
            entity_type=self._entity_type,
            entity_id=self._entity_id,
            action_url=self._action_url,
            metadata=self._metadata,
            scheduled_at=self._scheduled_at
        )


# Factory function
def create_notification(
    title: str,
    message: str,
    user_id: str,
    **kwargs
) -> Notification:
    """Factory function to create a notification."""
    builder = NotificationBuilder()
    builder.with_title(title)
    builder.with_message(message)
    builder.to_user(user_id, kwargs.get("user_email", ""))
    
    if notification_type := kwargs.get("notification_type"):
        builder.with_type(notification_type)
    if channel := kwargs.get("channel"):
        builder.via_channel(channel)
    if status := kwargs.get("status"):
        builder.with_status(status)
    if sender_id := kwargs.get("sender_id"):
        sender_name = kwargs.get("sender_name", "")
        builder.from_sender(sender_id, sender_name)
    if entity_type := kwargs.get("entity_type"):
        entity_id = kwargs.get("entity_id", "")
        builder.for_entity(entity_type, entity_id)
    if action_url := kwargs.get("action_url"):
        builder.with_action_url(action_url)
    if metadata := kwargs.get("metadata"):
        builder.with_metadata(metadata)
    if scheduled_at := kwargs.get("scheduled_at"):
        builder.scheduled_for(scheduled_at)
    
    return builder.build()
