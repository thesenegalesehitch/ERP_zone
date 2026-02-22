"""
Knowledge Base Entity for ERP System.

This module provides entities for managing knowledge base articles
following Clean Architecture principles.
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional, Dict, Any, List
from enum import Enum
from uuid import uuid4


class ArticleStatus(str, Enum):
    """Article status enumeration."""
    DRAFT = "draft"
    PUBLISHED = "published"
    ARCHIVED = "archived"
    UNDER_REVIEW = "under_review"


class ArticleVisibility(str, Enum):
    """Article visibility enumeration."""
    PUBLIC = "public"
    INTERNAL = "internal"
    PRIVATE = "private"


@dataclass(frozen=True)
class ArticleCategory:
    """
    Value Object representing an article category.
    Immutable and validated.
    """
    id: str
    name: str
    description: str
    slug: str
    parent_id: Optional[str] = None
    order: int = 0
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "slug": self.slug,
            "parent_id": self.parent_id,
            "order": self.order
        }


@dataclass(frozen=True)
class Article:
    """
    Knowledge Base Article entity.
    
    This entity follows Clean Architecture principles and is immutable.
    
    Attributes:
        id: Unique identifier
        title: Article title
        slug: URL-friendly slug
        content: Article content (markdown)
        summary: Brief summary
        status: Publication status
        visibility: Who can view
        category_id: Category identifier
        author_id: Author user ID
        author_name: Author display name
        tags: List of tags
        view_count: Number of views
        helpful_count: Times marked helpful
        not_helpful_count: Times marked not helpful
        versions: Content version history
        metadata: Additional metadata
        created_at: Creation timestamp
        updated_at: Last update timestamp
        published_at: Publication timestamp
    """
    id: str
    title: str
    slug: str
    content: str
    summary: str
    status: ArticleStatus
    visibility: ArticleVisibility
    category_id: str
    author_id: str
    author_name: str
    tags: List[str] = field(default_factory=list)
    view_count: int = 0
    helpful_count: int = 0
    not_helpful_count: int = 0
    versions: List[Dict[str, Any]] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime = field(default_factory=datetime.utcnow)
    published_at: Optional[datetime] = None
    
    def __post_init__(self):
        if not self.title:
            raise ValueError("title cannot be empty")
        if not self.slug:
            raise ValueError("slug cannot be empty")
    
    @property
    def is_published(self) -> bool:
        return self.status == ArticleStatus.PUBLISHED
    
    @property
    def is_draft(self) -> bool:
        return self.status == ArticleStatus.DRAFT
    
    @property
    def helpfulness_ratio(self) -> float:
        total = self.helpful_count + self.not_helpful_count
        if total == 0:
            return 0.0
        return self.helpful_count / total
    
    @property
    def reading_time(self) -> int:
        words = len(self.content.split())
        return max(1, words // 200)
    
    def add_version(self, content: str, user_id: str) -> None:
        version = {
            "version_number": len(self.versions) + 1,
            "content": content,
            "modified_by": user_id,
            "modified_at": datetime.utcnow().isoformat()
        }
        self.versions.append(version)
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "title": self.title,
            "slug": self.slug,
            "content": self.content,
            "summary": self.summary,
            "status": self.status.value,
            "visibility": self.visibility.value,
            "category_id": self.category_id,
            "author_id": self.author_id,
            "author_name": self.author_name,
            "tags": self.tags,
            "view_count": self.view_count,
            "helpful_count": self.helpful_count,
            "not_helpful_count": self.not_helpful_count,
            "versions": self.versions,
            "metadata": self.metadata,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
            "published_at": self.published_at.isoformat() if self.published_at else None,
            "is_published": self.is_published,
            "is_draft": self.is_draft,
            "helpfulness_ratio": self.helpfulness_ratio,
            "reading_time": self.reading_time
        }


class ArticleBuilder:
    """Builder for creating Article instances."""
    
    def __init__(self):
        self._id: Optional[str] = None
        self._title: Optional[str] = None
        self._slug: Optional[str] = None
        self._content: str = ""
        self._summary: str = ""
        self._status: ArticleStatus = ArticleStatus.DRAFT
        self._visibility: ArticleVisibility = ArticleVisibility.INTERNAL
        self._category_id: Optional[str] = None
        self._author_id: Optional[str] = None
        self._author_name: str = ""
        self._tags: List[str] = []
        self._view_count: int = 0
        self._helpful_count: int = 0
        self._not_helpful_count: int = 0
        self._versions: List[Dict[str, Any]] = []
        self._metadata: Dict[str, Any] = {}
        self._published_at: Optional[datetime] = None
    
    def with_id(self, article_id: str) -> "ArticleBuilder":
        self._id = article_id
        return self
    
    def with_title(self, title: str) -> "ArticleBuilder":
        self._title = title
        return self
    
    def with_slug(self, slug: str) -> "ArticleBuilder":
        self._slug = slug
        return self
    
    def with_content(self, content: str) -> "ArticleBuilder":
        self._content = content
        return self
    
    def with_summary(self, summary: str) -> "ArticleBuilder":
        self._summary = summary
        return self
    
    def with_status(self, status: ArticleStatus) -> "ArticleBuilder":
        self._status = status
        return self
    
    def with_visibility(self, visibility: ArticleVisibility) -> "ArticleBuilder":
        self._visibility = visibility
        return self
    
    def for_category(self, category_id: str) -> "ArticleBuilder":
        self._category_id = category_id
        return self
    
    def authored_by(self, author_id: str, author_name: str) -> "ArticleBuilder":
        self._author_id = author_id
        self._author_name = author_name
        return self
    
    def with_tags(self, tags: List[str]) -> "ArticleBuilder":
        self._tags = tags
        return self
    
    def with_counts(self, views: int, helpful: int, not_helpful: int) -> "ArticleBuilder":
        self._view_count = views
        self._helpful_count = helpful
        self._not_helpful_count = not_helpful
        return self
    
    def with_metadata(self, metadata: Dict[str, Any]) -> "ArticleBuilder":
        self._metadata = metadata
        return self
    
    def published_at(self, timestamp: datetime) -> "ArticleBuilder":
        self._published_at = timestamp
        return self
    
    def build(self) -> Article:
        if not self._id:
            self._id = str(uuid4())
        if not self._title:
            raise ValueError("title is required")
        if not self._slug:
            self._slug = self._title.lower().replace(" ", "-")
        if not self._category_id:
            raise ValueError("category_id is required")
        if not self._author_id:
            raise ValueError("author_id is required")
        
        return Article(
            id=self._id,
            title=self._title,
            slug=self._slug,
            content=self._content,
            summary=self._summary,
            status=self._status,
            visibility=self._visibility,
            category_id=self._category_id,
            author_id=self._author_id,
            author_name=self._author_name,
            tags=self._tags,
            view_count=self._view_count,
            helpful_count=self._helpful_count,
            not_helpful_count=self._not_helpful_count,
            versions=self._versions,
            metadata=self._metadata,
            published_at=self._published_at
        )


def create_article(
    title: str,
    category_id: str,
    author_id: str,
    author_name: str,
    **kwargs
) -> Article:
    """Factory function to create an article."""
    builder = ArticleBuilder()
    builder.with_title(title)
    builder.for_category(category_id)
    builder.authored_by(author_id, author_name)
    
    if slug := kwargs.get("slug"):
        builder.with_slug(slug)
    if content := kwargs.get("content"):
        builder.with_content(content)
    if summary := kwargs.get("summary"):
        builder.with_summary(summary)
    if status := kwargs.get("status"):
        builder.with_status(status)
    if visibility := kwargs.get("visibility"):
        builder.with_visibility(visibility)
    if tags := kwargs.get("tags"):
        builder.with_tags(tags)
    if metadata := kwargs.get("metadata"):
        builder.with_metadata(metadata)
    if published_at := kwargs.get("published_at"):
        builder.published_at(published_at)
    
    return builder.build()


def create_category(
    name: str,
    description: str,
    slug: str,
    **kwargs
) -> ArticleCategory:
    """Factory function to create an article category."""
    return ArticleCategory(
        id=str(uuid4()),
        name=name,
        description=description,
        slug=slug,
        parent_id=kwargs.get("parent_id"),
        order=kwargs.get("order", 0)
    )
