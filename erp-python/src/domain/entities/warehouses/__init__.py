"""
Warehouse Entity - Domain Layer
Represents warehouses in the ERP system.

Author: Alexandre Albert Ndour
"""

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Optional
import uuid


@dataclass
class Warehouse:
    """
    Warehouse Entity.
    
    Represents a warehouse or storage location.
    """
    
    # Identity
    id: uuid.UUID = field(default_factory=uuid.uuid4)
    code: str = ""
    name: str = ""
    
    # Address
    address: str = ""
    city: str = ""
    state: Optional[str] = None
    postal_code: str = ""
    country: str = ""
    
    # Contact
    contact_name: Optional[str] = None
    contact_phone: Optional[str] = None
    contact_email: Optional[str] = None
    
    # Status
    is_active: bool = True
    is_primary: bool = False
    
    # Capacity
    capacity: Optional[int] = None  # in units
    current_stock: int = 0
    
    # Notes
    notes: Optional[str] = None
    
    # Metadata
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    
    def activate(self) -> None:
        self.is_active = True
        self.updated_at = datetime.now(timezone.utc)
    
    def deactivate(self) -> None:
        self.is_active = False
        self.updated_at = datetime.now(timezone.utc)
    
    @classmethod
    def create(
        cls,
        code: str,
        name: str,
        address: str,
        city: str,
        country: str
    ) -> "Warehouse":
        return cls(code=code, name=name, address=address, city=city, country=country)
    
    def to_dict(self) -> dict:
        return {
            "id": str(self.id),
            "code": self.code,
            "name": self.name,
            "address": self.address,
            "city": self.city,
            "country": self.country,
            "is_active": self.is_active,
            "is_primary": self.is_primary,
            "capacity": self.capacity,
            "current_stock": self.current_stock,
        }


@dataclass
class WarehouseZone:
    """Warehouse zone within a warehouse."""
    
    id: uuid.UUID = field(default_factory=uuid.uuid4)
    warehouse_id: uuid.UUID = None  # type: ignore
    
    name: str = ""
    zone_type: str = "storage"  # storage, picking, shipping, receiving
    
    is_active: bool = True
    
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    
    def to_dict(self) -> dict:
        return {
            "id": str(self.id),
            "warehouse_id": str(self.warehouse_id),
            "name": self.name,
            "zone_type": self.zone_type,
            "is_active": self.is_active,
        }
