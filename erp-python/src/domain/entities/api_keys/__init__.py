"""
API Key Entity for ERP System.

This module provides the APIKey entity for managing API keys
following Clean Architecture principles.
"""

from dataclasses import dataclass, field
from datetime import datetime, timedelta
from typing import Optional, Dict, Any, List
from enum import Enum


class APIKeyStatus(str, Enum):
    """API Key status enumeration."""
    ACTIVE = "active"
    INACTIVE = "inactive"
    EXPIRED = "expired"
    REVOKED = "revoked"


class APIKeyScope(str, Enum):
    """API Key scope enumeration."""
    READ = "read"
    WRITE = "write"
    ADMIN = "admin"
    CUSTOM = "custom"


@dataclass(frozen=True)
class APIKey:
    """
    APIKey entity representing an API key for authentication.
    
    This entity follows Clean Architecture principles and is immutable.
    
    Attributes:
        id: Unique identifier for the API key
        key_hash: Hashed version of the API key
        name: API key name
        description: API key description
        status: Current status
        scopes: List of allowed scopes
        user_id: ID of the user who owns this key
        user_email: Email of the user
        expires_at: Expiration timestamp
        last_used_at: Last usage timestamp
        ip_whitelist: List of allowed IP addresses
        rate_limit: Rate limit (requests per minute)
        metadata: Additional metadata
        created_at: Timestamp when created
        updated_at: Timestamp when last updated
    """
    id: str
    key_hash: str
    name: str
    description: str
    status: APIKeyStatus
    scopes: List[APIKeyScope]
    user_id: str
    user_email: str
    expires_at: Optional[datetime] = None
    last_used_at: Optional[datetime] = None
    ip_whitelist: List[str] = field(default_factory=list)
    rate_limit: int = 60
    metadata: Dict[str, Any] = field(default_factory=dict)
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime = field(default_factory=datetime.utcnow)
    
    def __post_init__(self):
        """Validate API key after initialization."""
        if not self.key_hash:
            raise ValueError("key_hash cannot be empty")
        if not self.name:
            raise ValueError("name cannot be empty")
        if not self.user_id:
            raise ValueError("user_id cannot be empty")
        if not self.scopes:
            raise ValueError("scopes cannot be empty")
        if self.rate_limit <= 0:
            raise ValueError("rate_limit must be positive")
    
    @property
    def is_active(self) -> bool:
        """Check if API key is active."""
        return self.status == APIKeyStatus.ACTIVE
    
    @property
    def is_expired(self) -> bool:
        """Check if API key is expired."""
        if not self.expires_at:
            return False
        return datetime.utcnow() > self.expires_at
    
    @property
    def is_revoked(self) -> bool:
        """Check if API key is revoked."""
        return self.status == APIKeyStatus.REVOKED
    
    @property
    def days_until_expiry(self) -> Optional[int]:
        """Get days until expiry."""
        if not self.expires_at:
            return None
        delta = self.expires_at - datetime.utcnow()
        return max(0, delta.days)
    
    @property
    def scope_count(self) -> int:
        """Get number of scopes."""
        return len(self.scopes)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert API key to dictionary."""
        return {
            "id": self.id,
            "key_hash": self.key_hash[:8] + "****",
            "name": self.name,
            "description": self.description,
            "status": self.status.value,
            "scopes": [s.value for s in self.scopes],
            "user_id": self.user_id,
            "user_email": self.user_email,
            "expires_at": self.expires_at.isoformat() if self.expires_at else None,
            "last_used_at": self.last_used_at.isoformat() if self.last_used_at else None,
            "ip_whitelist": self.ip_whitelist,
            "rate_limit": self.rate_limit,
            "metadata": self.metadata,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
            "is_active": self.is_active,
            "is_expired": self.is_expired,
            "is_revoked": self.is_revoked,
            "days_until_expiry": self.days_until_expiry,
            "scope_count": self.scope_count
        }


class APIKeyBuilder:
    """Builder for creating APIKey instances."""
    
    def __init__(self):
        self._id: Optional[str] = None
        self._key_hash: Optional[str] = None
        self._name: Optional[str] = None
        self._description: str = ""
        self._status: APIKeyStatus = APIKeyStatus.ACTIVE
        self._scopes: List[APIKeyScope] = []
        self._user_id: Optional[str] = None
        self._user_email: Optional[str] = None
        self._expires_at: Optional[datetime] = None
        self._ip_whitelist: List[str] = []
        self._rate_limit: int = 60
        self._metadata: Dict[str, Any] = {}
    
    def with_id(self, api_key_id: str) -> "APIKeyBuilder":
        self._id = api_key_id
        return self
    
    def with_key_hash(self, key_hash: str) -> "APIKeyBuilder":
        self._key_hash = key_hash
        return self
    
    def with_name(self, name: str) -> "APIKeyBuilder":
        self._name = name
        return self
    
    def with_description(self, description: str) -> "APIKeyBuilder":
        self._description = description
        return self
    
    def with_status(self, status: APIKeyStatus) -> "APIKeyBuilder":
        self._status = status
        return self
    
    def with_scopes(self, scopes: List[APIKeyScope]) -> "APIKeyBuilder":
        self._scopes = scopes
        return self
    
    def for_user(self, user_id: str, user_email: str) -> "APIKeyBuilder":
        self._user_id = user_id
        self._user_email = user_email
        return self
    
    def expires_in_days(self, days: int) -> "APIKeyBuilder":
        self._expires_at = datetime.utcnow() + timedelta(days=days)
        return self
    
    def with_expiry(self, expires_at: datetime) -> "APIKeyBuilder":
        self._expires_at = expires_at
        return self
    
    def with_ip_whitelist(self, ips: List[str]) -> "APIKeyBuilder":
        self._ip_whitelist = ips
        return self
    
    def with_rate_limit(self, rate_limit: int) -> "APIKeyBuilder":
        self._rate_limit = rate_limit
        return self
    
    def with_metadata(self, metadata: Dict[str, Any]) -> "APIKeyBuilder":
        self._metadata = metadata
        return self
    
    def build(self) -> APIKey:
        from uuid import uuid4
        
        if not self._id:
            self._id = str(uuid4())
        if not self._key_hash:
            raise ValueError("key_hash is required")
        if not self._name:
            raise ValueError("name is required")
        if not self._user_id:
            raise ValueError("user_id is required")
        if not self._scopes:
            raise ValueError("scopes is required")
        
        return APIKey(
            id=self._id,
            key_hash=self._key_hash,
            name=self._name,
            description=self._description,
            status=self._status,
            scopes=self._scopes,
            user_id=self._user_id,
            user_email=self._user_email or "",
            expires_at=self._expires_at,
            ip_whitelist=self._ip_whitelist,
            rate_limit=self._rate_limit,
            metadata=self._metadata
        )


# Factory function
def create_api_key(
    key_hash: str,
    name: str,
    user_id: str,
    scopes: List[APIKeyScope],
    **kwargs
) -> APIKey:
    """Factory function to create an API key."""
    builder = APIKeyBuilder()
    builder.with_key_hash(key_hash)
    builder.with_name(name)
    builder.for_user(user_id, kwargs.get("user_email", ""))
    builder.with_scopes(scopes)
    
    if description := kwargs.get("description"):
        builder.with_description(description)
    if status := kwargs.get("status"):
        builder.with_status(status)
    if expires_in_days := kwargs.get("expires_in_days"):
        builder.expires_in_days(expires_in_days)
    if expires_at := kwargs.get("expires_at"):
        builder.with_expiry(expires_at)
    if ip_whitelist := kwargs.get("ip_whitelist"):
        builder.with_ip_whitelist(ip_whitelist)
    if rate_limit := kwargs.get("rate_limit"):
        builder.with_rate_limit(rate_limit)
    if metadata := kwargs.get("metadata"):
        builder.with_metadata(metadata)
    
    return builder.build()
