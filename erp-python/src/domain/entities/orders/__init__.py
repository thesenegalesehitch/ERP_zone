"""
Order Entity - Domain Layer
Represents an order in the ERP system.

Author: Alexandre Albert Ndour
"""

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Optional, List
from enum import Enum
import uuid


class OrderStatus(str, Enum):
    """Order status enumeration."""
    DRAFT = "draft"
    PENDING = "pending"
    CONFIRMED = "confirmed"
    PROCESSING = "processing"
    SHIPPED = "shipped"
    DELIVERED = "delivered"
    CANCELLED = "cancelled"
    REFUNDED = "refunded"


class PaymentStatus(str, Enum):
    """Payment status enumeration."""
    PENDING = "pending"
    PARTIAL = "partial"
    PAID = "paid"
    FAILED = "failed"
    REFUNDED = "refunded"


class ShippingStatus(str, Enum):
    """Shipping status enumeration."""
    NOT_SHIPPED = "not_shipped"
    PREPARING = "preparing"
    SHIPPED = "shipped"
    IN_TRANSIT = "in_transit"
    DELIVERED = "delivered"
    FAILED = "failed"


@dataclass
class Order:
    """
    Order Entity.
    
    Represents a customer order with lines, totals, and status tracking.
    """
    
    # Identity
    id: uuid.UUID = field(default_factory=uuid.uuid4)
    order_number: str = ""
    
    # References
    customer_id: uuid.UUID = None  # type: ignore
    
    # Status
    status: OrderStatus = OrderStatus.DRAFT
    payment_status: PaymentStatus = PaymentStatus.PENDING
    shipping_status: ShippingStatus = ShippingStatus.NOT_SHIPPED
    
    # Pricing
    subtotal: float = 0.0
    tax_amount: float = 0.0
    shipping_amount: float = 0.0
    discount_amount: float = 0.0
    total: float = 0.0
    
    # Currency
    currency: str = "EUR"
    
    # Dates
    order_date: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    confirmed_date: Optional[datetime] = None
    shipped_date: Optional[datetime] = None
    delivered_date: Optional[datetime] = None
    cancelled_date: Optional[datetime] = None
    
    # Notes
    customer_notes: Optional[str] = None
    internal_notes: Optional[str] = None
    
    # Shipping
    shipping_address_id: Optional[uuid.UUID] = None
    billing_address_id: Optional[uuid.UUID] = None
    
    # Metadata
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    created_by: Optional[uuid.UUID] = None
    
    # Lines (loaded separately)
    _lines: List["OrderLine"] = field(default_factory=list, repr=False)
    
    def __post_init__(self):
        """Validate after initialization."""
        if isinstance(self.customer_id, str):
            self.customer_id = uuid.UUID(self.customer_id)
    
    # ==================== Business Methods ====================
    
    def add_line(self, line: "OrderLine") -> None:
        """Add a line to the order."""
        self._lines.append(line)
        self._recalculate_totals()
    
    def remove_line(self, line_id: uuid.UUID) -> None:
        """Remove a line from the order."""
        self._lines = [l for l in self._lines if l.id != line_id]
        self._recalculate_totals()
    
    def _recalculate_totals(self) -> None:
        """Recalculate order totals."""
        self.subtotal = sum(line.total for line in self._lines)
        self.tax_amount = sum(line.tax_amount for line in self._lines)
        self.total = self.subtotal + self.tax_amount + self.shipping_amount - self.discount_amount
    
    def set_status(self, status: OrderStatus) -> None:
        """Set order status."""
        self.status = status
        self.updated_at = datetime.now(timezone.utc)
        
        # Update date based on status
        if status == OrderStatus.CONFIRMED:
            self.confirmed_date = datetime.now(timezone.utc)
        elif status == OrderStatus.SHIPPED:
            self.shipped_date = datetime.now(timezone.utc)
        elif status == OrderStatus.DELIVERED:
            self.delivered_date = datetime.now(timezone.utc)
        elif status == OrderStatus.CANCELLED:
            self.cancelled_date = datetime.now(timezone.utc)
    
    def set_payment_status(self, status: PaymentStatus) -> None:
        """Set payment status."""
        self.payment_status = status
        self.updated_at = datetime.now(timezone.utc)
    
    def set_shipping_status(self, status: ShippingStatus) -> None:
        """Set shipping status."""
        self.shipping_status = status
        self.updated_at = datetime.now(timezone.utc)
    
    def apply_discount(self, amount: float) -> None:
        """Apply discount to order."""
        if amount < 0:
            raise ValueError("Discount cannot be negative")
        if amount > self.subtotal + self.tax_amount:
            raise ValueError("Discount cannot exceed order total")
        self.discount_amount = amount
        self._recalculate_totals()
    
    def set_shipping_cost(self, cost: float) -> None:
        """Set shipping cost."""
        if cost < 0:
            raise ValueError("Shipping cost cannot be negative")
        self.shipping_amount = cost
        self._recalculate_totals()
    
    def can_cancel(self) -> bool:
        """Check if order can be cancelled."""
        return self.status not in [
            OrderStatus.DELIVERED,
            OrderStatus.CANCELLED,
            OrderStatus.REFUNDED
        ]
    
    def cancel(self, reason: str = None) -> None:
        """Cancel the order."""
        if not self.can_cancel():
            raise ValueError("Order cannot be cancelled")
        self.set_status(OrderStatus.CANCELLED)
        self.internal_notes = reason
    
    def confirm(self) -> None:
        """Confirm the order."""
        if self.status != OrderStatus.DRAFT:
            raise ValueError("Only draft orders can be confirmed")
        self.set_status(OrderStatus.CONFIRMED)
    
    def process(self) -> None:
        """Process the order."""
        if self.status != OrderStatus.CONFIRMED:
            raise ValueError("Only confirmed orders can be processed")
        self.set_status(OrderStatus.PROCESSING)
    
    def ship(self) -> None:
        """Ship the order."""
        if self.status != OrderStatus.PROCESSING:
            raise ValueError("Only processing orders can be shipped")
        self.set_status(OrderStatus.SHIPPED)
        self.set_shipping_status(ShippingStatus.SHIPPED)
    
    def deliver(self) -> None:
        """Mark order as delivered."""
        if self.status != OrderStatus.SHIPPED:
            raise ValueError("Only shipped orders can be delivered")
        self.set_status(OrderStatus.DELIVERED)
        self.set_shipping_status(ShippingStatus.DELIVERED)
    
    # ==================== Properties ====================
    
    @property
    def lines(self) -> List["OrderLine"]:
        """Get order lines."""
        return self._lines.copy()
    
    @property
    def line_count(self) -> int:
        """Get number of order lines."""
        return len(self._lines)
    
    @property
    def item_count(self) -> int:
        """Get total number of items."""
        return sum(line.quantity for line in self._lines)
    
    @property
    def is_paid(self) -> bool:
        """Check if order is fully paid."""
        return self.payment_status == PaymentStatus.PAID
    
    @property
    def is_shipped(self) -> bool:
        """Check if order is shipped."""
        return self.shipping_status in [
            ShippingStatus.SHIPPED,
            ShippingStatus.IN_TRANSIT,
            ShippingStatus.DELIVERED
        ]
    
    # ==================== Factory Methods ====================
    
    @classmethod
    def create(
        cls,
        customer_id: uuid.UUID,
        order_number: str = None,
        created_by: uuid.UUID = None
    ) -> "Order":
        """Factory method to create a new order."""
        if order_number is None:
            order_number = cls._generate_order_number()
        
        return cls(
            order_number=order_number,
            customer_id=customer_id,
            created_by=created_by
        )
    
    @classmethod
    def _generate_order_number(cls) -> str:
        """Generate order number."""
        from datetime import datetime
        now = datetime.now()
        return f"ORD-{now.strftime('%Y%m%d')}-{uuid.uuid4().hex[:8].upper()}"
    
    # ==================== Serialization ====================
    
    def to_dict(self) -> dict:
        """Convert to dictionary."""
        return {
            "id": str(self.id),
            "order_number": self.order_number,
            "customer_id": str(self.customer_id),
            "status": self.status.value,
            "payment_status": self.payment_status.value,
            "shipping_status": self.shipping_status.value,
            "subtotal": self.subtotal,
            "tax_amount": self.tax_amount,
            "shipping_amount": self.shipping_amount,
            "discount_amount": self.discount_amount,
            "total": self.total,
            "currency": self.currency,
            "order_date": self.order_date.isoformat(),
            "confirmed_date": self.confirmed_date.isoformat() if self.confirmed_date else None,
            "shipped_date": self.shipped_date.isoformat() if self.shipped_date else None,
            "delivered_date": self.delivered_date.isoformat() if self.delivered_date else None,
            "cancelled_date": self.cancelled_date.isoformat() if self.cancelled_date else None,
            "customer_notes": self.customer_notes,
            "internal_notes": self.internal_notes,
            "line_count": self.line_count,
            "item_count": self.item_count,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
        }


