"""
Customer Entity - Domain Layer
Represents a customer in the ERP system.

Author: Alexandre Albert Ndour
"""

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Optional, List
from enum import Enum
import uuid


class CustomerType(str, Enum):
    """Customer type enumeration."""
    INDIVIDUAL = "individual"
    COMPANY = "company"
    GOVERNMENT = "government"


class CustomerStatus(str, Enum):
    """Customer status enumeration."""
    PROSPECT = "prospect"
    ACTIVE = "active"
    INACTIVE = "inactive"
    BLOCKED = "blocked"


@dataclass
class Customer:
    """
    Customer Entity.
    
    Represents a customer (individual or company).
    """
    
    # Identity
    id: uuid.UUID = field(default_factory=uuid.uuid4)
    customer_number: str = ""
    
    # Type and status
    customer_type: CustomerType = CustomerType.INDIVIDUAL
    status: CustomerStatus = CustomerStatus.PROSPECT
    
    # Company info (for business customers)
    company_name: Optional[str] = None
    company_registration: Optional[str] = None
    company_tax_id: Optional[str] = None
    
    # Person info (for individual customers)
    first_name: str = ""
    last_name: str = ""
    
    # Contact
    email: str = ""
    phone: Optional[str] = None
    website: Optional[str] = None
    
    # Classification
    customer_group: Optional[str] = None
    sales_channel: Optional[str] = None
    price_list_id: Optional[uuid.UUID] = None
    
    # Credit
    credit_limit: float = 0.0
    credit_balance: float = 0.0
    
    # Tax
    tax_exempt: bool = False
    tax_id: Optional[str] = None
    
    # Notes
    notes: Optional[str] = None
    
    # Referrer
    referred_by: Optional[uuid.UUID] = None
    
    # Metadata
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    created_by: Optional[uuid.UUID] = None
    
    # Addresses (loaded separately)
    _addresses: List["Address"] = field(default_factory=list, repr=False)
    
    # ==================== Business Methods ====================
    
    def add_address(self, address: "Address") -> None:
        """Add an address to the customer."""
        address.customer_id = self.id
        self._addresses.append(address)
        self.updated_at = datetime.now(timezone.utc)
    
    def remove_address(self, address_id: uuid.UUID) -> None:
        """Remove an address from the customer."""
        self._addresses = [a for a in self._addresses if a.id != address_id]
        self.updated_at = datetime.now(timezone.utc)
    
    def activate(self) -> None:
        """Activate the customer."""
        self.status = CustomerStatus.ACTIVE
        self.updated_at = datetime.now(timezone.utc)
    
    def deactivate(self) -> None:
        """Deactivate the customer."""
        self.status = CustomerStatus.INACTIVE
        self.updated_at = datetime.now(timezone.utc)
    
    def block(self, reason: str = None) -> None:
        """Block the customer."""
        self.status = CustomerStatus.BLOCKED
        self.notes = reason
        self.updated_at = datetime.now(timezone.utc)
    
    def update_credit_balance(self, amount: float) -> None:
        """Update credit balance."""
        new_balance = self.credit_balance + amount
        if new_balance > self.credit_limit:
            raise ValueError("Credit limit exceeded")
        self.credit_balance = new_balance
        self.updated_at = datetime.now(timezone.utc)
    
    def can_make_purchase(self, amount: float) -> bool:
        """Check if customer can make a purchase."""
        return (self.credit_balance + amount) <= self.credit_limit
    
    # ==================== Properties ====================
    
    @property
    def name(self) -> str:
        """Get customer name."""
        if self.customer_type == CustomerType.COMPANY:
            return self.company_name or ""
        return f"{self.first_name} {self.last_name}".strip()
    
    @property
    def addresses(self) -> List["Address"]:
        """Get customer addresses."""
        return self._addresses.copy()
    
    @property
    def primary_address(self) -> Optional["Address"]:
        """Get primary address."""
        for addr in self._addresses:
            if addr.is_primary:
                return addr
        return self._addresses[0] if self._addresses else None
    
    @property
    def available_credit(self) -> float:
        """Get available credit."""
        return self.credit_limit - self.credit_balance
    
    @property
    def is_active(self) -> bool:
        """Check if customer is active."""
        return self.status == CustomerStatus.ACTIVE
    
    # ==================== Factory Methods ====================
    
    @classmethod
    def create(
        cls,
        customer_type: CustomerType,
        email: str,
        first_name: str = "",
        last_name: str = "",
        company_name: str = None,
        created_by: uuid.UUID = None
    ) -> "Customer":
        """Factory method to create a customer."""
        customer_number = cls._generate_customer_number(customer_type)
        
        return cls(
            customer_number=customer_number,
            customer_type=customer_type,
            email=email,
            first_name=first_name,
            last_name=last_name,
            company_name=company_name,
            created_by=created_by
        )
    
    @classmethod
    def _generate_customer_number(cls, customer_type: CustomerType) -> str:
        """Generate customer number."""
        prefix = "CUST"
        if customer_type == CustomerType.COMPANY:
            prefix = "COMP"
        elif customer_type == CustomerType.GOVERNMENT:
            prefix = "GOV"
        
        return f"{prefix}-{uuid.uuid4().hex[:8].upper()}"
    
    # ==================== Serialization ====================
    
    def to_dict(self) -> dict:
        """Convert to dictionary."""
        return {
            "id": str(self.id),
            "customer_number": self.customer_number,
            "customer_type": self.customer_type.value,
            "status": self.status.value,
            "company_name": self.company_name,
            "company_registration": self.company_registration,
            "company_tax_id": self.company_tax_id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "name": self.name,
            "email": self.email,
            "phone": self.phone,
            "website": self.website,
            "customer_group": self.customer_group,
            "credit_limit": self.credit_limit,
            "credit_balance": self.credit_balance,
            "available_credit": self.available_credit,
            "tax_exempt": self.tax_exempt,
            "tax_id": self.tax_id,
            "is_active": self.is_active,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
        }


