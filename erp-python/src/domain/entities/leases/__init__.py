"""
Lease Entity for ERP System.

This module provides the Lease entity for managing leases
following Clean Architecture principles.
"""

from dataclasses import dataclass, field
from datetime import datetime, date
from typing import Optional, Dict, Any, List
from enum import Enum
from decimal import Decimal


class LeaseStatus(str, Enum):
    """Lease status enumeration."""
    DRAFT = "draft"
    PENDING = "pending"
    ACTIVE = "active"
    EXPIRED = "expired"
    TERMINATED = "terminated"
    CANCELLED = "cancelled"


class LeaseType(str, Enum):
    """Lease type enumeration."""
    EQUIPMENT = "equipment"
    VEHICLE = "vehicle"
    PROPERTY = "property"
    SOFTWARE = "software"
    OTHER = "other"


class PaymentFrequency(str, Enum):
    """Payment frequency enumeration."""
    DAILY = "daily"
    WEEKLY = "weekly"
    MONTHLY = "monthly"
    QUARTERLY = "quarterly"
    YEARLY = "yearly"


@dataclass(frozen=True)
class LeasePayment:
    """
    Value Object representing a lease payment.
    Immutable and validated.
    """
    id: str
    amount: Decimal
    due_date: date
    paid_date: Optional[date] = None
    status: str = "pending"
    
    def __post_init__(self):
        if self.amount <= 0:
            raise ValueError("amount must be positive")
    
    @property
    def is_paid(self) -> bool:
        return self.paid_date is not None
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "amount": str(self.amount),
            "due_date": self.due_date.isoformat(),
            "paid_date": self.paid_date.isoformat() if self.paid_date else None,
            "status": self.status,
            "is_paid": self.is_paid
        }


