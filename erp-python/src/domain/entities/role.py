"""
Role Entity - Domain Layer
Represents a role in the RBAC system.

Author: Alexandre Albert Ndour
"""

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Optional, List
import uuid


@dataclass
class Role:
    """
    Role Entity.
    
    Represents a role that can be assigned to users.
    Roles contain permissions that determine what actions
    a user can perform.
    """
    
    # Identity
    id: uuid.UUID = field(default_factory=uuid.uuid4)
    name: str = ""
    slug: str = ""
    description: str = ""
    
    # Type
    is_system: bool = False  # System roles cannot be deleted
    is_default: bool = False  # Default role for new users
    
    # Hierarchy
    level: int = 0  # Higher level = more privileges
    parent_id: Optional[uuid.UUID] = None  # Role hierarchy
    
    # Status
    is_active: bool = True
    
    # Metadata
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    created_by: Optional[uuid.UUID] = None
    
    # Relationships
    _permissions: List[str] = field(default_factory=list, repr=False)
    
    def __post_init__(self):
        """Validate after initialization."""
        if self.slug == "" and self.name != "":
            self.slug = self.name.lower().replace(" ", "_")
    
    # ==================== Business Methods ====================
    
    def add_permission(self, permission: str) -> None:
        """Add a permission to this role."""
        if permission not in self._permissions:
            self._permissions.append(permission)
            self.updated_at = datetime.now(timezone.utc)
    
    def remove_permission(self, permission: str) -> None:
        """Remove a permission from this role."""
        if permission in self._permissions:
            self._permissions.remove(permission)
            self.updated_at = datetime.now(timezone.utc)
    
    def set_permissions(self, permissions: List[str]) -> None:
        """Set all permissions for this role."""
        self._permissions = permissions
        self.updated_at = datetime.now(timezone.utc)
    
    def has_permission(self, permission: str) -> bool:
        """Check if role has a specific permission."""
        return permission in self._permissions
    
    def deactivate(self) -> None:
        """Deactivate this role."""
        self.is_active = False
        self.updated_at = datetime.now(timezone.utc)
    
    def activate(self) -> None:
        """Activate this role."""
        self.is_active = True
        self.updated_at = datetime.now(timezone.utc)
    
    def can_grant_to(self, other: "Role") -> bool:
        """Check if this role can grant another role."""
        return self.level > other.level
    
    # ==================== Properties ====================
    
    @property
    def permissions(self) -> List[str]:
        """Get role permissions."""
        return self._permissions.copy()
    
    @property
    def permission_count(self) -> int:
        """Get number of permissions."""
        return len(self._permissions)
    
    # ==================== Factory Methods ====================
    
    @classmethod
    def create(
        cls,
        name: str,
        description: str = "",
        permissions: List[str] = None,
        level: int = 0,
        created_by: uuid.UUID = None
    ) -> "Role":
        """
        Factory method to create a new role.
        
        Args:
            name: Role name
            description: Role description
            permissions: List of permission strings
            level: Hierarchy level
            created_by: ID of user creating this role
            
        Returns:
            New Role instance
        """
        role = cls(
            name=name,
            slug=name.lower().replace(" ", "_"),
            description=description,
            level=level,
            created_by=created_by,
            is_system=False,
            is_default=False,
        )
        if permissions:
            role._permissions = permissions
        return role
    
    @classmethod
    def create_system_role(
        cls,
        name: str,
        description: str,
        permissions: List[str],
        level: int = 10
    ) -> "Role":
        """Factory method to create a system role."""
        role = cls.create(
            name=name,
            description=description,
            permissions=permissions,
            level=level
        )
        role.is_system = True
        return role
    
    # ==================== Default Roles ====================
    
    @classmethod
    def get_default_roles(cls) -> List["Role"]:
        """Get default system roles."""
        return [
            cls.create_system_role(
                name="Super Admin",
                description="Full system access",
                permissions=["*"],
                level=100
            ),
            cls.create_system_role(
                name="Admin",
                description="Administrative access",
                permissions=[
                    "users.read", "users.write", "users.delete",
                    "roles.read", "roles.write",
                    "products.read", "products.write", "products.delete",
                    "orders.read", "orders.write",
                    "invoices.read", "invoices.write",
                    "reports.read", "reports.export"
                ],
                level=50
            ),
            cls.create_system_role(
                name="Manager",
                description="Management access",
                permissions=[
                    "products.read", "products.write",
                    "orders.read", "orders.write",
                    "invoices.read", "invoices.write",
                    "reports.read"
                ],
                level=30
            ),
            cls.create_system_role(
                name="Employee",
                description="Basic employee access",
                permissions=[
                    "products.read",
                    "orders.read", "orders.write",
                    "invoices.read"
                ],
                level=10,
            ),
            cls.create_system_role(
                name="Customer",
                description="Customer access",
                permissions=[
                    "orders.read", "orders.create",
                    "invoices.read",
                    "profile.read", "profile.update"
                ],
                level=1
            ),
        ]
    
    # ==================== Serialization ====================
    
    def to_dict(self) -> dict:
        """Convert to dictionary."""
        return {
            "id": str(self.id),
            "name": self.name,
            "slug": self.slug,
            "description": self.description,
            "is_system": self.is_system,
            "is_default": self.is_default,
            "level": self.level,
            "parent_id": str(self.parent_id) if self.parent_id else None,
            "is_active": self.is_active,
            "permissions": self._permissions,
            "permission_count": len(self._permissions),
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
        }
