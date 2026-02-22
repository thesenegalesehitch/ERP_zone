"""
Infrastructure Layer - JWT Token Generator
JWT token generation and validation.

Author: Alexandre Albert Ndour
"""

from abc import ABC, abstractmethod
from datetime import datetime, timedelta, timezone
from typing import Optional, Dict, Any
import uuid
import jwt


class TokenGeneratorInterface(ABC):
    """Interface for token generation."""
    
    @abstractmethod
    async def generate_access_token(self, user) -> str:
        """Generate access token."""
        pass
    
    @abstractmethod
    async def generate_refresh_token(self, user) -> str:
        """Generate refresh token."""
        pass
    
    @abstractmethod
    async def verify_token(self, token: str) -> Dict[str, Any]:
        """Verify and decode token."""
        pass
    
    @abstractmethod
    async def decode_token(self, token: str) -> Optional[Dict[str, Any]]:
        """Decode token without verification."""
        pass


class JWTTokenGenerator(TokenGeneratorInterface):
    """JWT token generator implementation."""
    
    def __init__(
        self,
        secret_key: str,
        algorithm: str = "HS256",
        access_token_expire_minutes: int = 60,
        refresh_token_expire_days: int = 7
    ):
        self.secret_key = secret_key
        self.algorithm = algorithm
        self.access_token_expire_minutes = access_token_expire_minutes
        self.refresh_token_expire_days = refresh_token_expire_days
    
    async def generate_access_token(self, user) -> str:
        """Generate JWT access token."""
        now = datetime.now(timezone.utc)
        expire = now + timedelta(minutes=self.access_token_expire_minutes)
        
        payload = {
            "sub": str(user.id),
            "email": str(user.email),
            "iat": now,
            "exp": expire,
            "type": "access",
            "roles": [str(r) for r in user.roles] if hasattr(user, 'roles') else [],
            "permissions": user.permissions if hasattr(user, 'permissions') else [],
            "is_superuser": user.is_superuser if hasattr(user, 'is_superuser') else False
        }
        
        return jwt.encode(payload, self.secret_key, algorithm=self.algorithm)
    
    async def generate_refresh_token(self, user) -> str:
        """Generate JWT refresh token."""
        now = datetime.now(timezone.utc)
        expire = now + timedelta(days=self.refresh_token_expire_days)
        
        payload = {
            "sub": str(user.id),
            "iat": now,
            "exp": expire,
            "type": "refresh",
            "jti": str(uuid.uuid4())  # Unique token ID for revocation
        }
        
        return jwt.encode(payload, self.secret_key, algorithm=self.algorithm)
    
    async def verify_token(self, token: str) -> Dict[str, Any]:
        """Verify and decode JWT token."""
        try:
            payload = jwt.decode(
                token,
                self.secret_key,
                algorithms=[self.algorithm]
            )
            return payload
        except jwt.ExpiredSignatureError:
            raise ValueError("Token has expired")
        except jwt.InvalidTokenError as e:
            raise ValueError(f"Invalid token: {str(e)}")
    
    async def decode_token(self, token: str) -> Optional[Dict[str, Any]]:
        """Decode token without verification."""
        try:
            return jwt.decode(
                token,
                options={"verify_signature": False}
            )
        except Exception:
            return None
    
    async def get_token_expiration(self, token: str) -> Optional[datetime]:
        """Get token expiration time."""
        payload = await self.decode_token(token)
        if payload and "exp" in payload:
            return datetime.fromtimestamp(payload["exp"], tz=timezone.utc)
        return None
    
    async def is_token_expired(self, token: str) -> bool:
        """Check if token is expired."""
        expiration = await self.get_token_expiration(token)
        if expiration:
            return datetime.now(timezone.utc) > expiration
        return True
    
    async def get_token_type(self, token: str) -> Optional[str]:
        """Get token type (access/refresh)."""
        payload = await self.decode_token(token)
        return payload.get("type") if payload else None


class TokenResponse:
    """Token response data class."""
    
    def __init__(
        self,
        access_token: str,
        refresh_token: str,
        token_type: str = "bearer",
        expires_in: int = 3600
    ):
        self.access_token = access_token
        self.refresh_token = refresh_token
        self.token_type = token_type
        self.expires_in = expires_in
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "access_token": self.access_token,
            "refresh_token": self.refresh_token,
            "token_type": self.token_type,
            "expires_in": self.expires_in
        }
