"""
Supplier Entity for ERP System.

This module provides the Supplier entity for managing suppliers/vendors
following Clean Architecture principles.
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional, Dict, Any, List
from enum import Enum
from decimal import Decimal


class SupplierStatus(str, Enum):
    """Supplier status enumeration."""
    ACTIVE = "active"
    INACTIVE = "inactive"
    PENDING = "pending"
    SUSPENDED = "suspended"
    BLOCKED = "blocked"


class SupplierRating(str, Enum):
    """Supplier rating enumeration."""
    EXCELLENT = "excellent"
    GOOD = "good"
    AVERAGE = "average"
    POOR = "poor"
    VERY_POOR = "very_poor"


@dataclass(frozen=True)
class SupplierContact:
    """
    Value Object representing a supplier contact person.
    Immutable and validated.
    """
    id: str
    name: str
    email: str
    phone: Optional[str] = None
    role: Optional[str] = None
    is_primary: bool = False
    
    def __post_init__(self):
        if not self.name:
            raise ValueError("contact name cannot be empty")
        if not self.email:
            raise ValueError("contact email cannot be empty")
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "phone": self.phone,
            "role": self.role,
            "is_primary": self.is_primary
        }


@dataclass(frozen=True)
class SupplierAddress:
    """
    Value Object representing a supplier address.
    Immutable and validated.
    """
    id: str
    street: str
    city: str
    state: Optional[str] = None
    postal_code: Optional[str] = None
    country: str
    is_primary: bool = False
    address_type: str = "billing"
    
    def __post_init__(self):
        if not self.street:
            raise ValueError("street cannot be empty")
        if not self.city:
            raise ValueError("city cannot be empty")
        if not self.country:
            raise ValueError("country cannot be empty")
    
    @property
    def full_address(self) -> str:
        """Get full formatted address."""
        parts = [self.street, self.city]
        if self.state:
            parts.append(self.state)
        if self.postal_code:
            parts.append(self.postal_code)
        parts.append(self.country)
        return ", ".join(parts)
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "street": self.street,
            "city": self.city,
            "state": self.state,
            "postal_code": self.postal_code,
            "country": self.country,
            "full_address": self.full_address,
            "is_primary": self.is_primary,
            "address_type": self.address_type
        }


@dataclass(frozen=True)
class Supplier:
    """
    Supplier entity representing a vendor/supplier in the ERP system.
    
    This entity follows Clean Architecture principles and is immutable.
    
    Attributes:
        id: Unique identifier for the supplier
        supplier_code: Human-readable supplier code
        company_name: Supplier company name
        trade_name: Supplier trade name
        status: Current status of the supplier
        rating: Supplier rating
        contacts: List of contact persons
        addresses: List of addresses
        tax_id: Tax identification number
        payment_terms: Payment terms (days)
        credit_limit: Credit limit
        currency: Default currency
        website: Supplier website
        notes: Additional notes
        tags: List of tags
        metadata: Additional metadata
        created_at: Timestamp when created
        updated_at: Timestamp when last updated
    """
    id: str
    supplier_code: str
    company_name: str
    trade_name: Optional[str]
    status: SupplierStatus
    rating: Optional[SupplierRating]
    contacts: List[SupplierContact] = field(default_factory=list)
    addresses: List[SupplierAddress] = field(default_factory=list)
    tax_id: Optional[str] = None
    payment_terms: int = 30
    credit_limit: Optional[Decimal] = None
    currency: str = "USD"
    website: Optional[str] = None
    notes: Optional[str] = None
    tags: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime = field(default_factory=datetime.utcnow)
    
    def __post_init__(self):
        """Validate supplier after initialization."""
        if not self.supplier_code:
            raise ValueError("supplier_code cannot be empty")
        if not self.company_name:
            raise ValueError("company_name cannot be empty")
        if self.payment_terms < 0:
            raise ValueError("payment_terms cannot be negative")
    
    @property
    def is_active(self) -> bool:
        """Check if supplier is active."""
        return self.status == SupplierStatus.ACTIVE
    
    @property
    def primary_contact(self) -> Optional[SupplierContact]:
        """Get primary contact."""
        for contact in self.contacts:
            if contact.is_primary:
                return contact
        return self.contacts[0] if self.contacts else None
    
    @property
    def primary_address(self) -> Optional[SupplierAddress]:
        """Get primary address."""
        for address in self.addresses:
            if address.is_primary:
                return address
        return self.addresses[0] if self.addresses else None
    
    @property
    def contact_count(self) -> int:
        """Get number of contacts."""
        return len(self.contacts)
    
    @property
    def address_count(self) -> int:
        """Get number of addresses."""
        return len(self.addresses)
    
    def has_credit_limit(self) -> bool:
        """Check if supplier has a credit limit."""
        return self.credit_limit is not None and self.credit_limit > 0
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert supplier to dictionary."""
        return {
            "id": self.id,
            "supplier_code": self.supplier_code,
            "company_name": self.company_name,
            "trade_name": self.trade_name,
            "status": self.status.value,
            "rating": self.rating.value if self.rating else None,
            "contacts": [c.to_dict() for c in self.contacts],
            "addresses": [a.to_dict() for a in self.addresses],
            "tax_id": self.tax_id,
            "payment_terms": self.payment_terms,
            "credit_limit": str(self.credit_limit) if self.credit_limit else None,
            "currency": self.currency,
            "website": self.website,
            "notes": self.notes,
            "tags": self.tags,
            "metadata": self.metadata,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
            "is_active": self.is_active,
            "primary_contact": self.primary_contact.to_dict() if self.primary_contact else None,
            "primary_address": self.primary_address.to_dict() if self.primary_address else None,
            "contact_count": self.contact_count,
            "address_count": self.address_count,
            "has_credit_limit": self.has_credit_limit()
        }


