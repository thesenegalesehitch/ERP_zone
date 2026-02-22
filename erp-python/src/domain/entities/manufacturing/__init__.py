"""
Manufacturing Entity for ERP System.

This module provides the Manufacturing entity for managing manufacturing
following Clean Architecture principles.
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional, Dict, Any, List
from enum import Enum
from decimal import Decimal


class BillOfMaterialsStatus(str, Enum):
    """Bill of Materials status enumeration."""
    DRAFT = "draft"
    ACTIVE = "active"
    OBSOLETE = "obsolete"


class WorkOrderStatus(str, Enum):
    """Work Order status enumeration."""
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    CANCELLED = "cancelled"
    ON_HOLD = "on_hold"


@dataclass(frozen=True)
class BOMItem:
    """
    Value Object representing a Bill of Materials item.
    Immutable and validated.
    """
    id: str
    component_id: str
    component_name: str
    quantity: Decimal
    unit: str = "pcs"
    scrap_percent: Decimal = field(default=Decimal("0"))
    notes: Optional[str] = None
    
    def __post_init__(self):
        if self.quantity <= 0:
            raise ValueError("quantity must be positive")
        if self.scrap_percent < 0 or self.scrap_percent > 100:
            raise ValueError("scrap_percent must be between 0 and 100")
    
    @property
    def effective_quantity(self) -> Decimal:
        """Calculate effective quantity with scrap."""
        return self.quantity * (1 + self.scrap_percent / 100)
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "component_id": self.component_id,
            "component_name": self.component_name,
            "quantity": str(self.quantity),
            "unit": self.unit,
            "scrap_percent": str(self.scrap_percent),
            "effective_quantity": str(self.effective_quantity),
            "notes": self.notes
        }


@dataclass(frozen=True)
class BillOfMaterials:
    """
    BillOfMaterials entity representing a BOM.
    
    This entity follows Clean Architecture principles and is immutable.
    
    Attributes:
        id: Unique identifier for the BOM
        bom_code: Human-readable BOM code
        name: BOM name
        product_id: Finished product ID
        product_name: Finished product name
        status: Current status
        quantity: Production quantity
        items: List of BOM items
        notes: Additional notes
        metadata: Additional metadata
        created_at: Timestamp when created
        updated_at: Timestamp when last updated
    """
    id: str
    bom_code: str
    name: str
    product_id: str
    product_name: str
    status: BillOfMaterialsStatus
    quantity: Decimal
    items: List[BOMItem] = field(default_factory=list)
    notes: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime = field(default_factory=datetime.utcnow)
    
    def __post_init__(self):
        """Validate BOM after initialization."""
        if not self.bom_code:
            raise ValueError("bom_code cannot be empty")
        if not self.name:
            raise ValueError("name cannot be empty")
        if not self.product_id:
            raise ValueError("product_id cannot be empty")
        if self.quantity <= 0:
            raise ValueError("quantity must be positive")
    
    @property
    def is_active(self) -> bool:
        """Check if BOM is active."""
        return self.status == BillOfMaterialsStatus.ACTIVE
    
    @property
    def item_count(self) -> int:
        """Get number of items."""
        return len(self.items)
    
    @property
    def total_components(self) -> int:
        """Get total number of components."""
        return sum(1 for _ in self.items)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert BOM to dictionary."""
        return {
            "id": self.id,
            "bom_code": self.bom_code,
            "name": self.name,
            "product_id": self.product_id,
            "product_name": self.product_name,
            "status": self.status.value,
            "quantity": str(self.quantity),
            "items": [i.to_dict() for i in self.items],
            "notes": self.notes,
            "metadata": self.metadata,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
            "is_active": self.is_active,
            "item_count": self.item_count,
            "total_components": self.total_components
        }


