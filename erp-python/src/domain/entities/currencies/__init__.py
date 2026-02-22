"""
Currency Entity - Domain Layer
Represents currencies in the ERP system.

Author: Alexandre Albert Ndour
"""

from dataclasses import dataclass, field
from datetime import datetime, timezone
import uuid


@dataclass
class Currency:
    """Currency entity."""
    
    id: uuid.UUID = field(default_factory=uuid.uuid4)
    code: str = ""  # ISO 4217 code (e.g., EUR, USD)
    name: str = ""
    symbol: str = ""
    
    exchange_rate: float = 1.0  # Rate to base currency
    is_base: bool = False
    is_active: bool = True
    
    decimal_places: int = 2
    
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    
    def convert_to(self, amount: float, target_currency: "Currency") -> float:
        """Convert amount to target currency."""
        if self.code == target_currency.code:
            return amount
        return amount * target_currency.exchange_rate / self.exchange_rate
    
    def format_amount(self, amount: float) -> str:
        """Format amount with currency symbol."""
        return f"{self.symbol}{amount:.{self.decimal_places}f}"
    
    def to_dict(self) -> dict:
        return {
            "id": str(self.id),
            "code": self.code,
            "name": self.name,
            "symbol": self.symbol,
            "exchange_rate": self.exchange_rate,
            "is_base": self.is_base,
            "is_active": self.is_active,
            "decimal_places": self.decimal_places,
        }