class SupplierBuilder:
    """Builder for creating Supplier instances."""
    
    def __init__(self):
        self._id: Optional[str] = None
        self._supplier_code: Optional[str] = None
        self._company_name: Optional[str] = None
        self._trade_name: Optional[str] = None
        self._status: SupplierStatus = SupplierStatus.PENDING
        self._rating: Optional[SupplierRating] = None
        self._contacts: List[SupplierContact] = []
        self._addresses: List[SupplierAddress] = []
        self._tax_id: Optional[str] = None
        self._payment_terms: int = 30
        self._credit_limit: Optional[Decimal] = None
        self._currency: str = "USD"
        self._website: Optional[str] = None
        self._notes: Optional[str] = None
        self._tags: List[str] = []
        self._metadata: Dict[str, Any] = {}
    
    def with_id(self, supplier_id: str) -> "SupplierBuilder":
        self._id = supplier_id
        return self
    
    def with_code(self, supplier_code: str) -> "SupplierBuilder":
        self._supplier_code = supplier_code
        return self
    
    def with_company_name(self, company_name: str) -> "SupplierBuilder":
        self._company_name = company_name
        return self
    
    def with_trade_name(self, trade_name: str) -> "SupplierBuilder":
        self._trade_name = trade_name
        return self
    
    def with_status(self, status: SupplierStatus) -> "SupplierBuilder":
        self._status = status
        return self
    
    def with_rating(self, rating: SupplierRating) -> "SupplierBuilder":
        self._rating = rating
        return self
    
    def with_contacts(self, contacts: List[SupplierContact]) -> "SupplierBuilder":
        self._contacts = contacts
        return self
    
    def add_contact(self, contact: SupplierContact) -> "SupplierBuilder":
        self._contacts.append(contact)
        return self
    
    def with_addresses(self, addresses: List[SupplierAddress]) -> "SupplierBuilder":
        self._addresses = addresses
        return self
    
    def add_address(self, address: SupplierAddress) -> "SupplierBuilder":
        self._addresses.append(address)
        return self
    
    def with_tax_id(self, tax_id: str) -> "SupplierBuilder":
        self._tax_id = tax_id
        return self
    
    def with_payment_terms(self, terms: int) -> "SupplierBuilder":
        self._payment_terms = terms
        return self
    
    def with_credit_limit(self, limit: Decimal) -> "SupplierBuilder":
        self._credit_limit = limit
        return self
    
    def with_currency(self, currency: str) -> "SupplierBuilder":
        self._currency = currency
        return self
    
    def with_website(self, website: str) -> "SupplierBuilder":
        self._website = website
        return self
    
    def with_notes(self, notes: str) -> "SupplierBuilder":
        self._notes = notes
        return self
    
    def with_tags(self, tags: List[str]) -> "SupplierBuilder":
        self._tags = tags
        return self
    
    def with_metadata(self, metadata: Dict[str, Any]) -> "SupplierBuilder":
        self._metadata = metadata
        return self
    
    def build(self) -> Supplier:
        from uuid import uuid4
        
        if not self._id:
            self._id = str(uuid4())
        if not self._supplier_code:
            from time import time
            self._supplier_code = f"SUP-{int(time())}"
        if not self._company_name:
            raise ValueError("company_name is required")
        
        return Supplier(
            id=self._id,
            supplier_code=self._supplier_code,
            company_name=self._company_name,
            trade_name=self._trade_name,
            status=self._status,
            rating=self._rating,
            contacts=self._contacts,
            addresses=self._addresses,
            tax_id=self._tax_id,
            payment_terms=self._payment_terms,
            credit_limit=self._credit_limit,
            currency=self._currency,
            website=self._website,
            notes=self._notes,
            tags=self._tags,
            metadata=self._metadata
        )


