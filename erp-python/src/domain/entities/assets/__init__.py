"""
Asset Entity for ERP System.

This module provides the Asset entity for managing fixed assets
following Clean Architecture principles.
"""

from dataclasses import dataclass, field
from datetime import datetime, date
from typing import Optional, Dict, Any, List
from enum import Enum
from decimal import Decimal


class AssetStatus(str, Enum):
    """Asset status enumeration."""
    AVAILABLE = "available"
    IN_USE = "in_use"
    MAINTENANCE = "maintenance"
    RETIRED = "retired"
    DISPOSED = "disposed"
    LOST = "lost"


class AssetType(str, Enum):
    """Asset type enumeration."""
    EQUIPMENT = "equipment"
    VEHICLE = "vehicle"
    FURNITURE = "furniture"
    COMPUTER = "computer"
    MACHINERY = "machinery"
    BUILDING = "building"
    LAND = "land"
    OTHER = "other"


class DepreciationMethod(str, Enum):
    """Depreciation method enumeration."""
    STRAIGHT_LINE = "straight_line"
    Declining_BALANCE = "declining_balance"
    SUM_OF_YEARS = "sum_of_years"
    UNITS_OF_PRODUCTION = "units_of_production"


@dataclass(frozen=True)
class AssetDepreciation:
    """
    Value Object representing asset depreciation.
    Immutable and validated.
    """
    id: str
    period: str
    depreciation_amount: Decimal
    accumulated_depreciation: Decimal
    book_value: Decimal
    
    def __post_init__(self):
        if self.depreciation_amount < 0:
            raise ValueError("depreciation_amount cannot be negative")
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "period": self.period,
            "depreciation_amount": str(self.depreciation_amount),
            "accumulated_depreciation": str(self.accumulated_depreciation),
            "book_value": str(self.book_value)
        }


