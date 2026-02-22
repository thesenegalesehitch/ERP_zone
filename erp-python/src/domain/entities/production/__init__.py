"""
Production Entity for ERP System.

This module provides entities for production/manufacturing management
following Clean Architecture principles.
"""

from dataclasses import dataclass, field
from datetime import datetime, date, timedelta
from typing import Optional, Dict, Any, List
from enum import Enum
from uuid import uuid4
from decimal import Decimal


class ProductionOrderStatus(str, Enum):
    """Production order status enumeration."""
    DRAFT = "draft"
    SCHEDULED = "scheduled"
    IN_PROGRESS = "in_progress"
    ON_HOLD = "on_hold"
    COMPLETED = "completed"
    CANCELLED = "cancelled"
    PARTIALLY_COMPLETED = "partially_completed"


class ProductionType(str, Enum):
    """Production type enumeration."""
    MAKE_TO_ORDER = "make_to_order"
    MAKE_TO_STOCK = "make_to_stock"
    ENGINEER_TO_ORDER = "engineer_to_order"


class QualityCheckStatus(str, Enum):
    """Quality check status enumeration."""
    PENDING = "pending"
    PASSED = "passed"
    FAILED = "failed"
    REWORK_REQUIRED = "rework_required"


@dataclass(frozen=True)
class BillOfMaterialsLine:
    """
    Value Object representing a BOM line item.
    Immutable and validated.
    """
    id: str
    component_id: str
    component_sku: str
    component_name: str
    quantity: Decimal
    unit_of_measure: str
    scrap_percentage: Decimal = field(default=Decimal("0"))
    is_optional: bool = False
    sequence: int = 0
    
    @property
    def effective_quantity(self) -> Decimal:
        scrap_factor = Decimal("1") + (self.scrap_percentage / Decimal("100"))
        return self.quantity * scrap_factor
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "component_id": self.component_id,
            "component_sku": self.component_sku,
            "component_name": self.component_name,
            "quantity": str(self.quantity),
            "unit_of_measure": self.unit_of_measure,
            "scrap_percentage": str(self.scrap_percentage),
            "is_optional": self.is_optional,
            "sequence": self.sequence,
            "effective_quantity": str(self.effective_quantity)
        }


@dataclass(frozen=True)
class WorkCenter:
    """
    Value Object representing a work center.
    Immutable and validated.
    """
    id: str
    name: str
    code: str
    capacity: int
    efficiency: Decimal
    setup_time_minutes: int = 0
    is_active: bool = True
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "name": self.name,
            "code": self.code,
            "capacity": self.capacity,
            "efficiency": str(self.efficiency),
            "setup_time_minutes": self.setup_time_minutes,
            "is_active": self.is_active
        }


