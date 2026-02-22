"""
Application Layer - User DTOs
Data Transfer Objects for User operations.

Author: Alexandre Albert Ndour
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional, List
import uuid


@dataclass
class CreateUserDTO:
    """DTO for creating a new user."""
    email: str
    password: str
    first_name: str
    last_name: str
    phone: Optional[str] = None
    role_ids: List[uuid.UUID] = field(default_factory=list)


@dataclass
class UpdateUserDTO:
    """DTO for updating a user."""
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    phone: Optional[str] = None
    avatar_url: Optional[str] = None
    is_active: Optional[bool] = None


@dataclass
class UserResponseDTO:
    """DTO for user response."""
    id: uuid.UUID
    email: str
    first_name: str
    last_name: str
    phone: Optional[str]
    avatar_url: Optional[str]
    is_active: bool
    is_verified: bool
    is_superuser: bool
    last_login_at: Optional[datetime]
    created_at: datetime
    updated_at: datetime
    roles: List[str] = field(default_factory=list)
    permissions: List[str] = field(default_factory=list)


@dataclass
class UserListDTO:
    """DTO for user list response."""
    id: uuid.UUID
    email: str
    first_name: str
    last_name: str
    is_active: bool
    is_verified: bool
    created_at: datetime


@dataclass
class LoginDTO:
    """DTO for login request."""
    email: str
    password: str


@dataclass
class LoginResponseDTO:
    """DTO for login response."""
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    expires_in: int = 3600
    user: UserResponseDTO = None  # type: ignore


@dataclass
class ChangePasswordDTO:
    """DTO for password change."""
    current_password: str
    new_password: str


@dataclass
class ResetPasswordDTO:
    """DTO for password reset."""
    token: str
    new_password: str


@dataclass
class AssignRoleDTO:
    """DTO for assigning a role to a user."""
    role_id: uuid.UUID


@dataclass
class PaginationParams:
    """Pagination parameters."""
    page: int = 1
    limit: int = 20
    sort_by: str = "created_at"
    sort_order: str = "desc"
    
    @property
    def offset(self) -> int:
        return (self.page - 1) * self.limit


@dataclass
class UserFilterDTO:
    """Filter parameters for user list."""
    is_active: Optional[bool] = None
    is_verified: Optional[bool] = None
    search: Optional[str] = None
    role_id: Optional[uuid.UUID] = None
    created_from: Optional[datetime] = None
    created_to: Optional[datetime] = None