@dataclass(frozen=True)
class WorkOrder:
    """
    WorkOrder entity representing a manufacturing work order.
    
    This entity follows Clean Architecture principles and is immutable.
    
    Attributes:
        id: Unique identifier for the work order
        order_number: Human-readable work order number
        bom_id: BOM ID
        bom_name: BOM name
        product_id: Product ID
        product_name: Product name
        quantity: Production quantity
        status: Current status
        planned_start: Planned start date
        planned_end: Planned end date
        actual_start: Actual start date
        actual_end: Actual end date
        notes: Additional notes
        metadata: Additional metadata
        created_at: Timestamp when created
        updated_at: Timestamp when last updated
    """
    id: str
    order_number: str
    bom_id: str
    bom_name: str
    product_id: str
    product_name: str
    quantity: Decimal
    status: WorkOrderStatus
    planned_start: Optional[datetime] = None
    planned_end: Optional[datetime] = None
    actual_start: Optional[datetime] = None
    actual_end: Optional[datetime] = None
    notes: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime = field(default_factory=datetime.utcnow)
    
    def __post_init__(self):
        """Validate work order after initialization."""
        if not self.order_number:
            raise ValueError("order_number cannot be empty")
        if not self.bom_id:
            raise ValueError("bom_id cannot be empty")
        if not self.product_id:
            raise ValueError("product_id cannot be empty")
        if self.quantity <= 0:
            raise ValueError("quantity must be positive")
    
    @property
    def is_completed(self) -> bool:
        """Check if work order is completed."""
        return self.status == WorkOrderStatus.COMPLETED
    
    @property
    def is_in_progress(self) -> bool:
        """Check if work order is in progress."""
        return self.status == WorkOrderStatus.IN_PROGRESS
    
    @property
    def is_pending(self) -> bool:
        """Check if work order is pending."""
        return self.status == WorkOrderStatus.PENDING
    
    @property
    def is_overdue(self) -> bool:
        """Check if work order is overdue."""
        if not self.planned_end:
            return False
        if self.is_completed:
            return False
        return datetime.utcnow() > self.planned_end
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert work order to dictionary."""
        return {
            "id": self.id,
            "order_number": self.order_number,
            "bom_id": self.bom_id,
            "bom_name": self.bom_name,
            "product_id": self.product_id,
            "product_name": self.product_name,
            "quantity": str(self.quantity),
            "status": self.status.value,
            "planned_start": self.planned_start.isoformat() if self.planned_start else None,
            "planned_end": self.planned_end.isoformat() if self.planned_end else None,
            "actual_start": self.actual_start.isoformat() if self.actual_start else None,
            "actual_end": self.actual_end.isoformat() if self.actual_end else None,
            "notes": self.notes,
            "metadata": self.metadata,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
            "is_completed": self.is_completed,
            "is_in_progress": self.is_in_progress,
            "is_pending": self.is_pending,
            "is_overdue": self.is_overdue
        }


class BillOfMaterialsBuilder:
    """Builder for creating BillOfMaterials instances."""
    
    def __init__(self):
        self._id: Optional[str] = None
        self._bom_code: Optional[str] = None
        self._name: Optional[str] = None
        self._product_id: Optional[str] = None
        self._product_name: Optional[str] = None
        self._status: BillOfMaterialsStatus = BillOfMaterialsStatus.DRAFT
        self._quantity: Optional[Decimal] = None
        self._items: List[BOMItem] = []
        self._notes: Optional[str] = None
        self._metadata: Dict[str, Any] = {}
    
    def with_id(self, bom_id: str) -> "BillOfMaterialsBuilder":
        self._id = bom_id
        return self
    
    def with_code(self, bom_code: str) -> "BillOfMaterialsBuilder":
        self._bom_code = bom_code
        return self
    
    def with_name(self, name: str) -> "BillOfMaterialsBuilder":
        self._name = name
        return self
    
    def for_product(self, product_id: str, product_name: str) -> "BillOfMaterialsBuilder":
        self._product_id = product_id
        self._product_name = product_name
        return self
    
    def with_status(self, status: BillOfMaterialsStatus) -> "BillOfMaterialsBuilder":
        self._status = status
        return self
    
    def with_quantity(self, quantity: Decimal) -> "BillOfMaterialsBuilder":
        self._quantity = quantity
        return self
    
    def with_items(self, items: List[BOMItem]) -> "BillOfMaterialsBuilder":
        self._items = items
        return self
    
    def with_notes(self, notes: str) -> "BillOfMaterialsBuilder":
        self._notes = notes
        return self
    
    def with_metadata(self, metadata: Dict[str, Any]) -> "BillOfMaterialsBuilder":
        self._metadata = metadata
        return self
    
    def build(self) -> BillOfMaterials:
        from uuid import uuid4
        
        if not self._id:
            self._id = str(uuid4())
        if not self._bom_code:
            from time import time
            self._bom_code = f"BOM-{int(time())}"
        if not self._name:
            raise ValueError("name is required")
        if not self._product_id:
            raise ValueError("product_id is required")
        if not self._quantity:
            raise ValueError("quantity is required")
        
        return BillOfMaterials(
            id=self._id,
            bom_code=self._bom_code,
            name=self._name,
            product_id=self._product_id,
            product_name=self._product_name or "",
            status=self._status,
            quantity=self._quantity,
            items=self._items,
            notes=self._notes,
            metadata=self._metadata
        )


class WorkOrderBuilder:
    """Builder for creating WorkOrder instances."""
    
    def __init__(self):
        self._id: Optional[str] = None
        self._order_number: Optional[str] = None
        self._bom_id: Optional[str] = None
        self._bom_name: Optional[str] = None
        self._product_id: Optional[str] = None
        self._product_name: Optional[str] = None
        self._quantity: Optional[Decimal] = None
        self._status: WorkOrderStatus = WorkOrderStatus.PENDING
        self._planned_start: Optional[datetime] = None
        self._planned_end: Optional[datetime] = None
        self._notes: Optional[str] = None
        self._metadata: Dict[str, Any] = {}
    
    def with_id(self, order_id: str) -> "WorkOrderBuilder":
        self._id = order_id
        return self
    
    def with_number(self, order_number: str) -> "WorkOrderBuilder":
        self._order_number = order_number
        return self
    
    def for_bom(self, bom_id: str, bom_name: str) -> "WorkOrderBuilder":
        self._bom_id = bom_id
        self._bom_name = bom_name
        return self
    
    def for_product(self, product_id: str, product_name: str) -> "WorkOrderBuilder":
        self._product_id = product_id
        self._product_name = product_name
        return self
    
    def with_quantity(self, quantity: Decimal) -> "WorkOrderBuilder":
        self._quantity = quantity
        return self
    
    def with_status(self, status: WorkOrderStatus) -> "WorkOrderBuilder":
        self._status = status
        return self
    
    def planned(self, start: datetime, end: datetime) -> "WorkOrderBuilder":
        self._planned_start = start
        self._planned_end = end
        return self
    
    def with_notes(self, notes: str) -> "WorkOrderBuilder":
        self._notes = notes
        return self
    
    def with_metadata(self, metadata: Dict[str, Any]) -> "WorkOrderBuilder":
        self._metadata = metadata
        return self
    
    def build(self) -> WorkOrder:
        from uuid import uuid4
        
        if not self._id:
            self._id = str(uuid4())
        if not self._order_number:
            from time import time
            self._order_number = f"WO-{int(time())}"
        if not self._bom_id:
            raise ValueError("bom_id is required")
        if not self._product_id:
            raise ValueError("product_id is required")
        if not self._quantity:
            raise ValueError("quantity is required")
        
        return WorkOrder(
            id=self._id,
            order_number=self._order_number,
            bom_id=self._bom_id,
            bom_name=self._bom_name or "",
            product_id=self._product_id,
            product_name=self._product_name or "",
            quantity=self._quantity,
            status=self._status,
            planned_start=self._planned_start,
            planned_end=self._planned_end,
            notes=self._notes,
            metadata=self._metadata
        )


# Factory functions
def create_bom_item(
    component_id: str,
    component_name: str,
    quantity: Decimal,
    **kwargs
) -> BOMItem:
    """Factory function to create a BOM item."""
    from uuid import uuid4
    
    return BOMItem(
        id=str(uuid4()),
        component_id=component_id,
        component_name=component_name,
        quantity=quantity,
        unit=kwargs.get("unit", "pcs"),
        scrap_percent=kwargs.get("scrap_percent", Decimal("0")),
        notes=kwargs.get("notes")
    )


def create_bill_of_materials(
    name: str,
    product_id: str,
    product_name: str,
    quantity: Decimal,
    **kwargs
) -> BillOfMaterials:
    """Factory function to create a BOM."""
    builder = BillOfMaterialsBuilder()
    builder.with_name(name)
    builder.for_product(product_id, product_name)
    builder.with_quantity(quantity)
    
    if bom_code := kwargs.get("bom_code"):
        builder.with_code(bom_code)
    if status := kwargs.get("status"):
        builder.with_status(status)
    if items := kwargs.get("items"):
        builder.with_items(items)
    if notes := kwargs.get("notes"):
        builder.with_notes(notes)
    if metadata := kwargs.get("metadata"):
        builder.with_metadata(metadata)
    
    return builder.build()


def create_work_order(
    bom_id: str,
    bom_name: str,
    product_id: str,
    product_name: str,
    quantity: Decimal,
    **kwargs
) -> WorkOrder:
    """Factory function to create a work order."""
    builder = WorkOrderBuilder()
    builder.for_bom(bom_id, bom_name)
    builder.for_product(product_id, product_name)
    builder.with_quantity(quantity)
    
    if order_number := kwargs.get("order_number"):
        builder.with_number(order_number)
    if status := kwargs.get("status"):
        builder.with_status(status)
    if planned_start := kwargs.get("planned_start"):
        planned_end = kwargs.get("planned_end")
        builder.planned(planned_start, planned_end)
    if notes := kwargs.get("notes"):
        builder.with_notes(notes)
    if metadata := kwargs.get("metadata"):
        builder.with_metadata(metadata)
    
    return builder.build()