@dataclass(frozen=True)
class Lease:
    """
    Lease entity representing a lease agreement.
    
    This entity follows Clean Architecture principles and is immutable.
    
    Attributes:
        id: Unique identifier for the lease
        lease_number: Human-readable lease number
        name: Lease name
        description: Lease description
        lease_type: Type of lease
        status: Current status
        lessor_id: Lessor ID
        lessor_name: Lessor name
        lessee_id: Lessee ID
        lessee_name: Lessee name
        start_date: Lease start date
        end_date: Lease end date
        monthly_payment: Monthly payment amount
        total_amount: Total lease amount
        currency: Currency code
        payment_frequency: Payment frequency
        security_deposit: Security deposit
        payments: List of lease payments
        metadata: Additional metadata
        created_at: Timestamp when created
        updated_at: Timestamp when last updated
    """
    id: str
    lease_number: str
    name: str
    description: str
    lease_type: LeaseType
    status: LeaseStatus
    lessor_id: str
    lessor_name: str
    lessee_id: str
    lessee_name: str
    start_date: date
    end_date: date
    monthly_payment: Decimal
    total_amount: Decimal
    currency: str = "USD"
    payment_frequency: PaymentFrequency = PaymentFrequency.MONTHLY
    security_deposit: Optional[Decimal] = None
    payments: List[LeasePayment] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime = field(default_factory=datetime.utcnow)
    
    def __post_init__(self):
        """Validate lease after initialization."""
        if not self.lease_number:
            raise ValueError("lease_number cannot be empty")
        if not self.name:
            raise ValueError("name cannot be empty")
        if self.end_date < self.start_date:
            raise ValueError("end_date must be after start_date")
        if self.monthly_payment <= 0:
            raise ValueError("monthly_payment must be positive")
    
    @property
    def is_active(self) -> bool:
        """Check if lease is active."""
        today = date.today()
        return self.status == LeaseStatus.ACTIVE and self.start_date <= today <= self.end_date
    
    @property
    def is_expired(self) -> bool:
        """Check if lease is expired."""
        return date.today() > self.end_date
    
    @property
    def remaining_months(self) -> int:
        """Get remaining months."""
        if not self.is_active:
            return 0
        today = date.today()
        months = (self.end_date.year - today.year) * 12
        months += self.end_date.month - today.month
        return max(0, months)
    
    @property
    def total_paid(self) -> Decimal:
        """Get total amount paid."""
        return sum(p.amount for p in self.payments if p.is_paid)
    
    @property
    def total_remaining(self) -> Decimal:
        """Get total remaining amount."""
        return self.total_amount - self.total_paid
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert lease to dictionary."""
        return {
            "id": self.id,
            "lease_number": self.lease_number,
            "name": self.name,
            "description": self.description,
            "lease_type": self.lease_type.value,
            "status": self.status.value,
            "lessor_id": self.lessor_id,
            "lessor_name": self.lessor_name,
            "lessee_id": self.lessee_id,
            "lessee_name": self.lessee_name,
            "start_date": self.start_date.isoformat(),
            "end_date": self.end_date.isoformat(),
            "monthly_payment": str(self.monthly_payment),
            "total_amount": str(self.total_amount),
            "currency": self.currency,
            "payment_frequency": self.payment_frequency.value,
            "security_deposit": str(self.security_deposit) if self.security_deposit else None,
            "payments": [p.to_dict() for p in self.payments],
            "metadata": self.metadata,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
            "is_active": self.is_active,
            "is_expired": self.is_expired,
            "remaining_months": self.remaining_months,
            "total_paid": str(self.total_paid),
            "total_remaining": str(self.total_remaining)
        }


class LeaseBuilder:
    """Builder for creating Lease instances."""
    
    def __init__(self):
        self._id: Optional[str] = None
        self._lease_number: Optional[str] = None
        self._name: Optional[str] = None
        self._description: str = ""
        self._lease_type: LeaseType = LeaseType.EQUIPMENT
        self._status: LeaseStatus = LeaseStatus.DRAFT
        self._lessor_id: Optional[str] = None
        self._lessor_name: Optional[str] = None
        self._lessee_id: Optional[str] = None
        self._lessee_name: Optional[str] = None
        self._start_date: Optional[date] = None
        self._end_date: Optional[date] = None
        self._monthly_payment: Optional[Decimal] = None
        self._total_amount: Optional[Decimal] = None
        self._currency: str = "USD"
        self._payment_frequency: PaymentFrequency = PaymentFrequency.MONTHLY
        self._security_deposit: Optional[Decimal] = None
        self._payments: List[LeasePayment] = []
        self._metadata: Dict[str, Any] = {}
    
    def with_id(self, lease_id: str) -> "LeaseBuilder":
        self._id = lease_id
        return self
    
    def with_number(self, lease_number: str) -> "LeaseBuilder":
        self._lease_number = lease_number
        return self
    
    def with_name(self, name: str) -> "LeaseBuilder":
        self._name = name
        return self
    
    def with_description(self, description: str) -> "LeaseBuilder":
        self._description = description
        return self
    
    def with_type(self, lease_type: LeaseType) -> "LeaseBuilder":
        self._lease_type = lease_type
        return self
    
    def with_status(self, status: LeaseStatus) -> "LeaseBuilder":
        self._status = status
        return self
    
    def between(self, lessor_id: str, lessor_name: str, lessee_id: str, lessee_name: str) -> "LeaseBuilder":
        self._lessor_id = lessor_id
        self._lessor_name = lessor_name
        self._lessee_id = lessee_id
        self._lessee_name = lessee_name
        return self
    
    def valid_from(self, start_date: date, end_date: date) -> "LeaseBuilder":
        self._start_date = start_date
        self._end_date = end_date
        return self
    
    def with_payment(self, monthly_payment: Decimal, total_amount: Decimal) -> "LeaseBuilder":
        self._monthly_payment = monthly_payment
        self._total_amount = total_amount
        return self
    
    def with_currency(self, currency: str) -> "LeaseBuilder":
        self._currency = currency
        return self
    
    def with_frequency(self, frequency: PaymentFrequency) -> "LeaseBuilder":
        self._payment_frequency = frequency
        return self
    
    def with_deposit(self, deposit: Decimal) -> "LeaseBuilder":
        self._security_deposit = deposit
        return self
    
    def with_payments(self, payments: List[LeasePayment]) -> "LeaseBuilder":
        self._payments = payments
        return self
    
    def with_metadata(self, metadata: Dict[str, Any]) -> "LeaseBuilder":
        self._metadata = metadata
        return self
    
    def build(self) -> Lease:
        from uuid import uuid4
        
        if not self._id:
            self._id = str(uuid4())
        if not self._lease_number:
            from time import time
            self._lease_number = f"LSE-{int(time())}"
        if not self._name:
            raise ValueError("name is required")
        if not self._lessor_id:
            raise ValueError("lessor_id is required")
        if not self._lessee_id:
            raise ValueError("lessee_id is required")
        if not self._start_date:
            raise ValueError("start_date is required")
        if not self._end_date:
            raise ValueError("end_date is required")
        if not self._monthly_payment:
            raise ValueError("monthly_payment is required")
        if not self._total_amount:
            raise ValueError("total_amount is required")
        
        return Lease(
            id=self._id,
            lease_number=self._lease_number,
            name=self._name,
            description=self._description,
            lease_type=self._lease_type,
            status=self._status,
            lessor_id=self._lessor_id,
            lessor_name=self._lessor_name,
            lessee_id=self._lessee_id,
            lessee_name=self._lessee_name,
            start_date=self._start_date,
            end_date=self._end_date,
            monthly_payment=self._monthly_payment,
            total_amount=self._total_amount,
            currency=self._currency,
            payment_frequency=self._payment_frequency,
            security_deposit=self._security_deposit,
            payments=self._payments,
            metadata=self._metadata
        )


# Factory function
def create_lease_payment(
    amount: Decimal,
    due_date: date,
    **kwargs
) -> LeasePayment:
    """Factory function to create a lease payment."""
    from uuid import uuid4
    
    return LeasePayment(
        id=str(uuid4()),
        amount=amount,
        due_date=due_date,
        paid_date=kwargs.get("paid_date"),
        status=kwargs.get("status", "pending")
    )


def create_lease(
    name: str,
    lessor_id: str,
    lessor_name: str,
    lessee_id: str,
    lessee_name: str,
    start_date: date,
    end_date: date,
    monthly_payment: Decimal,
    total_amount: Decimal,
    **kwargs
) -> Lease:
    """Factory function to create a lease."""
    builder = LeaseBuilder()
    builder.with_name(name)
    builder.between(lessor_id, lessor_name, lessee_id, lessee_name)
    builder.valid_from(start_date, end_date)
    builder.with_payment(monthly_payment, total_amount)
    
    if lease_number := kwargs.get("lease_number"):
        builder.with_number(lease_number)
    if description := kwargs.get("description"):
        builder.with_description(description)
    if lease_type := kwargs.get("lease_type"):
        builder.with_type(lease_type)
    if status := kwargs.get("status"):
        builder.with_status(status)
    if currency := kwargs.get("currency"):
        builder.with_currency(currency)
    if frequency := kwargs.get("payment_frequency"):
        builder.with_frequency(frequency)
    if deposit := kwargs.get("security_deposit"):
        builder.with_deposit(deposit)
    if metadata := kwargs.get("metadata"):
        builder.with_metadata(metadata)
    
    return builder.build()
