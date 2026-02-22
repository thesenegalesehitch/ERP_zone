"""
Inventory Movement Entity - Domain Layer
Represents inventory stock movements.

Author: Alexandre Albert Ndour
"""

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Optional
from enum import Enum
import uuid


class MovementType(str, Enum):
    """Inventory movement types."""
    PURCHASE = "purchase"
    SALE = "sale"
    ADJUSTMENT = "adjustment"
    RETURN = "return"
    TRANSFER = "transfer"
    DAMAGE = "damage"
    THEFT = "theft"
    INITIAL = "initial"


class MovementReason(str, Enum):
    """Reasons for inventory movement."""
    # Purchase
    PURCHASE_ORDER = "purchase_order"
    RETURN_FROM_CUSTOMER = "return_from_customer"
    
    # Sale
    SALES_ORDER = "sales_order"
    RETURN_TO_SUPPLIER = "return_to_supplier"
    
    # Adjustment
    STOCK_COUNT = "stock_count"
    CORRECTION = "correction"
    DAMAGED = "damaged"
    EXPIRED = "expired"
    LOST = "lost"
    FOUND = "found"
    
    # Transfer
    WAREHOUSE_TRANSFER = "warehouse_transfer"
    LOCATION_TRANSFER = "location_transfer"


@dataclass
class InventoryMovement:
    """
    InventoryMovement Entity.
    
    Represents a movement of inventory (in or out).
    """
    
    # Identity
    id: uuid.UUID = field(default_factory=uuid.uuid4)
    
    # References
    product_id: uuid.UUID = None  # type: ignore
    variant_id: Optional[uuid.UUID] = None
    warehouse_id: Optional[uuid.UUID] = None
    
    # Movement details
    movement_type: MovementType = MovementType.ADJUSTMENT
    reason: MovementReason = MovementReason.CORRECTION
    
    # Quantity
    quantity: int = 0
    quantity_before: int = 0
    quantity_after: int = 0
    
    # Reference
    reference_type: Optional[str] = None  # order, invoice, etc.
    reference_id: Optional[uuid.UUID] = None
    
    # Notes
    notes: Optional[str] = None
    
    # User
    performed_by: Optional[uuid.UUID] = None
    
    # Status
    is_confirmed: bool = False
    
    # Metadata
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    
    def __post_init__(self):
        """Validate after initialization."""
        if isinstance(self.product_id, str):
            self.product_id = uuid.UUID(self.product_id)
        if isinstance(self.variant_id, str):
            self.variant_id = uuid.UUID(self.variant_id)
        if isinstance(self.reference_id, str):
            self.reference_id = uuid.UUID(self.reference_id)
        
        if self.quantity == 0:
            raise ValueError("Quantity cannot be zero")
    
    # ==================== Business Methods ====================
    
    def confirm(self, performed_by: uuid.UUID) -> None:
        """Confirm the movement."""
        self.is_confirmed = True
        self.performed_by = performed_by
    
    def cancel(self) -> None:
        """Cancel the movement."""
        self.is_confirmed = False
    
    def calculate_quantity_after(self) -> int:
        """Calculate quantity after movement."""
        if self.movement_type in [MovementType.PURCHASE, MovementType.RETURN, MovementType.INITIAL]:
            return self.quantity_before + abs(self.quantity)
        else:
            return self.quantity_before - abs(self.quantity)
    
    # ==================== Factory Methods ====================
    
    @classmethod
    def create_purchase(
        cls,
        product_id: uuid.UUID,
        quantity: int,
        warehouse_id: uuid.UUID = None,
        reference_id: uuid.UUID = None,
        notes: str = None
    ) -> "InventoryMovement":
        """Create a purchase movement."""
        return cls(
            product_id=product_id,
            warehouse_id=warehouse_id,
            movement_type=MovementType.PURCHASE,
            reason=MovementReason.PURCHASE_ORDER,
            quantity=abs(quantity),
            reference_id=reference_id,
            notes=notes
        )
    
    @classmethod
    def create_sale(
        cls,
        product_id: uuid.UUID,
        quantity: int,
        warehouse_id: uuid.UUID = None,
        reference_id: uuid.UUID = None,
        notes: str = None
    ) -> "InventoryMovement":
        """Create a sale movement."""
        return cls(
            product_id=product_id,
            warehouse_id=warehouse_id,
            movement_type=MovementType.SALE,
            reason=MovementReason.SALES_ORDER,
            quantity=-abs(quantity),
            reference_id=reference_id,
            notes=notes
        )
    
    @classmethod
    def create_adjustment(
        cls,
        product_id: uuid.UUID,
        quantity: int,
        reason: MovementReason = MovementReason.CORRECTION,
        notes: str = None
    ) -> "InventoryMovement":
        """Create an adjustment movement."""
        return cls(
            product_id=product_id,
            movement_type=MovementType.ADJUSTMENT,
            reason=reason,
            quantity=quantity,
            notes=notes
        )
    
    # ==================== Serialization ====================
    
    def to_dict(self) -> dict:
        """Convert to dictionary."""
        return {
            "id": str(self.id),
            "product_id": str(self.product_id),
            "variant_id": str(self.variant_id) if self.variant_id else None,
            "warehouse_id": str(self.warehouse_id) if self.warehouse_id else None,
            "movement_type": self.movement_type.value,
            "reason": self.reason.value,
            "quantity": self.quantity,
            "quantity_before": self.quantity_before,
            "quantity_after": self.quantity_after,
            "reference_type": self.reference_type,
            "reference_id": str(self.reference_id) if self.reference_id else None,
            "notes": self.notes,
            "performed_by": str(self.performed_by) if self.performed_by else None,
            "is_confirmed": self.is_confirmed,
            "created_at": self.created_at.isoformat(),
        }


@dataclass
class StockAlert:
    """
    StockAlert Entity.
    
    Represents an alert for low stock or out of stock.
    """
    
    # Identity
    id: uuid.UUID = field(default_factory=uuid.uuid4)
    
    # References
    product_id: uuid.UUID = None  # type: ignore
    warehouse_id: Optional[uuid.UUID] = None
    
    # Alert details
    alert_type: str = "low_stock"  # low_stock, out_of_stock, overstock
    current_stock: int = 0
    threshold: int = 0
    
    # Status
    is_resolved: bool = False
    resolved_at: Optional[datetime] = None
    resolution_notes: Optional[str] = None
    
    # Metadata
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    
    def resolve(self, notes: str = None) -> None:
        """Resolve the alert."""
        self.is_resolved = True
        self.resolved_at = datetime.now(timezone.utc)
        self.resolution_notes = notes
    
    def to_dict(self) -> dict:
        return {
            "id": str(self.id),
            "product_id": str(self.product_id),
            "warehouse_id": str(self.warehouse_id) if self.warehouse_id else None,
            "alert_type": self.alert_type,
            "current_stock": self.current_stock,
            "threshold": self.threshold,
            "is_resolved": self.is_resolved,
            "resolved_at": self.resolved_at.isoformat() if self.resolved_at else None,
            "created_at": self.created_at.isoformat(),
        }
