"""
Warehouse Entity for ERP System.

This module provides the Warehouse entity for managing warehouses
following Clean Architecture principles.
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional, Dict, Any, List
from enum import Enum
from decimal import Decimal


class WarehouseStatus(str, Enum):
    """Warehouse status enumeration."""
    ACTIVE = "active"
    INACTIVE = "inactive"
    MAINTENANCE = "maintenance"
    CLOSED = "closed"


class ZoneType(str, Enum):
    """Warehouse zone type enumeration."""
    STORAGE = "storage"
    RECEIVING = "receiving"
    SHIPPING = "shipping"
    RETURN = "return"
    QUARANTINE = "quarantine"
    BULK = "bulk"
    PICKING = "picking"


class ZoneStatus(str, Enum):
    """Warehouse zone status enumeration."""
    AVAILABLE = "available"
    FULL = "full"
    MAINTENANCE = "maintenance"
    UNAVAILABLE = "unavailable"


@dataclass(frozen=True)
class WarehouseZone:
    """
    Value Object representing a zone within a warehouse.
    Immutable and validated.
    """
    id: str
    name: str
    zone_type: ZoneType
    status: ZoneStatus
    capacity: int
    current_capacity: int = 0
    location_code: Optional[str] = None
    temperature_controlled: bool = False
    min_temperature: Optional[Decimal] = None
    max_temperature: Optional[Decimal] = None
    
    def __post_init__(self):
        if not self.name:
            raise ValueError("zone name cannot be empty")
        if self.capacity <= 0:
            raise ValueError("capacity must be positive")
        if self.current_capacity < 0:
            raise ValueError("current_capacity cannot be negative")
        if self.current_capacity > self.capacity:
            raise ValueError("current_capacity cannot exceed capacity")
        if self.temperature_controlled:
            if self.min_temperature is None or self.max_temperature is None:
                raise ValueError("temperature range required for temperature controlled zones")
    
    @property
    def available_capacity(self) -> int:
        """Get available capacity."""
        return self.capacity - self.current_capacity
    
    @property
    def utilization_percent(self) -> Decimal:
        """Get utilization percentage."""
        if self.capacity == 0:
            return Decimal("0")
        return Decimal(self.current_capacity) / Decimal(self.capacity) * 100
    
    @property
    def is_full(self) -> bool:
        """Check if zone is full."""
        return self.current_capacity >= self.capacity
    
    @property
    def is_available(self) -> bool:
        """Check if zone is available."""
        return self.status == ZoneStatus.AVAILABLE and not self.is_full
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "name": self.name,
            "zone_type": self.zone_type.value,
            "status": self.status.value,
            "capacity": self.capacity,
            "current_capacity": self.current_capacity,
            "available_capacity": self.available_capacity,
            "location_code": self.location_code,
            "temperature_controlled": self.temperature_controlled,
            "min_temperature": str(self.min_temperature) if self.min_temperature else None,
            "max_temperature": str(self.max_temperature) if self.max_temperature else None,
            "utilization_percent": str(self.utilization_percent),
            "is_full": self.is_full,
            "is_available": self.is_available
        }


@dataclass(frozen=True)
class Warehouse:
    """
    Warehouse entity representing a storage facility in the ERP system.
    
    This entity follows Clean Architecture principles and is immutable.
    
    Attributes:
        id: Unique identifier for the warehouse
        warehouse_code: Human-readable warehouse code
        name: Warehouse name
        status: Current status of the warehouse
        address: Warehouse address
        zones: List of zones within the warehouse
        manager_id: ID of warehouse manager
        manager_name: Name of warehouse manager
        total_capacity: Total storage capacity
        used_capacity: Currently used capacity
        default_currency: Default currency
        is_primary: Whether this is the primary warehouse
        notes: Additional notes
        metadata: Additional metadata
        created_at: Timestamp when created
        updated_at: Timestamp when last updated
    """
    id: str
    warehouse_code: str
    name: str
    status: WarehouseStatus
    address: str
    zones: List[WarehouseZone] = field(default_factory=list)
    manager_id: Optional[str] = None
    manager_name: Optional[str] = None
    total_capacity: int = 0
    used_capacity: int = 0
    default_currency: str = "USD"
    is_primary: bool = False
    notes: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime = field(default_factory=datetime.utcnow)
    
    def __post_init__(self):
        """Validate warehouse after initialization."""
        if not self.warehouse_code:
            raise ValueError("warehouse_code cannot be empty")
        if not self.name:
            raise ValueError("name cannot be empty")
        if not self.address:
            raise ValueError("address cannot be empty")
        if self.total_capacity < 0:
            raise ValueError("total_capacity cannot be negative")
        if self.used_capacity < 0:
            raise ValueError("used_capacity cannot be negative")
        if self.used_capacity > self.total_capacity:
            raise ValueError("used_capacity cannot exceed total_capacity")
    
    @property
    def is_active(self) -> bool:
        """Check if warehouse is active."""
        return self.status == WarehouseStatus.ACTIVE
    
    @property
    def available_capacity(self) -> int:
        """Get available capacity."""
        return self.total_capacity - self.used_capacity
    
    @property
    def utilization_percent(self) -> Decimal:
        """Get utilization percentage."""
        if self.total_capacity == 0:
            return Decimal("0")
        return Decimal(self.used_capacity) / Decimal(self.total_capacity) * 100
    
    @property
    def is_full(self) -> bool:
        """Check if warehouse is full."""
        return self.used_capacity >= self.total_capacity
    
    @property
    def zone_count(self) -> int:
        """Get number of zones."""
        return len(self.zones)
    
    @property
    def active_zone_count(self) -> int:
        """Get number of active zones."""
        return sum(1 for z in self.zones if z.status == ZoneStatus.AVAILABLE)
    
    def can_accommodate(self, quantity: int) -> bool:
        """Check if warehouse can accommodate given quantity."""
        return self.is_active and self.available_capacity >= quantity
    
    def get_zone_by_type(self, zone_type: ZoneType) -> Optional[WarehouseZone]:
        """Get a zone by its type."""
        for zone in self.zones:
            if zone.zone_type == zone_type:
                return zone
        return None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert warehouse to dictionary."""
        return {
            "id": self.id,
            "warehouse_code": self.warehouse_code,
            "name": self.name,
            "status": self.status.value,
            "address": self.address,
            "zones": [z.to_dict() for z in self.zones],
            "manager_id": self.manager_id,
            "manager_name": self.manager_name,
            "total_capacity": self.total_capacity,
            "used_capacity": self.used_capacity,
            "available_capacity": self.available_capacity,
            "utilization_percent": str(self.utilization_percent),
            "default_currency": self.default_currency,
            "is_primary": self.is_primary,
            "notes": self.notes,
            "metadata": self.metadata,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
            "is_active": self.is_active,
            "is_full": self.is_full,
            "zone_count": self.zone_count,
            "active_zone_count": self.active_zone_count
        }


