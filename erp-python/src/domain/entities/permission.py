"""
Permission Entity - Domain Layer
Represents a permission in the RBAC system.

Author: Alexandre Albert Ndour
"""

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Optional
import uuid


@dataclass
class Permission:
    """
    Permission Entity.
    
    Represents a granular permission that can be assigned
    to roles or users. Permissions follow a resource.action format.
    """
    
    # Identity
    id: uuid.UUID = field(default_factory=uuid.uuid4)
    name: str = ""
    slug: str = ""
    description: str = ""
    
    # Permission details
    resource: str = ""  # e.g., "users", "products", "orders"
    action: str = ""    # e.g., "read", "write", "delete", "execute"
    
    # Type
    is_crud: bool = False  # CRUD permissions are composable
    is_system: bool = False  # System permissions cannot be deleted
    
    # Metadata
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    
    def __post_init__(self):
        """Validate after initialization."""
        if self.slug == "" and self.name != "":
            self.slug = self.name.lower().replace(" ", "_")
        if self.name == "" and self.resource and self.action:
            self.name = f"{self.resource}.{self.action}"
            self.slug = self.name.lower().replace(" ", "_")
    
    # ==================== Business Methods ====================
    
    def matches(self, resource: str, action: str) -> bool:
        """Check if this permission matches a resource and action."""
        if self.slug == "*" or self.slug == "*.*":
            return True
        if self.resource == "*" and self.action == "*":
            return True
        return self.resource == resource and self.action == action
    
    def is_wildcard(self) -> bool:
        """Check if this is a wildcard permission."""
        return self.slug in ["*", "*.*"] or self.resource == "*"
    
    # ==================== Properties ====================
    
    @property
    def full_name(self) -> str:
        """Get full permission name."""
        return f"{self.resource}:{self.action}"
    
    # ==================== Factory Methods ====================
    
    @classmethod
    def create(
        cls,
        resource: str,
        action: str,
        description: str = ""
    ) -> "Permission":
        """
        Factory method to create a permission.
        
        Args:
            resource: Resource name (e.g., "users", "products")
            action: Action (e.g., "read", "write", "delete")
            description: Permission description
            
        Returns:
            New Permission instance
        """
        return cls(
            name=f"{resource}.{action}",
            slug=f"{resource}_{action}",
            resource=resource,
            action=action,
            description=description,
            is_crud=action in ["create", "read", "update", "delete"],
        )
    
    @classmethod
    def create_crud_permissions(cls, resource: str) -> list["Permission"]:
        """Create CRUD permissions for a resource."""
        return [
            cls.create(resource, "create", f"Create {resource}"),
            cls.create(resource, "read", f"Read {resource}"),
            cls.create(resource, "update", f"Update {resource}"),
            cls.create(resource, "delete", f"Delete {resource}"),
        ]
    
    @classmethod
    def get_all_crud_resources(cls) -> list:
        """Get list of all CRUD resources."""
        return [
            "users", "roles", "permissions",
            "customers", "products", "orders", 
            "invoices", "payments", "reports",
            "settings", "logs"
        ]
    
    # ==================== Default Permissions ====================
    
    @classmethod
    def get_default_permissions(cls) -> list["Permission"]:
        """Get default system permissions."""
        permissions = []
        
        # User management
        permissions.extend(cls.create_crud_permissions("users"))
        
        # Role management
        permissions.extend(cls.create_crud_permissions("roles"))
        
        # Customer management
        permissions.extend(cls.create_crud_permissions("customers"))
        
        # Product management
        permissions.extend(cls.create_crud_permissions("products"))
        
        # Order management
        permissions.extend(cls.create_crud_permissions("orders"))
        
        # Invoice management
        permissions.extend(cls.create_crud_permissions("invoices"))
        
        # Payment management
        permissions.extend(cls.create_crud_permissions("payments"))
        
        # Report management
        permissions.extend(cls.create_crud_permissions("reports"))
        
        # Settings
        permissions.extend(cls.create_crud_permissions("settings"))
        
        # Add wildcard permission
        permissions.append(cls(
            name="*",
            slug="*",
            description="Full access to all resources",
            resource="*",
            action="*",
            is_system=True
        ))
        
        return permissions
    
    # ==================== Serialization ====================
    
    def to_dict(self) -> dict:
        """Convert to dictionary."""
        return {
            "id": str(self.id),
            "name": self.name,
            "slug": self.slug,
            "description": self.description,
            "resource": self.resource,
            "action": self.action,
            "is_crud": self.is_crud,
            "is_system": self.is_system,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
        }
