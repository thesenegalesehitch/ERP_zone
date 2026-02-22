"""
Tax Entity for ERP System.

This module provides the Tax entity for managing taxes
following Clean Architecture principles.
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional, Dict, Any, List
from enum import Enum
from decimal import Decimal


class TaxType(str, Enum):
    """Tax type enumeration."""
    SALES = "sales"
    VAT = "vat"
    GST = "gst"
    PST = "pst"
    HST = "hst"
    INCOME = "income"
    WITHHOLDING = "withholding"
    CUSTOM = "custom"


class TaxStatus(str, Enum):
    """Tax status enumeration."""
    ACTIVE = "active"
    INACTIVE = "inactive"
    PENDING = "pending"
    EXPIRED = "expired"


class TaxCalculationMethod(str, Enum):
    """Tax calculation method enumeration."""
    FIXED = "fixed"
    PERCENTAGE = "percentage"
    TIERED = "tiered"


@dataclass(frozen=True)
class TaxRate:
    """
    Value Object representing a tax rate.
    Immutable and validated.
    """
    id: str
    rate: Decimal
    min_amount: Optional[Decimal] = None
    max_amount: Optional[Decimal] = None
    effective_from: Optional[datetime] = None
    effective_to: Optional[datetime] = None
    
    def __post_init__(self):
        if self.rate < 0:
            raise ValueError("rate cannot be negative")
        if self.min_amount is not None and self.max_amount is not None:
            if self.min_amount > self.max_amount:
                raise ValueError("min_amount cannot exceed max_amount")
    
    @property
    def is_tiered(self) -> bool:
        """Check if this is a tiered rate."""
        return self.min_amount is not None or self.max_amount is not None
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "rate": str(self.rate),
            "min_amount": str(self.min_amount) if self.min_amount else None,
            "max_amount": str(self.max_amount) if self.max_amount else None,
            "effective_from": self.effective_from.isoformat() if self.effective_from else None,
            "effective_to": self.effective_to.isoformat() if self.effective_to else None,
            "is_tiered": self.is_tiered
        }


@dataclass(frozen=True)
class Tax:
    """
    Tax entity representing a tax configuration.
    
    This entity follows Clean Architecture principles and is immutable.
    
    Attributes:
        id: Unique identifier for the tax
        name: Tax name
        code: Tax code
        tax_type: Type of tax
        status: Current status
        calculation_method: How tax is calculated
        rates: List of tax rates
        country: Country code
        state: State/Province code
        is_compound: Whether this is a compound tax
        is_recoverable: Whether tax is recoverable
        account_id: Tax account ID
        notes: Additional notes
        metadata: Additional metadata
        created_at: Timestamp when created
        updated_at: Timestamp when last updated
    """
    id: str
    name: str
    code: str
    tax_type: TaxType
    status: TaxStatus
    calculation_method: TaxCalculationMethod
    rates: List[TaxRate]
    country: str
    state: Optional[str] = None
    is_compound: bool = False
    is_recoverable: bool = False
    account_id: Optional[str] = None
    notes: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime = field(default_factory=datetime.utcnow)
    
    def __post_init__(self):
        """Validate tax after initialization."""
        if not self.name:
            raise ValueError("name cannot be empty")
        if not self.code:
            raise ValueError("code cannot be empty")
        if not self.country:
            raise ValueError("country cannot be empty")
        if not self.rates:
            raise ValueError("tax must have at least one rate")
    
    @property
    def is_active(self) -> bool:
        """Check if tax is active."""
        return self.status == TaxStatus.ACTIVE
    
    @property
    def current_rate(self) -> Optional[TaxRate]:
        """Get the current applicable rate."""
        now = datetime.utcnow()
        for rate in self.rates:
            if rate.effective_from and rate.effective_from > now:
                continue
            if rate.effective_to and rate.effective_to < now:
                continue
            return rate
        return self.rates[0] if self.rates else None
    
    @property
    def rate_count(self) -> int:
        """Get number of rates."""
        return len(self.rates)
    
    @property
    def jurisdiction(self) -> str:
        """Get full jurisdiction string."""
        if self.state:
            return f"{self.country}-{self.state}"
        return self.country
    
    def calculate_tax(self, amount: Decimal) -> Decimal:
        """Calculate tax amount."""
        rate = self.current_rate
        if not rate:
            return Decimal("0")
        return amount * (rate.rate / 100)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert tax to dictionary."""
        return {
            "id": self.id,
            "name": self.name,
            "code": self.code,
            "tax_type": self.tax_type.value,
            "status": self.status.value,
            "calculation_method": self.calculation_method.value,
            "rates": [r.to_dict() for r in self.rates],
            "country": self.country,
            "state": self.state,
            "jurisdiction": self.jurisdiction,
            "is_compound": self.is_compound,
            "is_recoverable": self.is_recoverable,
            "account_id": self.account_id,
            "notes": self.notes,
            "metadata": self.metadata,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
            "is_active": self.is_active,
            "current_rate": self.current_rate.to_dict() if self.current_rate else None,
            "rate_count": self.rate_count
        }


