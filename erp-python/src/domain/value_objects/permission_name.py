"""
PermissionName Value Object - Domain Layer
Represents a validated permission name.

Author: Alexandre Albert Ndour
"""

import re
from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class PermissionName:
    """
    PermissionName Value Object.
    
    Immutable value object that represents and validates
    a permission name in the format resource.action.
    """
    
    value: str
    
    # Permission pattern: resource.action or *
    PERMISSION_PATTERN = re.compile(r'^[a-z][a-z0-9_]*(\.[a-z][a-z0-9_]*)?$|^(\*)$')
    
    def __post_init__(self):
        """Validate permission name after initialization."""
        if not self.value:
            raise ValueError("Permission name cannot be empty")
        
        if not self.PERMISSION_PATTERN.match(self.value):
            raise ValueError(
                f"Invalid permission format: {self.value}. "
                "Expected format: resource.action (e.g., users.read)"
            )
        
        # Normalize to lowercase
        object.__setattr__(self, 'value', self.value.lower())
    
    def __str__(self) -> str:
        return self.value
    
    def __repr__(self) -> str:
        return f"PermissionName('{self.value}')"
    
    def __eq__(self, other) -> bool:
        if isinstance(other, PermissionName):
            return self.value == other.value
        if isinstance(other, str):
            return self.value == other.lower()
        return False
    
    def __hash__(self) -> int:
        return hash(self.value)
    
    def get_resource(self) -> Optional[str]:
        """Get the resource part of the permission."""
        if self.value == "*":
            return "*"
        parts = self.value.split(".")
        return parts[0] if parts else None
    
    def get_action(self) -> Optional[str]:
        """Get the action part of the permission."""
        if self.value == "*":
            return "*"
        parts = self.value.split(".")
        return parts[1] if len(parts) > 1 else None
    
    def is_wildcard(self) -> bool:
        """Check if this is a wildcard permission."""
        return self.value in ["*", "*.*"]
    
    def is_resource_wildcard(self) -> bool:
        """Check if this is a resource wildcard (e.g., users.*)."""
        return self.value.endswith(".*")
    
    @classmethod
    def is_valid(cls, permission: str) -> bool:
        """Check if a permission string is valid."""
        if not permission:
            return False
        return bool(cls.PERMISSION_PATTERN.match(permission.lower().strip()))
    
    @classmethod
    def create(cls, value: str) -> "PermissionName":
        """Factory function to create a PermissionName value object."""
        return cls(value=value)


# Convenience function
def create_permission(value: str) -> PermissionName:
    """Factory function to create a PermissionName value object."""
    return PermissionName(value=value)
