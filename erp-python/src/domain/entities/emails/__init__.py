"""
Email Queue Entity for ERP System.

This module provides the EmailQueue entity for managing email queue
following Clean Architecture principles.
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional, Dict, Any, List
from enum import Enum


class EmailStatus(str, Enum):
    """Email status enumeration."""
    PENDING = "pending"
    QUEUED = "queued"
    SENDING = "sending"
    SENT = "sent"
    FAILED = "failed"
    CANCELLED = "cancelled"


class EmailPriority(str, Enum):
    """Email priority enumeration."""
    LOW = "low"
    NORMAL = "normal"
    HIGH = "high"
    URGENT = "urgent"


@dataclass(frozen=True)
class EmailAttachment:
    """
    Value Object representing an email attachment.
    Immutable and validated.
    """
    id: str
    filename: str
    file_url: str
    content_type: str
    size: int
    
    def __post_init__(self):
        if not self.filename:
            raise ValueError("filename cannot be empty")
        if not self.file_url:
            raise ValueError("file_url cannot be empty")
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "filename": self.filename,
            "file_url": self.file_url,
            "content_type": self.content_type,
            "size": self.size
        }


@dataclass(frozen=True)
class EmailQueue:
    """
    EmailQueue entity representing an email in the queue.
    
    This entity follows Clean Architecture principles and is immutable.
    
    Attributes:
        id: Unique identifier for the email
        subject: Email subject
        body: Email body (HTML or plain text)
        from_email: Sender email
        from_name: Sender name
        to_recipients: List of recipient emails
        cc_recipients: List of CC recipients
        bcc_recipients: List of BCC recipients
        status: Current status
        priority: Email priority
        attachments: List of attachments
        headers: Custom email headers
        retry_count: Number of retry attempts
        max_retries: Maximum retry attempts
        scheduled_at: When to send the email
        sent_at: When the email was sent
        error_message: Error message if failed
        metadata: Additional metadata
        created_at: Timestamp when created
        updated_at: Timestamp when last updated
    """
    id: str
    subject: str
    body: str
    from_email: str
    from_name: Optional[str]
    to_recipients: List[str]
    cc_recipients: List[str] = field(default_factory=list)
    bcc_recipients: List[str] = field(default_factory=list)
    status: EmailStatus = EmailStatus.PENDING
    priority: EmailPriority = EmailPriority.NORMAL
    attachments: List[EmailAttachment] = field(default_factory=list)
    headers: Dict[str, str] = field(default_factory=dict)
    retry_count: int = 0
    max_retries: int = 3
    scheduled_at: Optional[datetime] = None
    sent_at: Optional[datetime] = None
    error_message: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime = field(default_factory=datetime.utcnow)
    
    def __post_init__(self):
        """Validate email after initialization."""
        if not self.subject:
            raise ValueError("subject cannot be empty")
        if not self.body:
            raise ValueError("body cannot be empty")
        if not self.from_email:
            raise ValueError("from_email cannot be empty")
        if not self.to_recipients:
            raise ValueError("to_recipients cannot be empty")
        if self.retry_count < 0:
            raise ValueError("retry_count cannot be negative")
        if self.max_retries < 0:
            raise ValueError("max_retries cannot be negative")
    
    @property
    def is_sent(self) -> bool:
        """Check if email was sent."""
        return self.status == EmailStatus.SENT
    
    @property
    def is_pending(self) -> bool:
        """Check if email is pending."""
        return self.status in [EmailStatus.PENDING, EmailStatus.QUEUED]
    
    @property
    def is_failed(self) -> bool:
        """Check if email failed."""
        return self.status == EmailStatus.FAILED
    
    @property
    def can_retry(self) -> bool:
        """Check if email can be retried."""
        return self.retry_count < self.max_retries
    
    @property
    def recipient_count(self) -> int:
        """Get total recipient count."""
        return len(self.to_recipients) + len(self.cc_recipients) + len(self.bcc_recipients)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert email to dictionary."""
        return {
            "id": self.id,
            "subject": self.subject,
            "body": self.body,
            "from_email": self.from_email,
            "from_name": self.from_name,
            "to_recipients": self.to_recipients,
            "cc_recipients": self.cc_recipients,
            "bcc_recipients": self.bcc_recipients,
            "status": self.status.value,
            "priority": self.priority.value,
            "attachments": [a.to_dict() for a in self.attachments],
            "headers": self.headers,
            "retry_count": self.retry_count,
            "max_retries": self.max_retries,
            "scheduled_at": self.scheduled_at.isoformat() if self.scheduled_at else None,
            "sent_at": self.sent_at.isoformat() if self.sent_at else None,
            "error_message": self.error_message,
            "metadata": self.metadata,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
            "is_sent": self.is_sent,
            "is_pending": self.is_pending,
            "is_failed": self.is_failed,
            "can_retry": self.can_retry,
            "recipient_count": self.recipient_count
        }


