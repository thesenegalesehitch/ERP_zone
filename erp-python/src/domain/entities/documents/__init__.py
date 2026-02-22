"""
Document Entity for ERP System.

This module provides the Document entity for managing documents
following Clean Architecture principles.
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional, Dict, Any, List
from enum import Enum


class DocumentStatus(str, Enum):
    """Document status enumeration."""
    DRAFT = "draft"
    PENDING = "pending"
    APPROVED = "approved"
    PUBLISHED = "published"
    ARCHIVED = "archived"
    CANCELLED = "cancelled"


class DocumentType(str, Enum):
    """Document type enumeration."""
    CONTRACT = "contract"
    INVOICE = "invoice"
    QUOTE = "quote"
    REPORT = "report"
    MANUAL = "manual"
    POLICY = "policy"
    PROCEDURE = "procedure"
    FORM = "form"
    TEMPLATE = "template"
    OTHER = "other"


@dataclass(frozen=True)
class Document:
    """
    Document entity representing a document in the ERP system.
    
    This entity follows Clean Architecture principles and is immutable.
    
    Attributes:
        id: Unique identifier for the document
        document_number: Human-readable document number
        title: Document title
        description: Document description
        document_type: Type of document
        status: Current status
        file_url: URL to the document file
        file_type: MIME type of the document
        file_size: Size of the document in bytes
        version: Document version number
        entity_type: Type of entity the document is associated with
        entity_id: ID of the associated entity
        author_id: ID of the document author
        author_name: Name of the document author
        tags: List of tags
        metadata: Additional metadata
        created_at: Timestamp when created
        updated_at: Timestamp when last updated
        published_at: Timestamp when published
    """
    id: str
    document_number: str
    title: str
    description: str
    document_type: DocumentType
    status: DocumentStatus
    file_url: str
    file_type: str
    file_size: int
    version: int = 1
    entity_type: Optional[str] = None
    entity_id: Optional[str] = None
    author_id: Optional[str] = None
    author_name: Optional[str] = None
    tags: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime = field(default_factory=datetime.utcnow)
    published_at: Optional[datetime] = None
    
    def __post_init__(self):
        """Validate document after initialization."""
        if not self.document_number:
            raise ValueError("document_number cannot be empty")
        if not self.title:
            raise ValueError("title cannot be empty")
        if not self.file_url:
            raise ValueError("file_url cannot be empty")
        if self.version < 1:
            raise ValueError("version must be at least 1")
        if self.file_size < 0:
            raise ValueError("file_size cannot be negative")
    
    @property
    def is_published(self) -> bool:
        """Check if document is published."""
        return self.status == DocumentStatus.PUBLISHED
    
    @property
    def is_archived(self) -> bool:
        """Check if document is archived."""
        return self.status == DocumentStatus.ARCHIVED
    
    @property
    def file_extension(self) -> str:
        """Get file extension."""
        if "." in self.file_url:
            return self.file_url.rsplit(".", 1)[-1].lower()
        return ""
    
    @property
    def file_size_mb(self) -> float:
        """Get file size in MB."""
        return self.file_size / (1024 * 1024)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert document to dictionary."""
        return {
            "id": self.id,
            "document_number": self.document_number,
            "title": self.title,
            "description": self.description,
            "document_type": self.document_type.value,
            "status": self.status.value,
            "file_url": self.file_url,
            "file_type": self.file_type,
            "file_size": self.file_size,
            "file_size_mb": round(self.file_size_mb, 2),
            "version": self.version,
            "entity_type": self.entity_type,
            "entity_id": self.entity_id,
            "author_id": self.author_id,
            "author_name": self.author_name,
            "tags": self.tags,
            "metadata": self.metadata,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
            "published_at": self.published_at.isoformat() if self.published_at else None,
            "is_published": self.is_published,
            "is_archived": self.is_archived,
            "file_extension": self.file_extension
        }


