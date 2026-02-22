"""
Tax Entity - Domain Layer
Represents taxes in the ERP system.

Author: Alexandre Albert Ndour
"""

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Optional
import uuid


@dataclass
class Tax:
    """
    Tax Entity.
    
    Represents a tax rate or rule.
    """
    
    id: uuid.UUID = field(default_factory=uuid.uuid4)
    name: str = ""
    code: str = ""
    rate: float = 0.0  # percentage
    
    tax_type: str = "percentage"  # percentage, fixed
    country: str = ""
    region: Optional[str] = None
    
    is_active: bool = True
    is_default: bool = False
    
    applies_to: str = "all"  # all, products, services
    
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    
    def calculate_tax(self, amount: float) -> float:
        """Calculate tax amount."""
        if self.tax_type == "percentage":
            return amount * (self.rate / 100)
        return self.rate
    
    @classmethod
    def create(cls, name: str, code: str, rate: float, country: str = "") -> "Tax":
        return cls(name=name, code=code, rate=rate, country=country)
    
    def to_dict(self) -> dict:
        return {
            "id": str(self.id),
            "name": self.name,
            "code": self.code,
            "rate": self.rate,
            "tax_type": self.tax_type,
            "country": self.country,
            "is_active": self.is_active,
            "is_default": self.is_default,
        }
