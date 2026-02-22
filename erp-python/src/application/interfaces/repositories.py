"""
Application Layer - Repository Interfaces
Contracts for data persistence.

Author: Alexandre Albert Ndour
"""

from abc import ABC, abstractmethod
from typing import Optional, List
import uuid


class UserRepositoryInterface(ABC):
    """Repository interface for User entity."""
    
    @abstractmethod
    async def create(self, user) -> "user":
        """Create a new user."""
        pass
    
    @abstractmethod
    async def get_by_id(self, user_id: uuid.UUID) -> Optional["user"]:
        """Get user by ID."""
        pass
    
    @abstractmethod
    async def get_by_email(self, email: str) -> Optional["user"]:
        """Get user by email."""
        pass
    
    @abstractmethod
    async def update(self, user) -> "user":
        """Update a user."""
        pass
    
    @abstractmethod
    async def delete(self, user_id: uuid.UUID) -> bool:
        """Delete a user."""
        pass
    
    @abstractmethod
    async def list(
        self,
        filters: dict = None,
        page: int = 1,
        limit: int = 20
    ) -> tuple[List["user"], int]:
        """List users with pagination."""
        pass
    
    @abstractmethod
    async def exists(self, email: str) -> bool:
        """Check if user exists by email."""
        pass


class RoleRepositoryInterface(ABC):
    """Repository interface for Role entity."""
    
    @abstractmethod
    async def create(self, role) -> "role":
        """Create a new role."""
        pass
    
    @abstractmethod
    async def get_by_id(self, role_id: uuid.UUID) -> Optional["role"]:
        """Get role by ID."""
        pass
    
    @abstractmethod
    async def get_by_slug(self, slug: str) -> Optional["role"]:
        """Get role by slug."""
        pass
    
    @abstractmethod
    async def update(self, role) -> "role":
        """Update a role."""
        pass
    
    @abstractmethod
    async def delete(self, role_id: uuid.UUID) -> bool:
        """Delete a role."""
        pass
    
    @abstractmethod
    async def list(
        self,
        filters: dict = None,
        page: int = 1,
        limit: int = 20
    ) -> tuple[List["role"], int]:
        """List roles with pagination."""
        pass
    
    @abstractmethod
    async def get_default_role(self) -> Optional["role"]:
        """Get the default role for new users."""
        pass


class PermissionRepositoryInterface(ABC):
    """Repository interface for Permission entity."""
    
    @abstractmethod
    async def create(self, permission) -> "permission":
        """Create a new permission."""
        pass
    
    @abstractmethod
    async def get_by_id(self, permission_id: uuid.UUID) -> Optional["permission"]:
        """Get permission by ID."""
        pass
    
    @abstractmethod
    async def get_by_slug(self, slug: str) -> Optional["permission"]:
        """Get permission by slug."""
        pass
    
    @abstractmethod
    async def list(
        self,
        filters: dict = None,
        page: int = 1,
        limit: int = 20
    ) -> tuple[List["permission"], int]:
        """List permissions with pagination."""
        pass
    
    @abstractmethod
    async def get_all(self) -> List["permission"]:
        """Get all permissions."""
        pass


class UserRoleRepositoryInterface(ABC):
    """Repository interface for UserRole association."""
    
    @abstractmethod
    async def assign_role(
        self,
        user_id: uuid.UUID,
        role_id: uuid.UUID,
        assigned_by: uuid.UUID = None
    ) -> "user_role":
        """Assign a role to a user."""
        pass
    
    @abstractmethod
    async def revoke_role(
        self,
        user_id: uuid.UUID,
        role_id: uuid.UUID
    ) -> bool:
        """Revoke a role from a user."""
        pass
    
    @abstractmethod
    async def get_user_roles(self, user_id: uuid.UUID) -> List["role"]:
        """Get all roles for a user."""
        pass
    
    @abstractmethod
    async def get_role_users(self, role_id: uuid.UUID) -> List["user"]:
        """Get all users with a specific role."""
        pass
    
    @abstractmethod
    async def has_role(self, user_id: uuid.UUID, role_id: uuid.UUID) -> bool:
        """Check if user has a specific role."""
        pass