@dataclass(frozen=True)
class ProductionOrder:
    """
    Production Order entity for managing manufacturing.
    
    This entity follows Clean Architecture principles and is immutable.
    
    Attributes:
        id: Unique identifier
        order_number: Human-readable order number
        product_id: Product to manufacture
        product_name: Product name
        product_sku: Product SKU
        quantity: Production quantity
        production_type: Type of production
        status: Current order status
        bom_id: Bill of materials ID
        bom_version: BOM version
        work_center_id: Work center ID
        work_center_name: Work center name
        scheduled_start: Scheduled start date
        scheduled_end: Scheduled end date
        actual_start: Actual start date
        actual_end: Actual end date
        produced_quantity: Quantity produced
        rejected_quantity: Rejected quantity
        scrap_quantity: Scrap quantity
        notes: Additional notes
        created_by: Creator user ID
        created_name: Creator name
        metadata: Additional metadata
        created_at: Creation timestamp
        updated_at: Last update timestamp
    """
    id: str
    order_number: str
    product_id: str
    product_name: str
    product_sku: str
    quantity: int
    production_type: ProductionType
    status: ProductionOrderStatus
    bom_id: str
    bom_version: str
    work_center_id: str
    work_center_name: str
    scheduled_start: Optional[datetime] = None
    scheduled_end: Optional[datetime] = None
    actual_start: Optional[datetime] = None
    actual_end: Optional[datetime] = None
    produced_quantity: int = 0
    rejected_quantity: int = 0
    scrap_quantity: int = 0
    notes: str = ""
    created_by: str = ""
    created_name: str = ""
    metadata: Dict[str, Any] = field(default_factory=dict)
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime = field(default_factory=datetime.utcnow)
    
    def __post_init__(self):
        if not self.order_number:
            raise ValueError("order_number cannot be empty")
        if self.quantity <= 0:
            raise ValueError("quantity must be positive")
    
    @property
    def is_scheduled(self) -> bool:
        return self.status == ProductionOrderStatus.SCHEDULED
    
    @property
    def is_in_progress(self) -> bool:
        return self.status == ProductionOrderStatus.IN_PROGRESS
    
    @property
    def is_completed(self) -> bool:
        return self.status == ProductionOrderStatus.COMPLETED
    
    @property
    def completion_percentage(self) -> float:
        if self.quantity == 0:
            return 0.0
        return (self.produced_quantity / self.quantity) * 100
    
    @property
    def quality_rate(self) -> float:
        total = self.produced_quantity + self.rejected_quantity + self.scrap_quantity
        if total == 0:
            return 0.0
        return (self.produced_quantity / total) * 100
    
    @property
    def is_delayed(self) -> bool:
        if not self.scheduled_end:
            return False
        return datetime.utcnow() > self.scheduled_end and not self.is_completed
    
    @property
    def duration_days(self) -> Optional[int]:
        if self.actual_start and self.actual_end:
            delta = self.actual_end - self.actual_start
            return delta.days
        return None
    
    def start(self) -> None:
        """Start the production order."""
        self.status = ProductionOrderStatus.IN_PROGRESS
        self.actual_start = datetime.utcnow()
    
    def complete(self, produced: int, rejected: int = 0, scrap: int = 0) -> None:
        """Complete the production order."""
        self.produced_quantity = produced
        self.rejected_quantity = rejected
        self.scrap_quantity = scrap
        self.status = ProductionOrderStatus.COMPLETED
        self.actual_end = datetime.utcnow()
    
    def hold(self, reason: str) -> None:
        """Put the production order on hold."""
        self.status = ProductionOrderStatus.ON_HOLD
        self.notes += f"\n[ON HOLD: {reason}]"
    
    def cancel(self, reason: str) -> None:
        """Cancel the production order."""
        self.status = ProductionOrderStatus.CANCELLED
        self.notes += f"\n[CANCELLED: {reason}]"
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "order_number": self.order_number,
            "product_id": self.product_id,
            "product_name": self.product_name,
            "product_sku": self.product_sku,
            "quantity": self.quantity,
            "production_type": self.production_type.value,
            "status": self.status.value,
            "bom_id": self.bom_id,
            "bom_version": self.bom_version,
            "work_center_id": self.work_center_id,
            "work_center_name": self.work_center_name,
            "scheduled_start": self.scheduled_start.isoformat() if self.scheduled_start else None,
            "scheduled_end": self.scheduled_end.isoformat() if self.scheduled_end else None,
            "actual_start": self.actual_start.isoformat() if self.actual_start else None,
            "actual_end": self.actual_end.isoformat() if self.actual_end else None,
            "produced_quantity": self.produced_quantity,
            "rejected_quantity": self.rejected_quantity,
            "scrap_quantity": self.scrap_quantity,
            "notes": self.notes,
            "created_by": self.created_by,
            "created_name": self.created_name,
            "metadata": self.metadata,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
            "is_scheduled": self.is_scheduled,
            "is_in_progress": self.is_in_progress,
            "is_completed": self.is_completed,
            "completion_percentage": self.completion_percentage,
            "quality_rate": self.quality_rate,
            "is_delayed": self.is_delayed,
            "duration_days": self.duration_days
        }


