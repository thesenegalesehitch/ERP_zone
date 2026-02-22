"""
Supplier Entity - Domain Layer
Represents suppliers/vendors in the ERP system.

Author: Alexandre Albert Ndour
"""

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Optional, List
from enum import Enum
import uuid


class SupplierStatus(str, Enum):
    """Supplier status enumeration."""
    PROSPECT = "prospect"
    ACTIVE = "active"
    INACTIVE = "inactive"
    BLOCKED = "blocked"


@dataclass
class Supplier:
    """
    Supplier Entity.
    
    Represents a supplier or vendor.
    """
    
    # Identity
    id: uuid.UUID = field(default_factory=uuid.uuid4)
    supplier_number: str = ""
    
    # Status
    status: SupplierStatus = SupplierStatus.PROSPECT
    
    # Company info
    company_name: str = ""
    registration_number: Optional[str] = None
    tax_id: Optional[str] = None
    
    # Contact
    email: str = ""
    phone: Optional[str] = None
    website: Optional[str] = None
    
    # Classification
    supplier_type: Optional[str] = None  # manufacturer, distributor, wholesaler
    category: Optional[str] = None
    
    # Payment terms
    payment_terms: Optional[str] = None  # Net 30, Net 60, etc.
    credit_limit: float = 0.0
    
    # Notes
    notes: Optional[str] = None
    
    # Metadata
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    created_by: Optional[uuid.UUID] = None
    
    # Contacts
    _contacts: List["SupplierContact"] = field(default_factory=list, repr=False)
    _addresses: List["SupplierAddress"] = field(default_factory=list, repr=False)
    
    # ==================== Business Methods ====================
    
    def activate(self) -> None:
        """Activate the supplier."""
        self.status = SupplierStatus.ACTIVE
        self.updated_at = datetime.now(timezone.utc)
    
    def deactivate(self) -> None:
        """Deactivate the supplier."""
        self.status = SupplierStatus.INACTIVE
        self.updated_at = datetime.now(timezone.utc)
    
    def block(self, reason: str = None) -> None:
        """Block the supplier."""
        self.status = SupplierStatus.BLOCKED
        self.notes = reason
        self.updated_at = datetime.now(timezone.utc)
    
    def add_contact(self, contact: "SupplierContact") -> None:
        """Add a contact."""
        contact.supplier_id = self.id
        self._contacts.append(contact)
        self.updated_at = datetime.now(timezone.utc)
    
    def add_address(self, address: "SupplierAddress") -> None:
        """Add an address."""
        address.supplier_id = self.id
        self._addresses.append(address)
        self.updated_at = datetime.now(timezone.utc)
    
    # ==================== Properties ====================
    
    @property
    def is_active(self) -> bool:
        """Check if supplier is active."""
        return self.status == SupplierStatus.ACTIVE
    
    @property
    def contacts(self) -> List["SupplierContact"]:
        return self._contacts.copy()
    
    @property
    def addresses(self) -> List["SupplierAddress"]:
        return self._addresses.copy()
    
    # ==================== Factory Methods ====================
    
    @classmethod
    def create(
        cls,
        company_name: str,
        email: str,
        created_by: uuid.UUID = None
    ) -> "Supplier":
        """Factory method to create a supplier."""
        supplier_number = cls._generate_supplier_number()
        
        return cls(
            supplier_number=supplier_number,
            company_name=company_name,
            email=email,
            created_by=created_by
        )
    
    @classmethod
    def _generate_supplier_number(cls) -> str:
        """Generate supplier number."""
        return f"SUP-{uuid.uuid4().hex[:8].upper()}"
    
    def to_dict(self) -> dict:
        return {
            "id": str(self.id),
            "supplier_number": self.supplier_number,
            "status": self.status.value,
            "company_name": self.company_name,
            "registration_number": self.registration_number,
            "tax_id": self.tax_id,
            "email": self.email,
            "phone": self.phone,
            "website": self.website,
            "supplier_type": self.supplier_type,
            "category": self.category,
            "payment_terms": self.payment_terms,
            "credit_limit": self.credit_limit,
            "is_active": self.is_active,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
        }


@dataclass
class SupplierContact:
    """Supplier contact person."""
    
    id: uuid.UUID = field(default_factory=uuid.uuid4)
    supplier_id: uuid.UUID = None  # type: ignore
    
    name: str = ""
    email: str = ""
    phone: Optional[str] = None
    role: Optional[str] = None
    
    is_primary: bool = False
    
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    
    def to_dict(self) -> dict:
        return {
            "id": str(self.id),
            "supplier_id": str(self.supplier_id),
            "name": self.name,
            "email": self.email,
            "phone": self.phone,
            "role": self.role,
            "is_primary": self.is_primary,
        }


@dataclass
class SupplierAddress:
    """Supplier address."""
    
    id: uuid.UUID = field(default_factory=uuid.uuid4)
    supplier_id: uuid.UUID = None  # type: ignore
    
    address_type: str = "shipping"
    is_primary: bool = False
    
    line1: str = ""
    line2: Optional[str] = None
    city: str = ""
    state: Optional[str] = None
    postal_code: str = ""
    country: str = ""
    
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    
    def to_dict(self) -> dict:
        return {
            "id": str(self.id),
            "supplier_id": str(self.supplier_id),
            "address_type": self.address_type,
            "is_primary": self.is_primary,
            "line1": self.line1,
            "city": self.city,
            "postal_code": self.postal_code,
            "country": self.country,
        }
