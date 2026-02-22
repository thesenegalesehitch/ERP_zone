"""
Email Value Object - Domain Layer
Represents a validated email address.

Author: Alexandre Albert Ndour
"""

import re
from dataclasses import dataclass


@dataclass(frozen=True)
class Email:
    """
    Email Value Object.
    
    Immutable value object that represents and validates
    an email address.
    """
    
    value: str
    
    # Email regex pattern (RFC 5322 simplified)
    EMAIL_PATTERN = re.compile(
        r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    )
    
    def __post_init__(self):
        """Validate email after initialization."""
        if not self.value:
            raise ValueError("Email cannot be empty")
        
        normalized = self.value.lower().strip()
        
        if not self.EMAIL_PATTERN.match(normalized):
            raise ValueError(f"Invalid email format: {self.value}")
        
        # Use dataclass frozen=True makes this immutable
        # We need to use object.__setattr__ to set the validated value
        object.__setattr__(self, 'value', normalized)
    
    def __str__(self) -> str:
        return self.value
    
    def __repr__(self) -> str:
        return f"Email('{self.value}')"
    
    def __eq__(self, other) -> bool:
        if isinstance(other, Email):
            return self.value == other.value
        if isinstance(other, str):
            return self.value == other.lower()
        return False
    
    def __hash__(self) -> int:
        return hash(self.value)
    
    def get_domain(self) -> str:
        """Get the domain part of the email."""
        return self.value.split('@')[1]
    
    def get_local_part(self) -> str:
        """Get the local part (before @) of the email."""
        return self.value.split('@')[0]
    
    def is_corporate(self, corporate_domains: list = None) -> bool:
        """Check if email is from corporate domain."""
        if corporate_domains is None:
            corporate_domains = []
        domain = self.get_domain()
        return domain in corporate_domains
    
    @classmethod
    def is_valid(cls, email: str) -> bool:
        """Check if an email string is valid."""
        if not email:
            return False
        return bool(cls.EMAIL_PATTERN.match(email.lower().strip()))


# Convenience function for creating Email
def create_email(value: str) -> Email:
    """Factory function to create an Email value object."""
    return Email(value)
