"""
Inventory Entity for ERP System.

This module provides entities for inventory and stock management
following Clean Architecture principles.
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional, Dict, Any, List
from enum import Enum
from uuid import uuid4
from decimal import Decimal


class StockMovementType(str, Enum):
    """Stock movement type enumeration."""
    PURCHASE = "purchase"
    SALE = "sale"
    RETURN = "return"
    ADJUSTMENT = "adjustment"
    TRANSFER = "transfer"
    DAMAGE = "damage"
    THEFT = "theft"
    EXPIRY = "expiry"


class StockStatus(str, Enum):
    """Stock status enumeration."""
    IN_STOCK = "in_stock"
    LOW_STOCK = "low_stock"
    OUT_OF_STOCK = "out_of_stock"
    ON_ORDER = "on_order"
    DISCONTINUED = "discontinued"


class ReorderLevel(str, Enum):
    """Reorder level type enumeration."""
    FIXED = "fixed"
    DYNAMIC = "dynamic"
    MANUAL = "manual"


@dataclass(frozen=True)
class StockLevel:
    """
    Value Object representing stock level at a location.
    Immutable and validated.
    """
    warehouse_id: str
    warehouse_name: str
    quantity: int
    reserved_quantity: int = 0
    available_quantity: int = 0
    reorder_point: int = 0
    reorder_quantity: int = 0
    
    def __post_init__(self):
        if self.quantity < 0:
            raise ValueError("quantity cannot be negative")
        if self.reserved_quantity < 0:
            raise ValueError("reserved_quantity cannot be negative")
    
    @property
    def available(self) -> int:
        return max(0, self.quantity - self.reserved_quantity)
    
    @property
    def is_below_reorder(self) -> bool:
        return self.quantity <= self.reorder_point
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "warehouse_id": self.warehouse_id,
            "warehouse_name": self.warehouse_name,
            "quantity": self.quantity,
            "reserved_quantity": self.reserved_quantity,
            "available_quantity": self.available,
            "reorder_point": self.reorder_point,
            "reorder_quantity": self.reorder_quantity,
            "is_below_reorder": self.is_below_reorder
        }


@dataclass(frozen=True)
class StockMovement:
    """
    Value Object representing a stock movement.
    Immutable and validated.
    """
    id: str
    product_id: str
    product_name: str
    movement_type: StockMovementType
    quantity: int
    unit_cost: Decimal
    total_cost: Decimal
    reference_number: str
    notes: str
    performed_by: str
    performed_at: datetime
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "product_id": self.product_id,
            "product_name": self.product_name,
            "movement_type": self.movement_type.value,
            "quantity": self.quantity,
            "unit_cost": str(self.unit_cost),
            "total_cost": str(self.total_cost),
            "reference_number": self.reference_number,
            "notes": self.notes,
            "performed_by": self.performed_by,
            "performed_at": self.performed_at.isoformat()
        }


@dataclass(frozen=True)
class InventoryItem:
    """
    Inventory Item entity for tracking stock.
    
    This entity follows Clean Architecture principles and is immutable.
    
    Attributes:
        id: Unique identifier
        product_id: Product identifier
        product_sku: Product SKU
        product_name: Product name
        status: Current stock status
        stock_levels: Stock levels by warehouse
        total_quantity: Total stock across all warehouses
        reserved_quantity: Total reserved
        available_quantity: Total available
        reorder_level_type: Type of reorder level
        reorder_point: Reorder point
        reorder_quantity: Default reorder quantity
        lead_time_days: Supplier lead time
        last_restocked: Last restock date
        average_daily_usage: Average daily usage
        turnover_rate: Stock turnover rate
        movements: Stock movement history
        metadata: Additional metadata
        created_at: Creation timestamp
        updated_at: Last update timestamp
    """
    id: str
    product_id: str
    product_sku: str
    product_name: str
    status: StockStatus
    stock_levels: List[StockLevel] = field(default_factory=list)
    total_quantity: int = 0
    reserved_quantity: int = 0
    available_quantity: int = 0
    reorder_level_type: ReorderLevel = ReorderLevel.FIXED
    reorder_point: int = 0
    reorder_quantity: int = 0
    lead_time_days: int = 0
    last_restocked: Optional[datetime] = None
    average_daily_usage: Decimal = field(default=Decimal("0"))
    turnover_rate: Decimal = field(default=Decimal("0"))
    movements: List[StockMovement] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime = field(default_factory=datetime.utcnow)
    
    def __post_init__(self):
        if not self.product_id:
            raise ValueError("product_id cannot be empty")
        if not self.product_sku:
            raise ValueError("product_sku cannot be empty")
    
    @property
    def is_in_stock(self) -> bool:
        return self.status == StockStatus.IN_STOCK
    
    @property
    def is_low_stock(self) -> bool:
        return self.status == StockStatus.LOW_STOCK
    
    @property
    def is_out_of_stock(self) -> bool:
        return self.status == StockStatus.OUT_OF_STOCK
    
    @property
    def needs_reorder(self) -> bool:
        return self.total_quantity <= self.reorder_point
    
    @property
    def days_of_stock(self) -> int:
        if self.average_daily_usage == 0:
            return 999
        return int(self.available_quantity / self.average_daily_usage)
    
    def calculate_totals(self) -> None:
        """Calculate total quantities from stock levels."""
        self.total_quantity = sum(sl.quantity for sl in self.stock_levels)
        self.reserved_quantity = sum(sl.reserved_quantity for sl in self.stock_levels)
        self.available_quantity = sum(sl.available for sl in self.stock_levels)
        
        if self.available_quantity <= 0:
            self.status = StockStatus.OUT_OF_STOCK
        elif self.available_quantity <= self.reorder_point:
            self.status = StockStatus.LOW_STOCK
        else:
            self.status = StockStatus.IN_STOCK
    
    def add_movement(self, movement: StockMovement) -> None:
        """Add a stock movement and update quantities."""
        self.movements.append(movement)
        
        if movement.movement_type in [StockMovementType.PURCHASE, StockMovementType.RETURN]:
            self.total_quantity += movement.quantity
        elif movement.movement_type == StockMovementType.SALE:
            self.total_quantity -= movement.quantity
            self.reserved_quantity -= movement.quantity
        
        self.last_restocked = movement.performed_at
        self.calculate_totals()
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "product_id": self.product_id,
            "product_sku": self.product_sku,
            "product_name": self.product_name,
            "status": self.status.value,
            "stock_levels": [sl.to_dict() for sl in self.stock_levels],
            "total_quantity": self.total_quantity,
            "reserved_quantity": self.reserved_quantity,
            "available_quantity": self.available_quantity,
            "reorder_level_type": self.reorder_level_type.value,
            "reorder_point": self.reorder_point,
            "reorder_quantity": self.reorder_quantity,
            "lead_time_days": self.lead_time_days,
            "last_restocked": self.last_restocked.isoformat() if self.last_restocked else None,
            "average_daily_usage": str(self.average_daily_usage),
            "turnover_rate": str(self.turnover_rate),
            "movements": [m.to_dict() for m in self.movements],
            "metadata": self.metadata,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
            "is_in_stock": self.is_in_stock,
            "is_low_stock": self.is_low_stock,
            "is_out_of_stock": self.is_out_of_stock,
            "needs_reorder": self.needs_reorder,
            "days_of_stock": self.days_of_stock
        }


class InventoryBuilder:
    """Builder for creating InventoryItem instances."""
    
    def __init__(self):
        self._id: Optional[str] = None
        self._product_id: Optional[str] = None
        self._product_sku: Optional[str] = None
        self._product_name: str = ""
        self._status: StockStatus = StockStatus.IN_STOCK
        self._stock_levels: List[StockLevel] = []
        self._reorder_level_type: ReorderLevel = ReorderLevel.FIXED
        self._reorder_point: int = 0
        self._reorder_quantity: int = 0
        self._lead_time_days: int = 0
        self._last_restocked: Optional[datetime] = None
        self._average_daily_usage: Decimal = Decimal("0")
        self._turnover_rate: Decimal = Decimal("0")
        self._movements: List[StockMovement] = []
        self._metadata: Dict[str, Any] = {}
    
    def with_id(self, item_id: str) -> "InventoryBuilder":
        self._id = item_id
        return self
    
    def for_product(self, product_id: str, product_sku: str, product_name: str) -> "InventoryBuilder":
        self._product_id = product_id
        self._product_sku = product_sku
        self._product_name = product_name
        return self
    
    def with_status(self, status: StockStatus) -> "InventoryBuilder":
        self._status = status
        return self
    
    def with_stock_levels(self, levels: List[StockLevel]) -> "InventoryBuilder":
        self._stock_levels = levels
        return self
    
    def with_reorder_settings(self, point: int, quantity: int, level_type: ReorderLevel = ReorderLevel.FIXED) -> "InventoryBuilder":
        self._reorder_point = point
        self._reorder_quantity = quantity
        self._reorder_level_type = level_type
        return self
    
    def with_lead_time(self, days: int) -> "InventoryBuilder":
        self._lead_time_days = days
        return self
    
    def with_usage(self, daily: Decimal, turnover: Decimal) -> "InventoryBuilder":
        self._average_daily_usage = daily
        self._turnover_rate = turnover
        return self
    
    def with_movements(self, movements: List[StockMovement]) -> "InventoryBuilder":
        self._movements = movements
        return self
    
    def with_metadata(self, metadata: Dict[str, Any]) -> "InventoryBuilder":
        self._metadata = metadata
        return self
    
    def build(self) -> InventoryItem:
        if not self._id:
            self._id = str(uuid4())
        if not self._product_id:
            raise ValueError("product_id is required")
        if not self._product_sku:
            raise ValueError("product_sku is required")
        
        item = InventoryItem(
            id=self._id,
            product_id=self._product_id,
            product_sku=self._product_sku,
            product_name=self._product_name,
            status=self._status,
            stock_levels=self._stock_levels,
            reorder_level_type=self._reorder_level_type,
            reorder_point=self._reorder_point,
            reorder_quantity=self._reorder_quantity,
            lead_time_days=self._lead_time_days,
            last_restocked=self._last_restocked,
            average_daily_usage=self._average_daily_usage,
            turnover_rate=self._turnover_rate,
            movements=self._movements,
            metadata=self._metadata
        )
        
        item.calculate_totals()
        return item


def create_inventory_item(
    product_id: str,
    product_sku: str,
    product_name: str,
    **kwargs
) -> InventoryItem:
    """Factory function to create an inventory item."""
    builder = InventoryBuilder()
    builder.for_product(product_id, product_sku, product_name)
    
    if reorder_point := kwargs.get("reorder_point"):
        reorder_quantity = kwargs.get("reorder_quantity", 10)
        level_type = kwargs.get("reorder_level_type", ReorderLevel.FIXED)
        builder.with_reorder_settings(reorder_point, reorder_quantity, level_type)
    
    if lead_time_days := kwargs.get("lead_time_days"):
        builder.with_lead_time(lead_time_days)
    
    if average_daily_usage := kwargs.get("average_daily_usage"):
        turnover_rate = kwargs.get("turnover_rate", Decimal("0"))
        builder.with_usage(average_daily_usage, turnover_rate)
    
    if metadata := kwargs.get("metadata"):
        builder.with_metadata(metadata)
    
    return builder.build()


def create_stock_level(
    warehouse_id: str,
    warehouse_name: str,
    quantity: int,
    **kwargs
) -> StockLevel:
    """Factory function to create a stock level."""
    return StockLevel(
        warehouse_id=warehouse_id,
        warehouse_name=warehouse_name,
        quantity=quantity,
        reserved_quantity=kwargs.get("reserved_quantity", 0),
        reorder_point=kwargs.get("reorder_point", 0),
        reorder_quantity=kwargs.get("reorder_quantity", 0)
    )


def create_stock_movement(
    product_id: str,
    product_name: str,
    movement_type: StockMovementType,
    quantity: int,
    unit_cost: Decimal,
    reference_number: str,
    performed_by: str,
    **kwargs
) -> StockMovement:
    """Factory function to create a stock movement."""
    return StockMovement(
        id=str(uuid4()),
        product_id=product_id,
        product_name=product_name,
        movement_type=movement_type,
        quantity=quantity,
        unit_cost=unit_cost,
        total_cost=unit_cost * quantity,
        reference_number=reference_number,
        notes=kwargs.get("notes", ""),
        performed_by=performed_by,
        performed_at=kwargs.get("performed_at", datetime.utcnow())
    )