# Factory functions
def create_supplier_contact(
    name: str,
    email: str,
    **kwargs
) -> SupplierContact:
    """Factory function to create a supplier contact."""
    from uuid import uuid4
    
    return SupplierContact(
        id=str(uuid4()),
        name=name,
        email=email,
        phone=kwargs.get("phone"),
        role=kwargs.get("role"),
        is_primary=kwargs.get("is_primary", False)
    )


def create_supplier_address(
    street: str,
    city: str,
    country: str,
    **kwargs
) -> SupplierAddress:
    """Factory function to create a supplier address."""
    from uuid import uuid4
    
    return SupplierAddress(
        id=str(uuid4()),
        street=street,
        city=city,
        state=kwargs.get("state"),
        postal_code=kwargs.get("postal_code"),
        country=country,
        is_primary=kwargs.get("is_primary", False),
        address_type=kwargs.get("address_type", "billing")
    )


def create_supplier(
    company_name: str,
    **kwargs
) -> Supplier:
    """Factory function to create a supplier."""
    builder = SupplierBuilder()
    builder.with_company_name(company_name)
    
    if supplier_code := kwargs.get("supplier_code"):
        builder.with_code(supplier_code)
    if trade_name := kwargs.get("trade_name"):
        builder.with_trade_name(trade_name)
    if status := kwargs.get("status"):
        builder.with_status(status)
    if rating := kwargs.get("rating"):
        builder.with_rating(rating)
    if contacts := kwargs.get("contacts"):
        builder.with_contacts(contacts)
    if addresses := kwargs.get("addresses"):
        builder.with_addresses(addresses)
    if tax_id := kwargs.get("tax_id"):
        builder.with_tax_id(tax_id)
    if payment_terms := kwargs.get("payment_terms"):
        builder.with_payment_terms(payment_terms)
    if credit_limit := kwargs.get("credit_limit"):
        builder.with_credit_limit(credit_limit)
    if currency := kwargs.get("currency"):
        builder.with_currency(currency)
    if website := kwargs.get("website"):
        builder.with_website(website)
    if notes := kwargs.get("notes"):
        builder.with_notes(notes)
    if tags := kwargs.get("tags"):
        builder.with_tags(tags)
    if metadata := kwargs.get("metadata"):
        builder.with_metadata(metadata)
    
    return builder.build()
