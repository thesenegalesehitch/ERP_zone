"""
Contract Entity for ERP System.

This module provides the Contract entity for managing contracts
following Clean Architecture principles.
"""

from dataclasses import dataclass, field
from datetime import datetime, date
from typing import Optional, Dict, Any, List
from enum import Enum
from decimal import Decimal


class ContractStatus(str, Enum):
    """Contract status enumeration."""
    DRAFT = "draft"
    PENDING = "pending"
    ACTIVE = "active"
    EXPIRED = "expired"
    TERMINATED = "terminated"
    CANCELLED = "cancelled"
    RENEWED = "renewed"


class ContractType(str, Enum):
    """Contract type enumeration."""
    SERVICE = "service"
    SUPPLY = "supply"
    LEASE = "lease"
    EMPLOYMENT = "employment"
    PARTNERSHIP = "partnership"
    LICENSE = "license"
    NDA = "nda"
    SLA = "sla"


class PaymentTerm(str, Enum):
    """Payment term enumeration."""
    IMMEDIATE = "immediate"
    NET_15 = "net_15"
    NET_30 = "net_30"
    NET_45 = "net_45"
    NET_60 = "net_60"
    NET_90 = "net_90"
    CUSTOM = "custom"


@dataclass(frozen=True)
class ContractValue:
    """
    Value Object representing contract monetary values.
    Immutable and validated.
    """
    amount: Decimal
    currency: str = "USD"
    
    def __post_init__(self):
        if self.amount < 0:
            raise ValueError("Contract value cannot be negative")
        if not self.currency:
            raise ValueError("Currency is required")
    
    @property
    def is_zero(self) -> bool:
        return self.amount == Decimal("0")
    
    def __add__(self, other: "ContractValue") -> "ContractValue":
        if self.currency != other.currency:
            raise ValueError("Cannot add different currencies")
        return ContractValue(
            amount=self.amount + other.amount,
            currency=self.currency
        )
    
    def __mul__(self, multiplier: int) -> "ContractValue":
        return ContractValue(
            amount=self.amount * multiplier,
            currency=self.currency
        )


