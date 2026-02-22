"""
API Layer - Auth Controller
FastAPI routes for authentication.

Author: Alexandre Albert Ndour
"""

from fastapi import APIRouter, HTTPException, status, Depends
from pydantic import BaseModel, EmailStr

from ...application.dtos.user_dtos import LoginDTO, LoginResponseDTO, ChangePasswordDTO


router = APIRouter(prefix="/auth", tags=["Authentication"])


class LoginRequest(BaseModel):
    """Login request model."""
    email: EmailStr
    password: str


class LoginResponse(BaseModel):
    """Login response model."""
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    expires_in: int = 3600


class RefreshTokenRequest(BaseModel):
    """Refresh token request model."""
    refresh_token: str


class ChangePasswordRequest(BaseModel):
    """Change password request model."""
    current_password: str
    new_password: str


class MessageResponse(BaseModel):
    """Generic message response."""
    message: str


@router.post(
    "/login",
    response_model=LoginResponse,
    summary="User login",
    description="Authenticate user and get access token"
)
async def login(
    request: LoginRequest,
    use_case=None
):
    """User login endpoint."""
    try:
        dto = LoginDTO(email=request.email, password=request.password)
        result = await use_case.execute(dto)
        
        return LoginResponse(
            access_token=result.access_token,
            refresh_token=result.refresh_token,
            token_type=result.token_type,
            expires_in=result.expires_in
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e),
            headers={"WWW-Authenticate": "Bearer"}
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )


@router.post(
    "/refresh",
    response_model=LoginResponse,
    summary="Refresh access token",
    description="Get new access token using refresh token"
)
async def refresh_token(
    request: RefreshTokenRequest,
    use_case=None
):
    """Refresh access token."""
    try:
        result = await use_case.refresh(request.refresh_token)
        
        return LoginResponse(
            access_token=result.access_token,
            refresh_token=result.refresh_token,
            token_type=result.token_type,
            expires_in=result.expires_in
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )


@router.post(
    "/logout",
    response_model=MessageResponse,
    summary="User logout",
    description="Logout user and invalidate tokens"
)
async def logout(
    current_user=None,
    token_repository=None
):
    """User logout endpoint."""
    try:
        # Invalidate tokens
        if current_user:
            await token_repository.invalidate_user_tokens(current_user.id)
        
        return MessageResponse(message="Successfully logged out")
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )


@router.post(
    "/change-password",
    response_model=MessageResponse,
    summary="Change password",
    description="Change user password"
)
async def change_password(
    request: ChangePasswordRequest,
    use_case=None,
    current_user=None
):
    """Change password endpoint."""
    try:
        if not current_user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Not authenticated"
            )
        
        dto = ChangePasswordDTO(
            current_password=request.current_password,
            new_password=request.new_password
        )
        
        await use_case.execute(current_user.id, dto)
        
        return MessageResponse(message="Password changed successfully")
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )


@router.post(
    "/forgot-password",
    response_model=MessageResponse,
    summary="Request password reset",
    description="Request password reset email"
)
async def forgot_password(
    email: str,
    use_case=None
):
    """Request password reset."""
    try:
        await use_case.request_password_reset(email)
        
        # Always return success to prevent email enumeration
        return MessageResponse(
            message="If the email exists, a reset link has been sent"
        )
    except Exception as e:
        # Don't expose internal errors
        return MessageResponse(
            message="If the email exists, a reset link has been sent"
        )


@router.post(
    "/reset-password",
    response_model=MessageResponse,
    summary="Reset password",
    description="Reset password using token"
)
async def reset_password(
    token: str,
    new_password: str,
    use_case=None
):
    """Reset password with token."""
    try:
        await use_case.reset_password(token, new_password)
        
        return MessageResponse(message="Password reset successfully")
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )


@router.get(
    "/me",
    summary="Get current user",
    description="Get authenticated user information"
)
async def get_current_user(
    current_user=None
):
    """Get current user info."""
    if not current_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated"
        )
    
    return current_user