class DocumentBuilder:
    """Builder for creating Document instances."""
    
    def __init__(self):
        self._id: Optional[str] = None
        self._document_number: Optional[str] = None
        self._title: Optional[str] = None
        self._description: str = ""
        self._document_type: DocumentType = DocumentType.OTHER
        self._status: DocumentStatus = DocumentStatus.DRAFT
        self._file_url: Optional[str] = None
        self._file_type: str = "application/octet-stream"
        self._file_size: int = 0
        self._version: int = 1
        self._entity_type: Optional[str] = None
        self._entity_id: Optional[str] = None
        self._author_id: Optional[str] = None
        self._author_name: Optional[str] = None
        self._tags: List[str] = []
        self._metadata: Dict[str, Any] = {}
    
    def with_id(self, document_id: str) -> "DocumentBuilder":
        self._id = document_id
        return self
    
    def with_number(self, document_number: str) -> "DocumentBuilder":
        self._document_number = document_number
        return self
    
    def with_title(self, title: str) -> "DocumentBuilder":
        self._title = title
        return self
    
    def with_description(self, description: str) -> "DocumentBuilder":
        self._description = description
        return self
    
    def with_type(self, document_type: DocumentType) -> "DocumentBuilder":
        self._document_type = document_type
        return self
    
    def with_status(self, status: DocumentStatus) -> "DocumentBuilder":
        self._status = status
        return self
    
    def with_file(self, file_url: str, file_type: str, file_size: int) -> "DocumentBuilder":
        self._file_url = file_url
        self._file_type = file_type
        self._file_size = file_size
        return self
    
    def with_version(self, version: int) -> "DocumentBuilder":
        self._version = version
        return self
    
    def for_entity(self, entity_type: str, entity_id: str) -> "DocumentBuilder":
        self._entity_type = entity_type
        self._entity_id = entity_id
        return self
    
    def by_author(self, author_id: str, author_name: str) -> "DocumentBuilder":
        self._author_id = author_id
        self._author_name = author_name
        return self
    
    def with_tags(self, tags: List[str]) -> "DocumentBuilder":
        self._tags = tags
        return self
    
    def with_metadata(self, metadata: Dict[str, Any]) -> "DocumentBuilder":
        self._metadata = metadata
        return self
    
    def build(self) -> Document:
        from uuid import uuid4
        
        if not self._id:
            self._id = str(uuid4())
        if not self._document_number:
            from time import time
            self._document_number = f"DOC-{int(time())}"
        if not self._title:
            raise ValueError("title is required")
        if not self._file_url:
            raise ValueError("file_url is required")
        
        return Document(
            id=self._id,
            document_number=self._document_number,
            title=self._title,
            description=self._description,
            document_type=self._document_type,
            status=self._status,
            file_url=self._file_url,
            file_type=self._file_type,
            file_size=self._file_size,
            version=self._version,
            entity_type=self._entity_type,
            entity_id=self._entity_id,
            author_id=self._author_id,
            author_name=self._author_name,
            tags=self._tags,
            metadata=self._metadata
        )


# Factory function
def create_document(
    title: str,
    file_url: str,
    file_type: str,
    file_size: int,
    **kwargs
) -> Document:
    """Factory function to create a document."""
    builder = DocumentBuilder()
    builder.with_title(title)
    builder.with_file(file_url, file_type, file_size)
    
    if document_number := kwargs.get("document_number"):
        builder.with_number(document_number)
    if description := kwargs.get("description"):
        builder.with_description(description)
    if document_type := kwargs.get("document_type"):
        builder.with_type(document_type)
    if status := kwargs.get("status"):
        builder.with_status(status)
    if version := kwargs.get("version"):
        builder.with_version(version)
    if entity_type := kwargs.get("entity_type"):
        entity_id = kwargs.get("entity_id", "")
        builder.for_entity(entity_type, entity_id)
    if author_id := kwargs.get("author_id"):
        author_name = kwargs.get("author_name", "")
        builder.by_author(author_id, author_name)
    if tags := kwargs.get("tags"):
        builder.with_tags(tags)
    if metadata := kwargs.get("metadata"):
        builder.with_metadata(metadata)
    
    return builder.build()