class EmailQueueBuilder:
    """Builder for creating EmailQueue instances."""
    
    def __init__(self):
        self._id: Optional[str] = None
        self._subject: Optional[str] = None
        self._body: Optional[str] = None
        self._from_email: Optional[str] = None
        self._from_name: Optional[str] = None
        self._to_recipients: List[str] = []
        self._cc_recipients: List[str] = []
        self._bcc_recipients: List[str] = []
        self._status: EmailStatus = EmailStatus.PENDING
        self._priority: EmailPriority = EmailPriority.NORMAL
        self._attachments: List[EmailAttachment] = []
        self._headers: Dict[str, str] = {}
        self._retry_count: int = 0
        self._max_retries: int = 3
        self._scheduled_at: Optional[datetime] = None
        self._metadata: Dict[str, Any] = {}
    
    def with_id(self, email_id: str) -> "EmailQueueBuilder":
        self._id = email_id
        return self
    
    def with_subject(self, subject: str) -> "EmailQueueBuilder":
        self._subject = subject
        return self
    
    def with_body(self, body: str) -> "EmailQueueBuilder":
        self._body = body
        return self
    
    def from_address(self, email: str, name: Optional[str] = None) -> "EmailQueueBuilder":
        self._from_email = email
        self._from_name = name
        return self
    
    def to(self, recipients: List[str]) -> "EmailQueueBuilder":
        self._to_recipients = recipients
        return self
    
    def cc(self, recipients: List[str]) -> "EmailQueueBuilder":
        self._cc_recipients = recipients
        return self
    
    def bcc(self, recipients: List[str]) -> "EmailQueueBuilder":
        self._bcc_recipients = recipients
        return self
    
    def with_status(self, status: EmailStatus) -> "EmailQueueBuilder":
        self._status = status
        return self
    
    def with_priority(self, priority: EmailPriority) -> "EmailQueueBuilder":
        self._priority = priority
        return self
    
    def with_attachments(self, attachments: List[EmailAttachment]) -> "EmailQueueBuilder":
        self._attachments = attachments
        return self
    
    def with_headers(self, headers: Dict[str, str]) -> "EmailQueueBuilder":
        self._headers = headers
        return self
    
    def with_retries(self, max_retries: int) -> "EmailQueueBuilder":
        self._max_retries = max_retries
        return self
    
    def scheduled_for(self, scheduled_at: datetime) -> "EmailQueueBuilder":
        self._scheduled_at = scheduled_at
        return self
    
    def with_metadata(self, metadata: Dict[str, Any]) -> "EmailQueueBuilder":
        self._metadata = metadata
        return self
    
    def build(self) -> EmailQueue:
        from uuid import uuid4
        
        if not self._id:
            self._id = str(uuid4())
        if not self._subject:
            raise ValueError("subject is required")
        if not self._body:
            raise ValueError("body is required")
        if not self._from_email:
            raise ValueError("from_email is required")
        if not self._to_recipients:
            raise ValueError("to_recipients is required")
        
        return EmailQueue(
            id=self._id,
            subject=self._subject,
            body=self._body,
            from_email=self._from_email,
            from_name=self._from_name,
            to_recipients=self._to_recipients,
            cc_recipients=self._cc_recipients,
            bcc_recipients=self._bcc_recipients,
            status=self._status,
            priority=self._priority,
            attachments=self._attachments,
            headers=self._headers,
            retry_count=self._retry_count,
            max_retries=self._max_retries,
            scheduled_at=self._scheduled_at,
            metadata=self._metadata
        )


# Factory functions
def create_email_attachment(
    filename: str,
    file_url: str,
    content_type: str,
    size: int
) -> EmailAttachment:
    """Factory function to create an email attachment."""
    from uuid import uuid4
    
    return EmailAttachment(
        id=str(uuid4()),
        filename=filename,
        file_url=file_url,
        content_type=content_type,
        size=size
    )


def create_email(
    subject: str,
    body: str,
    from_email: str,
    to_recipients: List[str],
    **kwargs
) -> EmailQueue:
    """Factory function to create an email."""
    builder = EmailQueueBuilder()
    builder.with_subject(subject)
    builder.with_body(body)
    builder.from_address(from_email, kwargs.get("from_name"))
    builder.to(to_recipients)
    
    if cc := kwargs.get("cc_recipients"):
        builder.cc(cc)
    if bcc := kwargs.get("bcc_recipients"):
        builder.bcc(bcc)
    if status := kwargs.get("status"):
        builder.with_status(status)
    if priority := kwargs.get("priority"):
        builder.with_priority(priority)
    if attachments := kwargs.get("attachments"):
        builder.with_attachments(attachments)
    if headers := kwargs.get("headers"):
        builder.with_headers(headers)
    if max_retries := kwargs.get("max_retries"):
        builder.with_retries(max_retries)
    if scheduled_at := kwargs.get("scheduled_at"):
        builder.scheduled_for(scheduled_at)
    if metadata := kwargs.get("metadata"):
        builder.with_metadata(metadata)
    
    return builder.build()
