"""
API Layer - User Controller
FastAPI routes for user management.

Author: Alexandre Albert Ndour
"""

from fastapi import APIRouter, Depends, HTTPException, status, Query
from typing import Optional, List
import uuid

from ...application.dtos.user_dtos import (
    CreateUserDTO,
    UpdateUserDTO,
    UserResponseDTO,
    UserListDTO,
    LoginDTO,
    LoginResponseDTO,
    ChangePasswordDTO,
    AssignRoleDTO,
    PaginationParams,
    UserFilterDTO,
)


router = APIRouter(prefix="/users", tags=["Users"])


@router.post(
    "/",
    response_model=UserResponseDTO,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new user",
    description="Create a new user with optional role assignments"
)
async def create_user(
    dto: CreateUserDTO,
    # These would be injected via dependency
    use_case=None,
    current_user=None
):
    """Create a new user."""
    try:
        # Check permissions (would use dependency)
        # if not current_user.has_permission("users.create"):
        #     raise HTTPException(status_code=403, detail="Insufficient permissions")
        
        result = await use_case.execute(dto, created_by=getattr(current_user, 'id', None))
        return result
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get(
    "/{user_id}",
    response_model=UserResponseDTO,
    summary="Get user by ID",
    description="Retrieve a user by their unique identifier"
)
async def get_user(
    user_id: uuid.UUID,
    use_case=None,
    current_user=None
):
    """Get user by ID."""
    try:
        result = await use_case.execute(user_id)
        return result
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get(
    "/",
    response_model=List[UserListDTO],
    summary="List users",
    description="List users with pagination and filters"
)
async def list_users(
    page: int = Query(1, ge=1, description="Page number"),
    limit: int = Query(20, ge=1, le=100, description="Items per page"),
    is_active: Optional[bool] = Query(None, description="Filter by active status"),
    is_verified: Optional[bool] = Query(None, description="Filter by verified status"),
    search: Optional[str] = Query(None, description="Search in name/email"),
    use_case=None,
    current_user=None
):
    """List users with pagination."""
    try:
        filters = UserFilterDTO(
            is_active=is_active,
            is_verified=is_verified,
            search=search
        )
        pagination = PaginationParams(page=page, limit=limit)
        
        users, total = await use_case.execute(filters, pagination)
        
        # Add pagination headers
        return users
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")


@router.put(
    "/{user_id}",
    response_model=UserResponseDTO,
    summary="Update user",
    description="Update user information"
)
async def update_user(
    user_id: uuid.UUID,
    dto: UpdateUserDTO,
    use_case=None,
    current_user=None
):
    """Update user information."""
    try:
        result = await use_case.execute(user_id, dto, updated_by=getattr(current_user, 'id', None))
        return result
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")


@router.delete(
    "/{user_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete user",
    description="Delete a user (soft delete)"
)
async def delete_user(
    user_id: uuid.UUID,
    use_case=None,
    current_user=None
):
    """Delete a user."""
    try:
        await use_case.execute(user_id, deleted_by=getattr(current_user, 'id', None))
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")


@router.post(
    "/{user_id}/roles",
    response_model=UserResponseDTO,
    summary="Assign role to user",
    description="Assign a role to a user"
)
async def assign_role(
    user_id: uuid.UUID,
    dto: AssignRoleDTO,
    use_case=None,
    current_user=None
):
    """Assign role to user."""
    try:
        result = await use_case.execute(user_id, dto, assigned_by=getattr(current_user, 'id', None))
        return result
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")


@router.delete(
    "/{user_id}/roles/{role_id}",
    response_model=UserResponseDTO,
    summary="Revoke role from user",
    description="Revoke a role from a user"
)
async def revoke_role(
    user_id: uuid.UUID,
    role_id: uuid.UUID,
    use_case=None,
    current_user=None
):
    """Revoke role from user."""
    try:
        # Would have a separate use case for this
        pass
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")


@router.post(
    "/{user_id}/activate",
    response_model=UserResponseDTO,
    summary="Activate user",
    description="Activate a user account"
)
async def activate_user(
    user_id: uuid.UUID,
    use_case=None,
    current_user=None
):
    """Activate a user."""
    try:
        dto = UpdateUserDTO(is_active=True)
        result = await use_case.execute(user_id, dto, updated_by=getattr(current_user, 'id', None))
        return result
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")


@router.post(
    "/{user_id}/deactivate",
    response_model=UserResponseDTO,
    summary="Deactivate user",
    description="Deactivate a user account"
)
async def deactivate_user(
    user_id: uuid.UUID,
    use_case=None,
    current_user=None
):
    """Deactivate a user."""
    try:
        dto = UpdateUserDTO(is_active=False)
        result = await use_case.execute(user_id, dto, updated_by=getattr(current_user, 'id', None))
        return result
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")
