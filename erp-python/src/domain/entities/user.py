"""
User Entity - Domain Layer
Represents a user in the ERP system with authentication and authorization capabilities.

Author: Alexandre Albert Ndour
"""

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Optional, List
import uuid

from .value_objects.email import Email
from .value_objects.password import Password


@dataclass
class User:
    """
    User Aggregate Root Entity.
    
    Represents a system user with authentication credentials,
    profile information, and role assignments.
    """
    
    # Identity
    id: uuid.UUID = field(default_factory=uuid.uuid4)
    email: Email = None  # type: ignore
    password_hash: str = ""
    
    # Profile
    first_name: str = ""
    last_name: str = ""
    phone: Optional[str] = None
    avatar_url: Optional[str] = None
    
    # Status
    is_active: bool = True
    is_verified: bool = False
    is_superuser: bool = False
    
    # Security
    failed_login_attempts: int = 0
    locked_until: Optional[datetime] = None
    password_changed_at: Optional[datetime] = None
    last_login_at: Optional[datetime] = None
    
    # Metadata
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    created_by: Optional[uuid.UUID] = None
    updated_by: Optional[uuid.UUID] = None
    
    # Relationships (loaded separately)
    _roles: List[uuid.UUID] = field(default_factory=list, repr=False)
    _permissions: List[str] = field(default_factory=list, repr=False)
    
    def __post_init__(self):
        """Validate after initialization."""
        if self.email and not isinstance(self.email, Email):
            self.email = Email(self.email)
    
    # ==================== Business Methods ====================
    
    def activate(self) -> None:
        """Activate the user account."""
        self.is_active = True
        self.updated_at = datetime.now(timezone.utc)
    
    def deactivate(self) -> None:
        """Deactivate the user account."""
        self.is_active = False
        self.updated_at = datetime.now(timezone.utc)
    
    def verify(self) -> None:
        """Mark user as verified."""
        self.is_verified = True
        self.updated_at = datetime.now(timezone.utc)
    
    def lock(self, duration_minutes: int = 30) -> None:
        """Lock the user account temporarily."""
        from datetime import timedelta
        self.locked_until = datetime.now(timezone.utc) + timedelta(minutes=duration_minutes)
        self.failed_login_attempts = 0
        self.updated_at = datetime.now(timezone.utc)
    
    def unlock(self) -> None:
        """Unlock the user account."""
        self.locked_until = None
        self.failed_login_attempts = 0
        self.updated_at = datetime.now(timezone.utc)
    
    def record_failed_login(self, max_attempts: int = 5) -> bool:
        """
        Record a failed login attempt.
        Returns True if account should be locked.
        """
        self.failed_login_attempts += 1
        if self.failed_login_attempts >= max_attempts:
            self.lock()
            return True
        return False
    
    def record_successful_login(self) -> None:
        """Record a successful login."""
        self.last_login_at = datetime.now(timezone.utc)
        self.failed_login_attempts = 0
        self.updated_at = datetime.now(timezone.utc)
    
    def update_password(self, new_password_hash: str) -> None:
        """Update the user's password."""
        self.password_hash = new_password_hash
        self.password_changed_at = datetime.now(timezone.utc)
        self.updated_at = datetime.now(timezone.utc)
    
    def update_profile(self, first_name: str = None, last_name: str = None, phone: str = None) -> None:
        """Update user profile information."""
        if first_name is not None:
            self.first_name = first_name
        if last_name is not None:
            self.last_name = last_name
        if phone is not None:
            self.phone = phone
        self.updated_at = datetime.now(timezone.utc)
    
    def has_role(self, role_id: uuid.UUID) -> bool:
        """Check if user has a specific role."""
        return role_id in self._roles
    
    def has_permission(self, permission: str) -> bool:
        """
        Check if user has a specific permission.
        Superusers have all permissions.
        """
        if self.is_superuser:
            return True
        return permission in self._permissions
    
    def add_role(self, role_id: uuid.UUID) -> None:
        """Assign a role to the user."""
        if role_id not in self._roles:
            self._roles.append(role_id)
            self.updated_at = datetime.now(timezone.utc)
    
    def remove_role(self, role_id: uuid.UUID) -> None:
        """Remove a role from the user."""
        if role_id in self._roles:
            self._roles.remove(role_id)
            self.updated_at = datetime.now(timezone.utc)
    
    def set_permissions(self, permissions: List[str]) -> None:
        """Set direct permissions for the user."""
        self._permissions = permissions
        self.updated_at = datetime.now(timezone.utc)
    
    # ==================== Read-Only Properties ====================
    
    @property
    def full_name(self) -> str:
        """Get user's full name."""
        return f"{self.first_name} {self.last_name}".strip()
    
    @property
    def initials(self) -> str:
        """Get user's initials."""
        first = self.first_name[0].upper() if self.first_name else ""
        last = self.last_name[0].upper() if self.last_name else ""
        return f"{first}{last}"
    
    @property
    def roles(self) -> List[uuid.UUID]:
        """Get user's role IDs."""
        return self._roles.copy()
    
    @property
    def permissions(self) -> List[str]:
        """Get user's permissions."""
        return self._permissions.copy()
    
    @property
    def is_locked(self) -> bool:
        """Check if account is currently locked."""
        if self.locked_until is None:
            return False
        return datetime.now(timezone.utc) < self.locked_until
    
    @property
    def can_login(self) -> bool:
        """Check if user can attempt login."""
        return self.is_active and not self.is_locked
    
    # ==================== Factory Methods ====================
    
    @classmethod
    def create(
        cls,
        email: str,
        password_hash: str,
        first_name: str,
        last_name: str,
        phone: str = None,
        created_by: uuid.UUID = None
    ) -> "User":
        """
        Factory method to create a new user.
        
        Args:
            email: User's email address
            password_hash: Hashed password
            first_name: User's first name
            last_name: User's last name
            phone: Optional phone number
            created_by: ID of user creating this account
            
        Returns:
            New User instance
        """
        user = cls(
            email=Email(email),
            password_hash=password_hash,
            first_name=first_name,
            last_name=last_name,
            phone=phone,
            created_by=created_by,
            is_active=True,
            is_verified=False,
        )
        return user
    
    @classmethod
    def create_superuser(
        cls,
        email: str,
        password_hash: str,
        first_name: str = "Admin",
        last_name: str = "User"
    ) -> "User":
        """Factory method to create a superuser."""
        user = cls.create(
            email=email,
            password_hash=password_hash,
            first_name=first_name,
            last_name=last_name
        )
        user.is_superuser = True
        user.is_verified = True
        return user
    
    # ==================== Serialization ====================
    
    def to_dict(self) -> dict:
        """Convert to dictionary (excluding sensitive data)."""
        return {
            "id": str(self.id),
            "email": str(self.email),
            "first_name": self.first_name,
            "last_name": self.last_name,
            "phone": self.phone,
            "avatar_url": self.avatar_url,
            "is_active": self.is_active,
            "is_verified": self.is_verified,
            "is_superuser": self.is_superuser,
            "last_login_at": self.last_login_at.isoformat() if self.last_login_at else None,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
        }
    
    def to_full_dict(self) -> dict:
        """Convert to dictionary including all data."""
        data = self.to_dict()
        data.update({
            "failed_login_attempts": self.failed_login_attempts,
            "locked_until": self.locked_until.isoformat() if self.locked_until else None,
            "password_changed_at": self.password_changed_at.isoformat() if self.password_changed_at else None,
            "roles": [str(r) for r in self._roles],
            "permissions": self._permissions,
        })
        return data