class WarehouseBuilder:
    """Builder for creating Warehouse instances."""
    
    def __init__(self):
        self._id: Optional[str] = None
        self._warehouse_code: Optional[str] = None
        self._name: Optional[str] = None
        self._status: WarehouseStatus = WarehouseStatus.ACTIVE
        self._address: Optional[str] = None
        self._zones: List[WarehouseZone] = []
        self._manager_id: Optional[str] = None
        self._manager_name: Optional[str] = None
        self._total_capacity: int = 0
        self._used_capacity: int = 0
        self._default_currency: str = "USD"
        self._is_primary: bool = False
        self._notes: Optional[str] = None
        self._metadata: Dict[str, Any] = {}
    
    def with_id(self, warehouse_id: str) -> "WarehouseBuilder":
        self._id = warehouse_id
        return self
    
    def with_code(self, warehouse_code: str) -> "WarehouseBuilder":
        self._warehouse_code = warehouse_code
        return self
    
    def with_name(self, name: str) -> "WarehouseBuilder":
        self._name = name
        return self
    
    def with_status(self, status: WarehouseStatus) -> "WarehouseBuilder":
        self._status = status
        return self
    
    def at_address(self, address: str) -> "WarehouseBuilder":
        self._address = address
        return self
    
    def with_zones(self, zones: List[WarehouseZone]) -> "WarehouseBuilder":
        self._zones = zones
        return self
    
    def add_zone(self, zone: WarehouseZone) -> "WarehouseBuilder":
        self._zones.append(zone)
        return self
    
    def with_manager(self, manager_id: str, manager_name: str) -> "WarehouseBuilder":
        self._manager_id = manager_id
        self._manager_name = manager_name
        return self
    
    def with_capacity(self, total: int, used: int = 0) -> "WarehouseBuilder":
        self._total_capacity = total
        self._used_capacity = used
        return self
    
    def with_currency(self, currency: str) -> "WarehouseBuilder":
        self._default_currency = currency
        return self
    
    def as_primary(self, is_primary: bool = True) -> "WarehouseBuilder":
        self._is_primary = is_primary
        return self
    
    def with_notes(self, notes: str) -> "WarehouseBuilder":
        self._notes = notes
        return self
    
    def with_metadata(self, metadata: Dict[str, Any]) -> "WarehouseBuilder":
        self._metadata = metadata
        return self
    
    def build(self) -> Warehouse:
        from uuid import uuid4
        
        if not self._id:
            self._id = str(uuid4())
        if not self._warehouse_code:
            from time import time
            self._warehouse_code = f"WH-{int(time())}"
        if not self._name:
            raise ValueError("name is required")
        if not self._address:
            raise ValueError("address is required")
        
        return Warehouse(
            id=self._id,
            warehouse_code=self._warehouse_code,
            name=self._name,
            status=self._status,
            address=self._address,
            zones=self._zones,
            manager_id=self._manager_id,
            manager_name=self._manager_name,
            total_capacity=self._total_capacity,
            used_capacity=self._used_capacity,
            default_currency=self._default_currency,
            is_primary=self._is_primary,
            notes=self._notes,
            metadata=self._metadata
        )


