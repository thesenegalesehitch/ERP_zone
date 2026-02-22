"""
Password Value Object - Domain Layer
Represents a validated password with strength requirements.

Author: Alexandre Albert Ndour
"""

import re
from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class Password:
    """
    Password Value Object.
    
    Immutable value object that validates password strength
    and provides secure comparison.
    """
    
    # Store hash, not plain password
    hash: str
    
    # Minimum requirements
    MIN_LENGTH: int = 8
    REQUIRE_UPPERCASE: bool = True
    REQUIRE_LOWERCASE: bool = True
    REQUIRE_DIGIT: bool = True
    REQUIRE_SPECIAL: bool = False
    
    # Validation patterns
    UPPERCASE_PATTERN = re.compile(r'[A-Z]')
    LOWERCASE_PATTERN = re.compile(r'[a-z]')
    DIGIT_PATTERN = re.compile(r'\d')
    SPECIAL_PATTERN = re.compile(r'[!@#$%^&*(),.?":{}|<>]')
    
    def __post_init__(self):
        """Validate password after initialization."""
        if not self.hash:
            raise ValueError("Password hash cannot be empty")
    
    @classmethod
    def create(cls, plain_password: str) -> "Password":
        """
        Factory method to create a password from plain text.
        
        Note: This should be used with proper hashing in infrastructure layer.
        The plain password is only used for validation, then hashed.
        """
        cls.validate_strength(plain_password)
        # Return a password with hash (in production, hash here or in infrastructure)
        return cls(hash=plain_password)
    
    @classmethod
    def create_from_hash(cls, hash: str) -> "Password":
        """Create password from existing hash."""
        return cls(hash=hash)
    
    @classmethod
    def validate_strength(cls, password: str) -> list[str]:
        """
        Validate password strength.
        
        Returns:
            List of validation errors (empty if valid)
        """
        errors = []
        
        if not password:
            errors.append("Password cannot be empty")
            return errors
        
        if len(password) < cls.MIN_LENGTH:
            errors.append(f"Password must be at least {cls.MIN_LENGTH} characters")
        
        if cls.REQUIRE_UPPERCASE and not cls.UPPERCASE_PATTERN.search(password):
            errors.append("Password must contain at least one uppercase letter")
        
        if cls.REQUIRE_LOWERCASE and not cls.LOWERCASE_PATTERN.search(password):
            errors.append("Password must contain at least one lowercase letter")
        
        if cls.REQUIRE_DIGIT and not cls.DIGIT_PATTERN.search(password):
            errors.append("Password must contain at least one digit")
        
        if cls.REQUIRE_SPECIAL and not cls.SPECIAL_PATTERN.search(password):
            errors.append("Password must contain at least one special character")
        
        return errors
    
    @classmethod
    def is_strong(cls, password: str) -> bool:
        """Check if password meets strength requirements."""
        return len(cls.validate_strength(password)) == 0
    
    @classmethod
    def calculate_strength(cls, password: str) -> int:
        """
        Calculate password strength score (0-100).
        
        0-25: Weak
        26-50: Fair
        51-75: Good
        76-100: Strong
        """
        if not password:
            return 0
        
        score = 0
        
        # Length score (up to 30 points)
        score += min(len(password) * 2, 30)
        
        # Character variety (up to 40 points)
        if cls.UPPERCASE_PATTERN.search(password):
            score += 10
        if cls.LOWERCASE_PATTERN.search(password):
            score += 10
        if cls.DIGIT_PATTERN.search(password):
            score += 10
        if cls.SPECIAL_PATTERN.search(password):
            score += 10
        
        # Bonus for length (up to 30 points)
        if len(password) >= 12:
            score += 15
        if len(password) >= 16:
            score += 15
        
        return min(score, 100)
    
    def __str__(self) -> str:
        return "***REDACTED***"
    
    def __repr__(self) -> str:
        return f"Password(hash='***')"
    
    def __eq__(self, other) -> bool:
        if isinstance(other, Password):
            return self.hash == other.hash
        if isinstance(other, str):
            return self.hash == other
        return False
    
    def __hash__(self) -> int:
        return hash(self.hash)
    
    def to_dict(self) -> dict:
        """Convert to dictionary (without exposing hash)."""
        return {
            "length": len(self.hash),
            "has_uppercase": bool(self.UPPERCASE_PATTERN.search(self.hash)),
            "has_lowercase": bool(self.LOWERCASE_PATTERN.search(self.hash)),
            "has_digit": bool(self.DIGIT_PATTERN.search(self.hash)),
            "has_special": bool(self.SPECIAL_PATTERN.search(self.hash)),
            "strength_score": self.calculate_strength(self.hash),
        }