@dataclass(frozen=True)
class Contract:
    """
    Contract entity representing a legal agreement in the ERP system.
    
    This entity follows Clean Architecture principles and is immutable.
    
    Attributes:
        id: Unique identifier for the contract
        contract_number: Human-readable contract number
        title: Contract title
        description: Contract description
        contract_type: Type of contract
        status: Current status of the contract
        party_a: First party (organization)
        party_b: Second party (client/supplier)
        start_date: Contract start date
        end_date: Contract end date
        value: Contract monetary value
        payment_term: Payment terms
        renewal_date: Date for renewal consideration
        auto_renew: Whether the contract auto-renews
        terms_and_conditions: Contract T&C text
        attachments: List of attachment URLs
        signed_date: Date when contract was signed
        created_by: User who created the contract
        approvers: List of approver user IDs
        metadata: Additional metadata
        created_at: Timestamp when created
        updated_at: Timestamp when last updated
    """
    id: str
    contract_number: str
    title: str
    description: str
    contract_type: ContractType
    status: ContractStatus
    party_a: str
    party_b: str
    start_date: date
    end_date: date
    value: ContractValue
    payment_term: PaymentTerm
    renewal_date: Optional[date] = None
    auto_renew: bool = False
    terms_and_conditions: Optional[str] = None
    attachments: List[str] = field(default_factory=list)
    signed_date: Optional[date] = None
    created_by: Optional[str] = None
    approvers: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime = field(default_factory=datetime.utcnow)
    
    def __post_init__(self):
        """Validate contract after initialization."""
        if not self.title:
            raise ValueError("title cannot be empty")
        if not self.party_a:
            raise ValueError("party_a cannot be empty")
        if not self.party_b:
            raise ValueError("party_b cannot be empty")
        if self.end_date < self.start_date:
            raise ValueError("end_date must be after start_date")
        if self.renewal_date and self.renewal_date < self.start_date:
            raise ValueError("renewal_date must be after start_date")
    
    @property
    def is_active(self) -> bool:
        """Check if contract is currently active."""
        today = date.today()
        return (
            self.status == ContractStatus.ACTIVE
            and self.start_date <= today <= self.end_date
        )
    
    @property
    def is_expired(self) -> bool:
        """Check if contract has expired."""
        return date.today() > self.end_date
    
    @property
    def days_remaining(self) -> Optional[int]:
        """Get days remaining until contract expires."""
        if not self.is_active:
            return None
        delta = self.end_date - date.today()
        return delta.days
    
    @property
    def duration_months(self) -> int:
        """Calculate contract duration in months."""
        months = (self.end_date.year - self.start_date.year) * 12
        months += self.end_date.month - self.start_date.month
        return max(1, months)
    
    @property
    def monthly_value(self) -> ContractValue:
        """Calculate monthly value of the contract."""
        monthly = self.value.amount / self.duration_months
        return ContractValue(amount=monthly, currency=self.value.currency)
    
    def can_renew(self) -> bool:
        """Check if contract can be renewed."""
        if self.status in [ContractStatus.TERMINATED, ContractStatus.CANCELLED]:
            return False
        if self.renewal_date and date.today() >= self.renewal_date:
            return True
        if self.auto_renew and self.is_active:
            return True
        return False
    
    def needs_approval(self) -> bool:
        """Check if contract needs approval."""
        return self.status == ContractStatus.PENDING and bool(self.approvers)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert contract to dictionary."""
        return {
            "id": self.id,
            "contract_number": self.contract_number,
            "title": self.title,
            "description": self.description,
            "contract_type": self.contract_type.value,
            "status": self.status.value,
            "party_a": self.party_a,
            "party_b": self.party_b,
            "start_date": self.start_date.isoformat(),
            "end_date": self.end_date.isoformat(),
            "value": {
                "amount": str(self.value.amount),
                "currency": self.value.currency
            },
            "payment_term": self.payment_term.value,
            "renewal_date": self.renewal_date.isoformat() if self.renewal_date else None,
            "auto_renew": self.auto_renew,
            "terms_and_conditions": self.terms_and_conditions,
            "attachments": self.attachments,
            "signed_date": self.signed_date.isoformat() if self.signed_date else None,
            "created_by": self.created_by,
            "approvers": self.approvers,
            "metadata": self.metadata,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
            "is_active": self.is_active,
            "is_expired": self.is_expired,
            "days_remaining": self.days_remaining,
            "duration_months": self.duration_months
        }


class ContractBuilder:
    """Builder for creating Contract instances."""
    
    def __init__(self):
        self._id: Optional[str] = None
        self._contract_number: Optional[str] = None
        self._title: Optional[str] = None
        self._description: str = ""
        self._contract_type: Optional[ContractType] = None
        self._status: ContractStatus = ContractStatus.DRAFT
        self._party_a: Optional[str] = None
        self._party_b: Optional[str] = None
        self._start_date: Optional[date] = None
        self._end_date: Optional[date] = None
        self._value: Optional[ContractValue] = None
        self._payment_term: PaymentTerm = PaymentTerm.NET_30
        self._renewal_date: Optional[date] = None
        self._auto_renew: bool = False
        self._terms_and_conditions: Optional[str] = None
        self._attachments: List[str] = []
        self._signed_date: Optional[date] = None
        self._created_by: Optional[str] = None
        self._approvers: List[str] = []
        self._metadata: Dict[str, Any] = {}
    
    def with_id(self, contract_id: str) -> "ContractBuilder":
        self._id = contract_id
        return self
    
    def with_contract_number(self, number: str) -> "ContractBuilder":
        self._contract_number = number
        return self
    
    def with_title(self, title: str) -> "ContractBuilder":
        self._title = title
        return self
    
    def with_description(self, description: str) -> "ContractBuilder":
        self._description = description
        return self
    
    def with_type(self, contract_type: ContractType) -> "ContractBuilder":
        self._contract_type = contract_type
        return self
    
    def with_status(self, status: ContractStatus) -> "ContractBuilder":
        self._status = status
        return self
    
    def between(self, party_a: str, party_b: str) -> "ContractBuilder":
        self._party_a = party_a
        self._party_b = party_b
        return self
    
    def valid_from(self, start_date: date, end_date: date) -> "ContractBuilder":
        self._start_date = start_date
        self._end_date = end_date
        return self
    
    def with_value(self, amount: Decimal, currency: str = "USD") -> "ContractBuilder":
        self._value = ContractValue(amount=amount, currency=currency)
        return self
    
    def with_payment_term(self, term: PaymentTerm) -> "ContractBuilder":
        self._payment_term = term
        return self
    
    def with_renewal(self, renewal_date: Optional[date] = None, auto_renew: bool = False) -> "ContractBuilder":
        self._renewal_date = renewal_date
        self._auto_renew = auto_renew
        return self
    
    def with_terms(self, terms: str) -> "ContractBuilder":
        self._terms_and_conditions = terms
        return self
    
    def with_attachments(self, attachments: List[str]) -> "ContractBuilder":
        self._attachments = attachments
        return self
    
    def signed_on(self, signed_date: date) -> "ContractBuilder":
        self._signed_date = signed_date
        return self
    
    def created_by(self, user_id: str) -> "ContractBuilder":
        self._created_by = user_id
        return self
    
    def with_approvers(self, approvers: List[str]) -> "ContractBuilder":
        self._approvers = approvers
        return self
    
    def with_metadata(self, metadata: Dict[str, Any]) -> "ContractBuilder":
        self._metadata = metadata
        return self
    
    def build(self) -> Contract:
        from uuid import uuid4
        
        if not self._id:
            self._id = str(uuid4())
        if not self._contract_number:
            from time import time
            self._contract_number = f"CNT-{int(time())}"
        if not self._title:
            raise ValueError("title is required")
        if not self._party_a:
            raise ValueError("party_a is required")
        if not self._party_b:
            raise ValueError("party_b is required")
        if not self._start_date:
            raise ValueError("start_date is required")
        if not self._end_date:
            raise ValueError("end_date is required")
        if not self._value:
            self._value = ContractValue(amount=Decimal("0"), currency="USD")
        
        return Contract(
            id=self._id,
            contract_number=self._contract_number,
            title=self._title,
            description=self._description,
            contract_type=self._contract_type or ContractType.SERVICE,
            status=self._status,
            party_a=self._party_a,
            party_b=self._party_b,
            start_date=self._start_date,
            end_date=self._end_date,
            value=self._value,
            payment_term=self._payment_term,
            renewal_date=self._renewal_date,
            auto_renew=self._auto_renew,
            terms_and_conditions=self._terms_and_conditions,
            attachments=self._attachments,
            signed_date=self._signed_date,
            created_by=self._created_by,
            approvers=self._approvers,
            metadata=self._metadata
        )


# Factory functions
def create_contract(
    title: str,
    party_a: str,
    party_b: str,
    start_date: date,
    end_date: date,
    amount: Decimal,
    currency: str = "USD",
    contract_type: ContractType = ContractType.SERVICE,
    **kwargs
) -> Contract:
    """Factory function to create a contract."""
    builder = ContractBuilder()
    builder.with_title(title)
    builder.between(party_a, party_b)
    builder.valid_from(start_date, end_date)
    builder.with_value(amount, currency)
    builder.with_type(contract_type)
    
    if contract_number := kwargs.get("contract_number"):
        builder.with_contract_number(contract_number)
    if description := kwargs.get("description"):
        builder.with_description(description)
    if status := kwargs.get("status"):
        builder.with_status(status)
    if payment_term := kwargs.get("payment_term"):
        builder.with_payment_term(payment_term)
    if renewal_date := kwargs.get("renewal_date"):
        builder.with_renewal(renewal_date, kwargs.get("auto_renew", False))
    if terms := kwargs.get("terms_and_conditions"):
        builder.with_terms(terms)
    if attachments := kwargs.get("attachments"):
        builder.with_attachments(attachments)
    if signed_date := kwargs.get("signed_date"):
        builder.signed_on(signed_date)
    if created_by := kwargs.get("created_by"):
        builder.created_by(created_by)
    if approvers := kwargs.get("approvers"):
        builder.with_approvers(approvers)
    if metadata := kwargs.get("metadata"):
        builder.with_metadata(metadata)
    
    return builder.build()