class ProductionOrderBuilder:
    """Builder for creating ProductionOrder instances."""
    
    def __init__(self):
        self._id: Optional[str] = None
        self._order_number: Optional[str] = None
        self._product_id: Optional[str] = None
        self._product_name: str = ""
        self._product_sku: str = ""
        self._quantity: int = 0
        self._production_type: ProductionType = ProductionType.MAKE_TO_STOCK
        self._status: ProductionOrderStatus = ProductionOrderStatus.DRAFT
        self._bom_id: str = ""
        self._bom_version: str = "1.0"
        self._work_center_id: str = ""
        self._work_center_name: str = ""
        self._scheduled_start: Optional[datetime] = None
        self._scheduled_end: Optional[datetime] = None
        self._notes: str = ""
        self._created_by: str = ""
        self._created_name: str = ""
        self._metadata: Dict[str, Any] = {}
    
    def with_id(self, order_id: str) -> "ProductionOrderBuilder":
        self._id = order_id
        return self
    
    def with_order_number(self, order_number: str) -> "ProductionOrderBuilder":
        self._order_number = order_number
        return self
    
    def for_product(self, product_id: str, product_sku: str, product_name: str, quantity: int) -> "ProductionOrderBuilder":
        self._product_id = product_id
        self._product_sku = product_sku
        self._product_name = product_name
        self._quantity = quantity
        return self
    
    def with_production_type(self, prod_type: ProductionType) -> "ProductionOrderBuilder":
        self._production_type = prod_type
        return self
    
    def with_status(self, status: ProductionOrderStatus) -> "ProductionOrderBuilder":
        self._status = status
        return self
    
    def with_bom(self, bom_id: str, version: str = "1.0") -> "ProductionOrderBuilder":
        self._bom_id = bom_id
        self._bom_version = version
        return self
    
    def at_work_center(self, work_center_id: str, work_center_name: str) -> "ProductionOrderBuilder":
        self._work_center_id = work_center_id
        self._work_center_name = work_center_name
        return self
    
    def scheduled(self, start: datetime, end: datetime) -> "ProductionOrderBuilder":
        self._scheduled_start = start
        self._scheduled_end = end
        return self
    
    def with_notes(self, notes: str) -> "ProductionOrderBuilder":
        self._notes = notes
        return self
    
    def created_by(self, user_id: str, user_name: str) -> "ProductionOrderBuilder":
        self._created_by = user_id
        self._created_name = user_name
        return self
    
    def with_metadata(self, metadata: Dict[str, Any]) -> "ProductionOrderBuilder":
        self._metadata = metadata
        return self
    
    def build(self) -> ProductionOrder:
        if not self._id:
            self._id = str(uuid4())
        if not self._order_number:
            from time import time
            self._order_number = f"PROD-{int(time())}"
        if not self._product_id:
            raise ValueError("product_id is required")
        if self._quantity <= 0:
            raise ValueError("quantity must be positive")
        
        return ProductionOrder(
            id=self._id,
            order_number=self._order_number,
            product_id=self._product_id,
            product_name=self._product_name,
            product_sku=self._product_sku,
            quantity=self._quantity,
            production_type=self._production_type,
            status=self._status,
            bom_id=self._bom_id,
            bom_version=self._bom_version,
            work_center_id=self._work_center_id,
            work_center_name=self._work_center_name,
            scheduled_start=self._scheduled_start,
            scheduled_end=self._scheduled_end,
            notes=self._notes,
            created_by=self._created_by,
            created_name=self._created_name,
            metadata=self._metadata
        )


def create_production_order(
    product_id: str,
    product_sku: str,
    product_name: str,
    quantity: int,
    **kwargs
) -> ProductionOrder:
    """Factory function to create a production order."""
    builder = ProductionOrderBuilder()
    builder.for_product(product_id, product_sku, product_name, quantity)
    
    if order_number := kwargs.get("order_number"):
        builder.with_order_number(order_number)
    if production_type := kwargs.get("production_type"):
        builder.with_production_type(production_type)
    if status := kwargs.get("status"):
        builder.with_status(status)
    if bom_id := kwargs.get("bom_id"):
        bom_version = kwargs.get("bom_version", "1.0")
        builder.with_bom(bom_id, bom_version)
    if work_center_id := kwargs.get("work_center_id"):
        work_center_name = kwargs.get("work_center_name", "")
        builder.at_work_center(work_center_id, work_center_name)
    if scheduled_start := kwargs.get("scheduled_start"):
        scheduled_end = kwargs.get("scheduled_end")
        if scheduled_end:
            builder.scheduled(scheduled_start, scheduled_end)
    if notes := kwargs.get("notes"):
        builder.with_notes(notes)
    if created_by := kwargs.get("created_by"):
        created_name = kwargs.get("created_name", "")
        builder.created_by(created_by, created_name)
    if metadata := kwargs.get("metadata"):
        builder.with_metadata(metadata)
    
    return builder.build()


def create_work_center(
    name: str,
    code: str,
    capacity: int,
    **kwargs
) -> WorkCenter:
    """Factory function to create a work center."""
    return WorkCenter(
        id=str(uuid4()),
        name=name,
        code=code,
        capacity=capacity,
        efficiency=kwargs.get("efficiency", Decimal("100")),
        setup_time_minutes=kwargs.get("setup_time_minutes", 0),
        is_active=kwargs.get("is_active", True)
    )


def create_bom_line(
    component_id: str,
    component_sku: str,
    component_name: str,
    quantity: Decimal,
    unit_of_measure: str,
    **kwargs
) -> BillOfMaterialsLine:
    """Factory function to create a BOM line."""
    return BillOfMaterialsLine(
        id=str(uuid4()),
        component_id=component_id,
        component_sku=component_sku,
        component_name=component_name,
        quantity=quantity,
        unit_of_measure=unit_of_measure,
        scrap_percentage=kwargs.get("scrap_percentage", Decimal("0")),
        is_optional=kwargs.get("is_optional", False),
        sequence=kwargs.get("sequence", 0)
    )
