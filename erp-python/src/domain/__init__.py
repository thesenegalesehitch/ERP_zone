"""
ERP Library - Python (FastAPI) Implementation
Module: Users Management with RBAC

Author: Alexandre Albert Ndour
"""

# Domain Layer - Entities
from .entities.user import User
from .entities.role import Role
from .entities.permission import Permission
from .entities.user_role import UserRole

# Domain Layer - Value Objects
from .value_objects.email import Email
from .value_objects.password import Password
from .value_objects.permission_name import PermissionName

# Domain Layer - Events
from .events.user_events import UserCreatedEvent, UserUpdatedEvent, UserDeletedEvent
from .events.role_events import RoleAssignedEvent, RoleRevokedEvent

# Domain Layer - Services
from .services.user_service import UserDomainService
from .services.permission_service import PermissionDomainService

__all__ = [
    # Entities
    "User",
    "Role", 
    "Permission",
    "UserRole",
    # Value Objects
    "Email",
    "Password",
    "PermissionName",
    # Events
    "UserCreatedEvent",
    "UserUpdatedEvent",
    "UserDeletedEvent",
    "RoleAssignedEvent",
    "RoleRevokedEvent",
    # Services
    "UserDomainService",
    "PermissionDomainService",
]
