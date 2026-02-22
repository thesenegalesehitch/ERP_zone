"""
Help Desk Entity for ERP System.

This module provides entities for ticketing and support management
following Clean Architecture principles.
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional, Dict, Any, List
from enum import Enum
from uuid import uuid4


class TicketStatus(str, Enum):
    """Ticket status enumeration."""
    OPEN = "open"
    IN_PROGRESS = "in_progress"
    PENDING = "pending"
    RESOLVED = "resolved"
    CLOSED = "closed"
    CANCELLED = "cancelled"


class TicketPriority(str, Enum):
    """Ticket priority enumeration."""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    URGENT = "urgent"
    CRITICAL = "critical"


class TicketCategory(str, Enum):
    """Ticket category enumeration."""
    TECHNICAL = "technical"
    BILLING = "billing"
    SALES = "sales"
    GENERAL = "general"
    FEATURE_REQUEST = "feature_request"
    BUG_REPORT = "bug_report"


@dataclass(frozen=True)
class TicketComment:
    """
    Value Object representing a ticket comment.
    Immutable and validated.
    """
    id: str
    author_id: str
    author_name: str
    author_email: str
    content: str
    is_internal: bool = False
    attachments: List[str] = field(default_factory=list)
    created_at: datetime = field(default_factory=datetime.utcnow)
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "author_id": self.author_id,
            "author_name": self.author_name,
            "author_email": self.author_email,
            "content": self.content,
            "is_internal": self.is_internal,
            "attachments": self.attachments,
            "created_at": self.created_at.isoformat()
        }


@dataclass(frozen=True)
class TicketAttachment:
    """
    Value Object representing a ticket attachment.
    Immutable and validated.
    """
    id: str
    filename: str
    file_path: str
    file_size: int
    mime_type: str
    uploaded_by: str
    uploaded_at: datetime = field(default_factory=datetime.utcnow)
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "filename": self.filename,
            "file_path": self.file_path,
            "file_size": self.file_size,
            "mime_type": self.mime_type,
            "uploaded_by": self.uploaded_by,
            "uploaded_at": self.uploaded_at.isoformat()
        }


@dataclass(frozen=True)
class Ticket:
    """
    Help Desk Ticket entity for support management.
    
    This entity follows Clean Architecture principles and is immutable.
    
    Attributes:
        id: Unique identifier
        ticket_number: Human-readable ticket number
        subject: Ticket subject
        description: Detailed description
        status: Current ticket status
        priority: Ticket priority
        category: Ticket category
        requester_id: Requester user ID
        requester_name: Requester name
        requester_email: Requester email
        assigned_to: Assigned agent user ID
        assigned_name: Assigned agent name
        tags: List of tags
        comments: List of comments
        attachments: List of attachments
        resolution: Resolution notes
        related_tickets: Related ticket IDs
        sla_deadline: SLA deadline
        first_response_at: First response timestamp
        resolved_at: Resolution timestamp
        closed_at: Closure timestamp
        created_at: Creation timestamp
        updated_at: Last update timestamp
    """
    id: str
    ticket_number: str
    subject: str
    description: str
    status: TicketStatus
    priority: TicketPriority
    category: TicketCategory
    requester_id: str
    requester_name: str
    requester_email: str
    assigned_to: Optional[str] = None
    assigned_name: str = ""
    tags: List[str] = field(default_factory=list)
    comments: List[TicketComment] = field(default_factory=list)
    attachments: List[TicketAttachment] = field(default_factory=list)
    resolution: str = ""
    related_tickets: List[str] = field(default_factory=list)
    sla_deadline: Optional[datetime] = None
    first_response_at: Optional[datetime] = None
    resolved_at: Optional[datetime] = None
    closed_at: Optional[datetime] = None
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime = field(default_factory=datetime.utcnow)
    
    def __post_init__(self):
        if not self.subject:
            raise ValueError("subject cannot be empty")
        if not self.requester_id:
            raise ValueError("requester_id cannot be empty")
    
    @property
    def is_open(self) -> bool:
        return self.status in [TicketStatus.OPEN, TicketStatus.IN_PROGRESS]
    
    @property
    def is_resolved(self) -> bool:
        return self.status in [TicketStatus.RESOLVED, TicketStatus.CLOSED]
    
    @property
    def is_assigned(self) -> bool:
        return self.assigned_to is not None
    
    @property
    def is_overdue(self) -> bool:
        if not self.sla_deadline:
            return False
        return datetime.utcnow() > self.sla_deadline and not self.is_resolved
    
    @property
    def comment_count(self) -> int:
        return len(self.comments)
    
    @property
    def response_time_minutes(self) -> Optional[int]:
        if not self.first_response_at:
            return None
        delta = self.first_response_at - self.created_at
        return int(delta.total_seconds() / 60)
    
    @property
    def resolution_time_minutes(self) -> Optional[int]:
        if not self.resolved_at:
            return None
        delta = self.resolved_at - self.created_at
        return int(delta.total_seconds() / 60)
    
    def assign(self, user_id: str, user_name: str) -> None:
        """Assign the ticket to an agent."""
        self.assigned_to = user_id
        self.assigned_name = user_name
        if self.status == TicketStatus.OPEN:
            self.status = TicketStatus.IN_PROGRESS
    
    def add_comment(self, author_id: str, author_name: str, author_email: str, content: str, is_internal: bool = False) -> None:
        """Add a comment to the ticket."""
        comment = TicketComment(
            id=str(uuid4()),
            author_id=author_id,
            author_name=author_name,
            author_email=author_email,
            content=content,
            is_internal=is_internal
        )
        self.comments.append(comment)
        
        if not self.first_response_at and not is_internal:
            self.first_response_at = datetime.utcnow()
        
        if self.status == TicketStatus.PENDING:
            self.status = TicketStatus.IN_PROGRESS
    
    def resolve(self, resolution: str) -> None:
        """Resolve the ticket."""
        self.status = TicketStatus.RESOLVED
        self.resolution = resolution
        self.resolved_at = datetime.utcnow()
    
    def close(self) -> None:
        """Close the ticket."""
        self.status = TicketStatus.CLOSED
        self.closed_at = datetime.utcnow()
    
    def reopen(self, reason: str) -> None:
        """Reopen a closed ticket."""
        self.status = TicketStatus.OPEN
        self.resolution += f"\n[REOPENED: {reason}]"
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "ticket_number": self.ticket_number,
            "subject": self.subject,
            "description": self.description,
            "status": self.status.value,
            "priority": self.priority.value,
            "category": self.category.value,
            "requester_id": self.requester_id,
            "requester_name": self.requester_name,
            "requester_email": self.requester_email,
            "assigned_to": self.assigned_to,
            "assigned_name": self.assigned_name,
            "tags": self.tags,
            "comments": [c.to_dict() for c in self.comments],
            "attachments": [a.to_dict() for a in self.attachments],
            "resolution": self.resolution,
            "related_tickets": self.related_tickets,
            "sla_deadline": self.sla_deadline.isoformat() if self.sla_deadline else None,
            "first_response_at": self.first_response_at.isoformat() if self.first_response_at else None,
            "resolved_at": self.resolved_at.isoformat() if self.resolved_at else None,
            "closed_at": self.closed_at.isoformat() if self.closed_at else None,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
            "is_open": self.is_open,
            "is_resolved": self.is_resolved,
            "is_assigned": self.is_assigned,
            "is_overdue": self.is_overdue,
            "comment_count": self.comment_count,
            "response_time_minutes": self.response_time_minutes,
            "resolution_time_minutes": self.resolution_time_minutes
        }


class TicketBuilder:
    """Builder for creating Ticket instances."""
    
    def __init__(self):
        self._id: Optional[str] = None
        self._ticket_number: Optional[str] = None
        self._subject: Optional[str] = None
        self._description: str = ""
        self._status: TicketStatus = TicketStatus.OPEN
        self._priority: TicketPriority = TicketPriority.MEDIUM
        self._category: TicketCategory = TicketCategory.GENERAL
        self._requester_id: Optional[str] = None
        self._requester_name: str = ""
        self._requester_email: str = ""
        self._assigned_to: Optional[str] = None
        self._assigned_name: str = ""
        self._tags: List[str] = []
        self._comments: List[TicketComment] = []
        self._attachments: List[TicketAttachment] = []
        self._related_tickets: List[str] = []
        self._sla_deadline: Optional[datetime] = None
        self._metadata: Dict[str, Any] = {}
    
    def with_id(self, ticket_id: str) -> "TicketBuilder":
        self._id = ticket_id
        return self
    
    def with_ticket_number(self, ticket_number: str) -> "TicketBuilder":
        self._ticket_number = ticket_number
        return self
    
    def with_subject(self, subject: str) -> "TicketBuilder":
        self._subject = subject
        return self
    
    def with_description(self, description: str) -> "TicketBuilder":
        self._description = description
        return self
    
    def with_status(self, status: TicketStatus) -> "TicketBuilder":
        self._status = status
        return self
    
    def with_priority(self, priority: TicketPriority) -> "TicketBuilder":
        self._priority = priority
        return self
    
    def with_category(self, category: TicketCategory) -> "TicketBuilder":
        self._category = category
        return self
    
    def from_requester(self, requester_id: str, requester_name: str, requester_email: str) -> "TicketBuilder":
        self._requester_id = requester_id
        self._requester_name = requester_name
        self._requester_email = requester_email
        return self
    
    def assigned_to(self, user_id: str, user_name: str) -> "TicketBuilder":
        self._assigned_to = user_id
        self._assigned_name = user_name
        return self
    
    def with_tags(self, tags: List[str]) -> "TicketBuilder":
        self._tags = tags
        return self
    
    def with_comments(self, comments: List[TicketComment]) -> "TicketBuilder":
        self._comments = comments
        return self
    
    def with_attachments(self, attachments: List[TicketAttachment]) -> "TicketBuilder":
        self._attachments = attachments
        return self
    
    def with_related_tickets(self, tickets: List[str]) -> "TicketBuilder":
        self._related_tickets = tickets
        return self
    
    def with_sla_deadline(self, deadline: datetime) -> "TicketBuilder":
        self._sla_deadline = deadline
        return self
    
    def with_metadata(self, metadata: Dict[str, Any]) -> "TicketBuilder":
        self._metadata = metadata
        return self
    
    def build(self) -> Ticket:
        if not self._id:
            self._id = str(uuid4())
        if not self._ticket_number:
            from time import time
            self._ticket_number = f"TKT-{int(time())}"
        if not self._subject:
            raise ValueError("subject is required")
        if not self._requester_id:
            raise ValueError("requester_id is required")
        
        return Ticket(
            id=self._id,
            ticket_number=self._ticket_number,
            subject=self._subject,
            description=self._description,
            status=self._status,
            priority=self._priority,
            category=self._category,
            requester_id=self._requester_id,
            requester_name=self._requester_name,
            requester_email=self._requester_email,
            assigned_to=self._assigned_to,
            assigned_name=self._assigned_name,
            tags=self._tags,
            comments=self._comments,
            attachments=self._attachments,
            related_tickets=self._related_tickets,
            sla_deadline=self._sla_deadline,
            metadata=self._metadata
        )


def create_ticket(
    subject: str,
    requester_id: str,
    requester_name: str,
    requester_email: str,
    **kwargs
) -> Ticket:
    """Factory function to create a ticket."""
    builder = TicketBuilder()
    builder.with_subject(subject)
    builder.from_requester(requester_id, requester_name, requester_email)
    
    if ticket_number := kwargs.get("ticket_number"):
        builder.with_ticket_number(ticket_number)
    if description := kwargs.get("description"):
        builder.with_description(description)
    if status := kwargs.get("status"):
        builder.with_status(status)
    if priority := kwargs.get("priority"):
        builder.with_priority(priority)
    if category := kwargs.get("category"):
        builder.with_category(category)
    if assigned_to := kwargs.get("assigned_to"):
        assigned_name = kwargs.get("assigned_name", "")
        builder.assigned_to(assigned_to, assigned_name)
    if tags := kwargs.get("tags"):
        builder.with_tags(tags)
    if related_tickets := kwargs.get("related_tickets"):
        builder.with_related_tickets(related_tickets)
    if sla_deadline := kwargs.get("sla_deadline"):
        builder.with_sla_deadline(sla_deadline)
    if metadata := kwargs.get("metadata"):
        builder.with_metadata(metadata)
    
    return builder.build()


def create_ticket_comment(
    author_id: str,
    author_name: str,
    author_email: str,
    content: str,
    **kwargs
) -> TicketComment:
    """Factory function to create a ticket comment."""
    return TicketComment(
        id=str(uuid4()),
        author_id=author_id,
        author_name=author_name,
        author_email=author_email,
        content=content,
        is_internal=kwargs.get("is_internal", False)
    )