@dataclass
class OrderLine:
    """
    OrderLine Entity.
    
    Represents a single line item in an order.
    """
    
    # Identity
    id: uuid.UUID = field(default_factory=uuid.uuid4)
    order_id: uuid.UUID = None  # type: ignore
    
    # Product reference
    product_id: uuid.UUID = None  # type: ignore
    variant_id: Optional[uuid.UUID] = None
    
    # Line details
    name: str = ""
    sku: str = ""
    
    # Quantity
    quantity: int = 1
    unit_price: float = 0.0
    tax_rate: float = 0.0
    
    # Totals
    discount_amount: float = 0.0
    
    # Status
    is_cancelled: bool = False
    cancelled_reason: Optional[str] = None
    
    # Metadata
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    
    def __post_init__(self):
        """Validate after initialization."""
        if isinstance(self.product_id, str):
            self.product_id = uuid.UUID(self.product_id)
        if self.quantity <= 0:
            raise ValueError("Quantity must be positive")
        if self.unit_price < 0:
            raise ValueError("Unit price cannot be negative")
    
    # ==================== Business Methods ====================
    
    @property
    def subtotal(self) -> float:
        """Calculate line subtotal (before tax and discount)."""
        return self.quantity * self.unit_price
    
    @property
    def tax_amount(self) -> float:
        """Calculate line tax amount."""
        taxable = self.subtotal - self.discount_amount
        return taxable * (self.tax_rate / 100)
    
    @property
    def total(self) -> float:
        """Calculate line total (with tax and discount)."""
        return self.subtotal - self.discount_amount + self.tax_amount
    
    @property
    def total_with_tax(self) -> float:
        """Calculate line total including tax."""
        return self.subtotal - self.discount_amount + self.tax_amount
    
    def apply_discount(self, amount: float) -> None:
        """Apply discount to line."""
        if amount < 0:
            raise ValueError("Discount cannot be negative")
        if amount > self.subtotal:
            raise ValueError("Discount cannot exceed line subtotal")
        self.discount_amount = amount
        self.updated_at = datetime.now(timezone.utc)
    
    def cancel(self, reason: str = None) -> None:
        """Cancel the line item."""
        self.is_cancelled = True
        self.cancelled_reason = reason
        self.updated_at = datetime.now(timezone.utc)
    
    def update_quantity(self, quantity: int) -> None:
        """Update line quantity."""
        if quantity <= 0:
            raise ValueError("Quantity must be positive")
        self.quantity = quantity
        self.updated_at = datetime.now(timezone.utc)
    
    # ==================== Factory Methods ====================
    
    @classmethod
    def create(
        cls,
        order_id: uuid.UUID,
        product_id: uuid.UUID,
        name: str,
        sku: str,
        quantity: int,
        unit_price: float,
        tax_rate: float = 0.0,
        variant_id: uuid.UUID = None
    ) -> "OrderLine":
        """Factory method to create an order line."""
        return cls(
            order_id=order_id,
            product_id=product_id,
            variant_id=variant_id,
            name=name,
            sku=sku,
            quantity=quantity,
            unit_price=unit_price,
            tax_rate=tax_rate
        )
    
    # ==================== Serialization ====================
    
    def to_dict(self) -> dict:
        """Convert to dictionary."""
        return {
            "id": str(self.id),
            "order_id": str(self.order_id),
            "product_id": str(self.product_id),
            "variant_id": str(self.variant_id) if self.variant_id else None,
            "name": self.name,
            "sku": self.sku,
            "quantity": self.quantity,
            "unit_price": self.unit_price,
            "tax_rate": self.tax_rate,
            "discount_amount": self.discount_amount,
            "subtotal": self.subtotal,
            "tax_amount": self.tax_amount,
            "total": self.total,
            "is_cancelled": self.is_cancelled,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
        }