@dataclass(frozen=True)
class Asset:
    """
    Asset entity representing a fixed asset.
    
    This entity follows Clean Architecture principles and is immutable.
    
    Attributes:
        id: Unique identifier for the asset
        asset_code: Human-readable asset code
        name: Asset name
        description: Asset description
        asset_type: Type of asset
        status: Current status
        purchase_date: Purchase date
        purchase_cost: Purchase cost
        salvage_value: Salvage value
        useful_life_years: Useful life in years
        depreciation_method: Depreciation method
        accumulated_depreciation: Accumulated depreciation
        location: Asset location
        assigned_to: User ID assigned to
        assigned_name: User name assigned to
        serial_number: Serial number
        warranty_expiry: Warranty expiry date
        notes: Additional notes
        metadata: Additional metadata
        created_at: Timestamp when created
        updated_at: Timestamp when last updated
    """
    id: str
    asset_code: str
    name: str
    description: str
    asset_type: AssetType
    status: AssetStatus
    purchase_date: date
    purchase_cost: Decimal
    salvage_value: Decimal
    useful_life_years: int
    depreciation_method: DepreciationMethod
    accumulated_depreciation: Decimal = field(default=Decimal("0"))
    location: Optional[str] = None
    assigned_to: Optional[str] = None
    assigned_name: Optional[str] = None
    serial_number: Optional[str] = None
    warranty_expiry: Optional[date] = None
    notes: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime = field(default_factory=datetime.utcnow)
    
    def __post_init__(self):
        """Validate asset after initialization."""
        if not self.asset_code:
            raise ValueError("asset_code cannot be empty")
        if not self.name:
            raise ValueError("name cannot be empty")
        if self.purchase_cost <= 0:
            raise ValueError("purchase_cost must be positive")
        if self.salvage_value < 0:
            raise ValueError("salvage_value cannot be negative")
        if self.useful_life_years <= 0:
            raise ValueError("useful_life_years must be positive")
    
    @property
    def is_in_use(self) -> bool:
        """Check if asset is in use."""
        return self.status == AssetStatus.IN_USE
    
    @property
    def is_available(self) -> bool:
        """Check if asset is available."""
        return self.status == AssetStatus.AVAILABLE
    
    @property
    def current_book_value(self) -> Decimal:
        """Calculate current book value."""
        return self.purchase_cost - self.accumulated_depreciation
    
    @property
    def depreciation_per_year(self) -> Decimal:
        """Calculate annual depreciation (straight-line)."""
        if self.depreciation_method != DepreciationMethod.STRAIGHT_LINE:
            return Decimal("0")
        return (self.purchase_cost - self.salvage_value) / self.useful_life_years
    
    @property
    def age_years(self) -> int:
        """Get asset age in years."""
        today = date.today()
        years = today.year - self.purchase_date.year
        if today.month < self.purchase_date.month or (today.month == self.purchase_date.month and today.day < self.purchase_date.day):
            years -= 1
        return max(0, years)
    
    @property
    def is_fully_depreciated(self) -> bool:
        """Check if asset is fully depreciated."""
        depreciable_amount = self.purchase_cost - self.salvage_value
        return self.accumulated_depreciation >= depreciable_amount
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert asset to dictionary."""
        return {
            "id": self.id,
            "asset_code": self.asset_code,
            "name": self.name,
            "description": self.description,
            "asset_type": self.asset_type.value,
            "status": self.status.value,
            "purchase_date": self.purchase_date.isoformat(),
            "purchase_cost": str(self.purchase_cost),
            "salvage_value": str(self.salvage_value),
            "useful_life_years": self.useful_life_years,
            "depreciation_method": self.depreciation_method.value,
            "accumulated_depreciation": str(self.accumulated_depreciation),
            "current_book_value": str(self.current_book_value),
            "depreciation_per_year": str(self.depreciation_per_year),
            "location": self.location,
            "assigned_to": self.assigned_to,
            "assigned_name": self.assigned_name,
            "serial_number": self.serial_number,
            "warranty_expiry": self.warranty_expiry.isoformat() if self.warranty_expiry else None,
            "notes": self.notes,
            "metadata": self.metadata,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
            "is_in_use": self.is_in_use,
            "is_available": self.is_available,
            "age_years": self.age_years,
            "is_fully_depreciated": self.is_fully_depreciated
        }


class AssetBuilder:
    """Builder for creating Asset instances."""
    
    def __init__(self):
        self._id: Optional[str] = None
        self._asset_code: Optional[str] = None
        self._name: Optional[str] = None
        self._description: str = ""
        self._asset_type: AssetType = AssetType.EQUIPMENT
        self._status: AssetStatus = AssetStatus.AVAILABLE
        self._purchase_date: Optional[date] = None
        self._purchase_cost: Optional[Decimal] = None
        self._salvage_value: Decimal = Decimal("0")
        self._useful_life_years: int = 5
        self._depreciation_method: DepreciationMethod = DepreciationMethod.STRAIGHT_LINE
        self._accumulated_depreciation: Decimal = Decimal("0")
        self._location: Optional[str] = None
        self._assigned_to: Optional[str] = None
        self._assigned_name: Optional[str] = None
        self._serial_number: Optional[str] = None
        self._warranty_expiry: Optional[date] = None
        self._notes: Optional[str] = None
        self._metadata: Dict[str, Any] = {}
    
    def with_id(self, asset_id: str) -> "AssetBuilder":
        self._id = asset_id
        return self
    
    def with_code(self, asset_code: str) -> "AssetBuilder":
        self._asset_code = asset_code
        return self
    
    def with_name(self, name: str) -> "AssetBuilder":
        self._name = name
        return self
    
    def with_description(self, description: str) -> "AssetBuilder":
        self._description = description
        return self
    
    def with_type(self, asset_type: AssetType) -> "AssetBuilder":
        self._asset_type = asset_type
        return self
    
    def with_status(self, status: AssetStatus) -> "AssetBuilder":
        self._status = status
        return self
    
    def purchased_on(self, purchase_date: date) -> "AssetBuilder":
        self._purchase_date = purchase_date
        return self
    
    def with_cost(self, cost: Decimal) -> "AssetBuilder":
        self._purchase_cost = cost
        return self
    
    def with_salvage_value(self, value: Decimal) -> "AssetBuilder":
        self._salvage_value = value
        return self
    
    def with_useful_life(self, years: int) -> "AssetBuilder":
        self._useful_life_years = years
        return self
    
    def with_depreciation_method(self, method: DepreciationMethod) -> "AssetBuilder":
        self._depreciation_method = method
        return self
    
    def with_accumulated_depreciation(self, depreciation: Decimal) -> "AssetBuilder":
        self._accumulated_depreciation = depreciation
        return self
    
    def at_location(self, location: str) -> "AssetBuilder":
        self._location = location
        return self
    
    def assigned_to(self, user_id: str, user_name: str) -> "AssetBuilder":
        self._assigned_to = user_id
        self._assigned_name = user_name
        return self
    
    def with_serial_number(self, serial: str) -> "AssetBuilder":
        self._serial_number = serial
        return self
    
    def with_warranty_expiry(self, expiry: date) -> "AssetBuilder":
        self._warranty_expiry = expiry
        return self
    
    def with_notes(self, notes: str) -> "AssetBuilder":
        self._notes = notes
        return self
    
    def with_metadata(self, metadata: Dict[str, Any]) -> "AssetBuilder":
        self._metadata = metadata
        return self
    
    def build(self) -> Asset:
        from uuid import uuid4
        
        if not self._id:
            self._id = str(uuid4())
        if not self._asset_code:
            from time import time
            self._asset_code = f"AST-{int(time())}"
        if not self._name:
            raise ValueError("name is required")
        if not self._purchase_date:
            raise ValueError("purchase_date is required")
        if not self._purchase_cost:
            raise ValueError("purchase_cost is required")
        
        return Asset(
            id=self._id,
            asset_code=self._asset_code,
            name=self._name,
            description=self._description,
            asset_type=self._asset_type,
            status=self._status,
            purchase_date=self._purchase_date,
            purchase_cost=self._purchase_cost,
            salvage_value=self._salvage_value,
            useful_life_years=self._useful_life_years,
            depreciation_method=self._depreciation_method,
            accumulated_depreciation=self._accumulated_depreciation,
            location=self._location,
            assigned_to=self._assigned_to,
            assigned_name=self._assigned_name,
            serial_number=self._serial_number,
            warranty_expiry=self._warranty_expiry,
            notes=self._notes,
            metadata=self._metadata
        )


# Factory function
def create_asset(
    name: str,
    purchase_date: date,
    purchase_cost: Decimal,
    **kwargs
) -> Asset:
    """Factory function to create an asset."""
    builder = AssetBuilder()
    builder.with_name(name)
    builder.purchased_on(purchase_date)
    builder.with_cost(purchase_cost)
    
    if asset_code := kwargs.get("asset_code"):
        builder.with_code(asset_code)
    if description := kwargs.get("description"):
        builder.with_description(description)
    if asset_type := kwargs.get("asset_type"):
        builder.with_type(asset_type)
    if status := kwargs.get("status"):
        builder.with_status(status)
    if salvage_value := kwargs.get("salvage_value"):
        builder.with_salvage_value(salvage_value)
    if useful_life := kwargs.get("useful_life_years"):
        builder.with_useful_life(useful_life)
    if depreciation_method := kwargs.get("depreciation_method"):
        builder.with_depreciation_method(depreciation_method)
    if location := kwargs.get("location"):
        builder.at_location(location)
    if assigned_to := kwargs.get("assigned_to"):
        assigned_name = kwargs.get("assigned_name", "")
        builder.assigned_to(assigned_to, assigned_name)
    if serial_number := kwargs.get("serial_number"):
        builder.with_serial_number(serial_number)
    if warranty_expiry := kwargs.get("warranty_expiry"):
        builder.with_warranty_expiry(warranty_expiry)
    if notes := kwargs.get("notes"):
        builder.with_notes(notes)
    if metadata := kwargs.get("metadata"):
        builder.with_metadata(metadata)
    
    return builder.build()