class TaxBuilder:
    """Builder for creating Tax instances."""
    
    def __init__(self):
        self._id: Optional[str] = None
        self._name: Optional[str] = None
        self._code: Optional[str] = None
        self._tax_type: TaxType = TaxType.SALES
        self._status: TaxStatus = TaxStatus.ACTIVE
        self._calculation_method: TaxCalculationMethod = TaxCalculationMethod.PERCENTAGE
        self._rates: List[TaxRate] = []
        self._country: Optional[str] = None
        self._state: Optional[str] = None
        self._is_compound: bool = False
        self._is_recoverable: bool = False
        self._account_id: Optional[str] = None
        self._notes: Optional[str] = None
        self._metadata: Dict[str, Any] = {}
    
    def with_id(self, tax_id: str) -> "TaxBuilder":
        self._id = tax_id
        return self
    
    def with_name(self, name: str) -> "TaxBuilder":
        self._name = name
        return self
    
    def with_code(self, code: str) -> "TaxBuilder":
        self._code = code
        return self
    
    def with_type(self, tax_type: TaxType) -> "TaxBuilder":
        self._tax_type = tax_type
        return self
    
    def with_status(self, status: TaxStatus) -> "TaxBuilder":
        self._status = status
        return self
    
    def with_calculation_method(self, method: TaxCalculationMethod) -> "TaxBuilder":
        self._calculation_method = method
        return self
    
    def with_rates(self, rates: List[TaxRate]) -> "TaxBuilder":
        self._rates = rates
        return self
    
    def add_rate(self, rate: TaxRate) -> "TaxBuilder":
        self._rates.append(rate)
        return self
    
    def in_country(self, country: str, state: Optional[str] = None) -> "TaxBuilder":
        self._country = country
        self._state = state
        return self
    
    def compound(self, is_compound: bool = True) -> "TaxBuilder":
        self._is_compound = is_compound
        return self
    
    def recoverable(self, is_recoverable: bool = True) -> "TaxBuilder":
        self._is_recoverable = is_recoverable
        return self
    
    def with_account(self, account_id: str) -> "TaxBuilder":
        self._account_id = account_id
        return self
    
    def with_notes(self, notes: str) -> "TaxBuilder":
        self._notes = notes
        return self
    
    def with_metadata(self, metadata: Dict[str, Any]) -> "TaxBuilder":
        self._metadata = metadata
        return self
    
    def build(self) -> Tax:
        from uuid import uuid4
        
        if not self._id:
            self._id = str(uuid4())
        if not self._name:
            raise ValueError("name is required")
        if not self._code:
            raise ValueError("code is required")
        if not self._country:
            raise ValueError("country is required")
        if not self._rates:
            raise ValueError("rates is required")
        
        return Tax(
            id=self._id,
            name=self._name,
            code=self._code,
            tax_type=self._tax_type,
            status=self._status,
            calculation_method=self._calculation_method,
            rates=self._rates,
            country=self._country,
            state=self._state,
            is_compound=self._is_compound,
            is_recoverable=self._is_recoverable,
            account_id=self._account_id,
            notes=self._notes,
            metadata=self._metadata
        )


# Factory functions
def create_tax_rate(
    rate: Decimal,
    **kwargs
) -> TaxRate:
    """Factory function to create a tax rate."""
    from uuid import uuid4
    
    return TaxRate(
        id=str(uuid4()),
        rate=rate,
        min_amount=kwargs.get("min_amount"),
        max_amount=kwargs.get("max_amount"),
        effective_from=kwargs.get("effective_from"),
        effective_to=kwargs.get("effective_to")
    )


def create_tax(
    name: str,
    code: str,
    country: str,
    rates: List[TaxRate],
    **kwargs
) -> Tax:
    """Factory function to create a tax."""
    builder = TaxBuilder()
    builder.with_name(name)
    builder.with_code(code)
    builder.in_country(country, kwargs.get("state"))
    builder.with_rates(rates)
    
    if tax_type := kwargs.get("tax_type"):
        builder.with_type(tax_type)
    if status := kwargs.get("status"):
        builder.with_status(status)
    if calculation_method := kwargs.get("calculation_method"):
        builder.with_calculation_method(calculation_method)
    if is_compound := kwargs.get("is_compound"):
        builder.compound(is_compound)
    if is_recoverable := kwargs.get("is_recoverable"):
        builder.recoverable(is_recoverable)
    if account_id := kwargs.get("account_id"):
        builder.with_account(account_id)
    if notes := kwargs.get("notes"):
        builder.with_notes(notes)
    if metadata := kwargs.get("metadata"):
        builder.with_metadata(metadata)
    
    return builder.build()
