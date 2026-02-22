"""
Currency Entity for ERP System.

This module provides the Currency entity for managing currencies
following Clean Architecture principles.
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional, Dict, Any
from enum import Enum
from decimal import Decimal


class CurrencyStatus(str, Enum):
    """Currency status enumeration."""
    ACTIVE = "active"
    INACTIVE = "inactive"
    DEPRECATED = "deprecated"


class CurrencyFormat(str, Enum):
    """Currency format enumeration."""
    SYMBOL = "symbol"
    CODE = "code"
    NAME = "name"


@dataclass(frozen=True)
class ExchangeRate:
    """
    Value Object representing an exchange rate.
    Immutable and validated.
    """
    id: str
    from_currency: str
    to_currency: str
    rate: Decimal
    effective_date: datetime
    
    def __post_init__(self):
        if self.rate <= 0:
            raise ValueError("rate must be positive")
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "from_currency": self.from_currency,
            "to_currency": self.to_currency,
            "rate": str(self.rate),
            "effective_date": self.effective_date.isoformat()
        }


@dataclass(frozen=True)
class Currency:
    """
    Currency entity representing a currency in the ERP system.
    
    This entity follows Clean Architecture principles and is immutable.
    
    Attributes:
        id: Unique identifier for the currency
        code: Currency code (ISO 4217)
        name: Currency name
        symbol: Currency symbol
        status: Current status
        decimal_places: Number of decimal places
        exchange_rate: Exchange rate to base currency
        format: Currency format style
        is_base: Whether this is the base currency
        metadata: Additional metadata
        created_at: Timestamp when created
        updated_at: Timestamp when last updated
    """
    id: str
    code: str
    name: str
    symbol: str
    status: CurrencyStatus
    decimal_places: int = 2
    exchange_rate: Optional[Decimal] = None
    format: CurrencyFormat = CurrencyFormat.SYMBOL
    is_base: bool = False
    metadata: Dict[str, Any] = field(default_factory=dict)
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime = field(default_factory=datetime.utcnow)
    
    def __post_init__(self):
        """Validate currency after initialization."""
        if not self.code:
            raise ValueError("code cannot be empty")
        if not self.name:
            raise ValueError("name cannot be empty")
        if not self.symbol:
            raise ValueError("symbol cannot be empty")
        if self.decimal_places < 0:
            raise ValueError("decimal_places cannot be negative")
    
    @property
    def is_active(self) -> bool:
        """Check if currency is active."""
        return self.status == CurrencyStatus.ACTIVE
    
    @property
    def format_symbol(self) -> str:
        """Get formatted currency symbol."""
        return f"{self.symbol}" if self.format == CurrencyFormat.SYMBOL else self.code
    
    def format_amount(self, amount: Decimal) -> str:
        """Format amount with currency."""
        formatted = f"{amount:.{self.decimal_places}f}"
        if self.format == CurrencyFormat.SYMBOL:
            return f"{self.symbol}{formatted}"
        elif self.format == CurrencyFormat.CODE:
            return f"{formatted} {self.code}"
        return f"{self.name} {formatted}"
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert currency to dictionary."""
        return {
            "id": self.id,
            "code": self.code,
            "name": self.name,
            "symbol": self.symbol,
            "status": self.status.value,
            "decimal_places": self.decimal_places,
            "exchange_rate": str(self.exchange_rate) if self.exchange_rate else None,
            "format": self.format.value,
            "is_base": self.is_base,
            "metadata": self.metadata,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
            "is_active": self.is_active,
            "format_symbol": self.format_symbol
        }


class CurrencyBuilder:
    """Builder for creating Currency instances."""
    
    def __init__(self):
        self._id: Optional[str] = None
        self._code: Optional[str] = None
        self._name: Optional[str] = None
        self._symbol: Optional[str] = None
        self._status: CurrencyStatus = CurrencyStatus.ACTIVE
        self._decimal_places: int = 2
        self._exchange_rate: Optional[Decimal] = None
        self._format: CurrencyFormat = CurrencyFormat.SYMBOL
        self._is_base: bool = False
        self._metadata: Dict[str, Any] = {}
    
    def with_id(self, currency_id: str) -> "CurrencyBuilder":
        self._id = currency_id
        return self
    
    def with_code(self, code: str) -> "CurrencyBuilder":
        self._code = code
        return self
    
    def with_name(self, name: str) -> "CurrencyBuilder":
        self._name = name
        return self
    
    def with_symbol(self, symbol: str) -> "CurrencyBuilder":
        self._symbol = symbol
        return self
    
    def with_status(self, status: CurrencyStatus) -> "CurrencyBuilder":
        self._status = status
        return self
    
    def with_decimal_places(self, decimal_places: int) -> "CurrencyBuilder":
        self._decimal_places = decimal_places
        return self
    
    def with_exchange_rate(self, rate: Decimal) -> "CurrencyBuilder":
        self._exchange_rate = rate
        return self
    
    def with_format(self, format: CurrencyFormat) -> "CurrencyBuilder":
        self._format = format
        return self
    
    def as_base(self, is_base: bool = True) -> "CurrencyBuilder":
        self._is_base = is_base
        return self
    
    def with_metadata(self, metadata: Dict[str, Any]) -> "CurrencyBuilder":
        self._metadata = metadata
        return self
    
    def build(self) -> Currency:
        from uuid import uuid4
        
        if not self._id:
            self._id = str(uuid4())
        if not self._code:
            raise ValueError("code is required")
        if not self._name:
            raise ValueError("name is required")
        if not self._symbol:
            raise ValueError("symbol is required")
        
        return Currency(
            id=self._id,
            code=self._code,
            name=self._name,
            symbol=self._symbol,
            status=self._status,
            decimal_places=self._decimal_places,
            exchange_rate=self._exchange_rate,
            format=self._format,
            is_base=self._is_base,
            metadata=self._metadata
        )


# Factory functions
def create_exchange_rate(
    from_currency: str,
    to_currency: str,
    rate: Decimal,
    effective_date: datetime
) -> ExchangeRate:
    """Factory function to create an exchange rate."""
    from uuid import uuid4
    
    return ExchangeRate(
        id=str(uuid4()),
        from_currency=from_currency,
        to_currency=to_currency,
        rate=rate,
        effective_date=effective_date
    )


def create_currency(
    code: str,
    name: str,
    symbol: str,
    **kwargs
) -> Currency:
    """Factory function to create a currency."""
    builder = CurrencyBuilder()
    builder.with_code(code)
    builder.with_name(name)
    builder.with_symbol(symbol)
    
    if status := kwargs.get("status"):
        builder.with_status(status)
    if decimal_places := kwargs.get("decimal_places"):
        builder.with_decimal_places(decimal_places)
    if exchange_rate := kwargs.get("exchange_rate"):
        builder.with_exchange_rate(exchange_rate)
    if format := kwargs.get("format"):
        builder.with_format(format)
    if is_base := kwargs.get("is_base"):
        builder.as_base(is_base)
    if metadata := kwargs.get("metadata"):
        builder.with_metadata(metadata)
    
    return builder.build()