# Factory functions
def create_warehouse_zone(
    name: str,
    zone_type: ZoneType,
    capacity: int,
    **kwargs
) -> WarehouseZone:
    """Factory function to create a warehouse zone."""
    from uuid import uuid4
    
    return WarehouseZone(
        id=str(uuid4()),
        name=name,
        zone_type=zone_type,
        status=kwargs.get("status", ZoneStatus.AVAILABLE),
        capacity=capacity,
        current_capacity=kwargs.get("current_capacity", 0),
        location_code=kwargs.get("location_code"),
        temperature_controlled=kwargs.get("temperature_controlled", False),
        min_temperature=kwargs.get("min_temperature"),
        max_temperature=kwargs.get("max_temperature")
    )


def create_warehouse(
    name: str,
    address: str,
    **kwargs
) -> Warehouse:
    """Factory function to create a warehouse."""
    builder = WarehouseBuilder()
    builder.with_name(name)
    builder.at_address(address)
    
    if warehouse_code := kwargs.get("warehouse_code"):
        builder.with_code(warehouse_code)
    if status := kwargs.get("status"):
        builder.with_status(status)
    if zones := kwargs.get("zones"):
        builder.with_zones(zones)
    if manager_id := kwargs.get("manager_id"):
        manager_name = kwargs.get("manager_name", "")
        builder.with_manager(manager_id, manager_name)
    if capacity := kwargs.get("total_capacity"):
        used = kwargs.get("used_capacity", 0)
        builder.with_capacity(capacity, used)
    if currency := kwargs.get("default_currency"):
        builder.with_currency(currency)
    if is_primary := kwargs.get("is_primary"):
        builder.as_primary(is_primary)
    if notes := kwargs.get("notes"):
        builder.with_notes(notes)
    if metadata := kwargs.get("metadata"):
        builder.with_metadata(metadata)
    
    return builder.build()