@dataclass
class Address:
    """
    Address Entity.
    
    Represents a customer address.
    """
    
    # Identity
    id: uuid.UUID = field(default_factory=uuid.uuid4)
    customer_id: uuid.UUID = None  # type: ignore
    
    # Address fields
    address_type: str = "billing"  # billing, shipping
    is_primary: bool = False
    
    name: str = ""
    line1: str = ""
    line2: Optional[str] = None
    city: str = ""
    state: Optional[str] = None
    postal_code: str = ""
    country: str = ""
    
    # Contact
    contact_name: Optional[str] = None
    contact_phone: Optional[str] = None
    
    # Metadata
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    
    def __post_init__(self):
        if isinstance(self.customer_id, str):
            self.customer_id = uuid.UUID(self.customer_id)
    
    @property
    def full_address(self) -> str:
        """Get formatted address."""
        parts = [self.line1]
        if self.line2:
            parts.append(self.line2)
        parts.append(f"{self.postal_code} {self.city}")
        if self.state:
            parts.append(self.state)
        parts.append(self.country)
        return ", ".join(p for p in parts if p)
    
    @classmethod
    def create(
        cls,
        customer_id: uuid.UUID,
        line1: str,
        city: str,
        postal_code: str,
        country: str,
        address_type: str = "billing",
        is_primary: bool = False,
        line2: str = None,
        state: str = None,
        name: str = ""
    ) -> "Address":
        """Factory method to create an address."""
        return cls(
            customer_id=customer_id,
            line1=line1,
            city=city,
            postal_code=postal_code,
            country=country,
            address_type=address_type,
            is_primary=is_primary,
            line2=line2,
            state=state,
            name=name or address_type.title()
        )
    
    def to_dict(self) -> dict:
        return {
            "id": str(self.id),
            "customer_id": str(self.customer_id),
            "address_type": self.address_type,
            "is_primary": self.is_primary,
            "name": self.name,
            "line1": self.line1,
            "line2": self.line2,
            "city": self.city,
            "state": self.state,
            "postal_code": self.postal_code,
            "country": self.country,
            "contact_name": self.contact_name,
            "contact_phone": self.contact_phone,
            "full_address": self.full_address,
            "created_at": self.created_at.isoformat(),
        }
