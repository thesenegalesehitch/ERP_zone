"""
Purchasing Entity for ERP System.

This module provides entities for managing purchases and supplier orders
following Clean Architecture principles.
"""

from dataclasses import dataclass, field
from datetime import datetime, date
from typing import Optional, Dict, Any, List
from enum import Enum
from uuid import uuid4
from decimal import Decimal


class PurchaseOrderStatus(str, Enum):
    """Purchase order status enumeration."""
    DRAFT = "draft"
    PENDING = "pending"
    APPROVED = "approved"
    ORDERED = "ordered"
    PARTIALLY_RECEIVED = "partially_received"
    RECEIVED = "received"
    CANCELLED = "cancelled"
    REJECTED = "rejected"


class PurchaseRequestStatus(str, Enum):
    """Purchase request status enumeration."""
    DRAFT = "draft"
    SUBMITTED = "submitted"
    UNDER_REVIEW = "under_review"
    APPROVED = "approved"
    REJECTED = "rejected"
    CONVERTED = "converted"


class DeliveryStatus(str, Enum):
    """Delivery status enumeration."""
    PENDING = "pending"
    PARTIAL = "partial"
    COMPLETE = "complete"
    OVERDUE = "overdue"


@dataclass(frozen=True)
class PurchaseOrderLine:
    """
    Value Object representing a purchase order line item.
    Immutable and validated.
    """
    id: str
    product_id: str
    product_sku: str
    product_name: str
    quantity: int
    unit_price: Decimal
    total_price: Decimal
    received_quantity: int = 0
    rejected_quantity: int = 0
    expected_date: Optional[date] = None
    notes: str = ""
    
    def __post_init__(self):
        if self.quantity <= 0:
            raise ValueError("quantity must be positive")
        self.total_price = self.unit_price * self.quantity
    
    @property
    def is_fully_received(self) -> bool:
        return self.received_quantity >= self.quantity
    
    @property
    def is_partial(self) -> bool:
        return 0 < self.received_quantity < self.quantity
    
    @property
    def remaining_quantity(self) -> int:
        return max(0, self.quantity - self.received_quantity)
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "product_id": self.product_id,
            "product_sku": self.product_sku,
            "product_name": self.product_name,
            "quantity": self.quantity,
            "unit_price": str(self.unit_price),
            "total_price": str(self.total_price),
            "received_quantity": self.received_quantity,
            "rejected_quantity": self.rejected_quantity,
            "expected_date": self.expected_date.isoformat() if self.expected_date else None,
            "notes": self.notes,
            "is_fully_received": self.is_fully_received,
            "is_partial": self.is_partial,
            "remaining_quantity": self.remaining_quantity
        }


@dataclass(frozen=True)
class PurchaseOrder:
    """
    Purchase Order entity for managing supplier purchases.
    
    This entity follows Clean Architecture principles and is immutable.
    
    Attributes:
        id: Unique identifier
        order_number: Human-readable order number
        supplier_id: Supplier identifier
        supplier_name: Supplier name
        supplier_reference: Supplier's reference
        status: Current order status
        lines: Order line items
        subtotal: Subtotal amount
        tax_amount: Tax amount
        discount_amount: Discount amount
        total_amount: Total amount
        currency: Currency code
        expected_delivery: Expected delivery date
        actual_delivery: Actual delivery date
        payment_terms: Payment terms
        shipping_address: Delivery address
        billing_address: Billing address
        notes: Additional notes
        terms_conditions: Terms and conditions
        approved_by: Approver user ID
        approved_name: Approver name
        approved_at: Approval timestamp
        created_by: Creator user ID
        created_name: Creator name
        metadata: Additional metadata
        created_at: Creation timestamp
        updated_at: Last update timestamp
    """
    id: str
    order_number: str
    supplier_id: str
    supplier_name: str
    supplier_reference: str
    status: PurchaseOrderStatus
    lines: List[PurchaseOrderLine] = field(default_factory=list)
    subtotal: Decimal = field(default=Decimal("0"))
    tax_amount: Decimal = field(default=Decimal("0"))
    discount_amount: Decimal = field(default=Decimal("0"))
    total_amount: Decimal = field(default=Decimal("0"))
    currency: str = "USD"
    expected_delivery: Optional[date] = None
    actual_delivery: Optional[date] = None
    payment_terms: str = ""
    shipping_address: str = ""
    billing_address: str = ""
    notes: str = ""
    terms_conditions: str = ""
    approved_by: Optional[str] = None
    approved_name: Optional[str] = None
    approved_at: Optional[datetime] = None
    created_by: str = ""
    created_name: str = ""
    metadata: Dict[str, Any] = field(default_factory=dict)
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime = field(default_factory=datetime.utcnow)
    
    def __post_init__(self):
        if not self.order_number:
            raise ValueError("order_number cannot be empty")
        if not self.supplier_id:
            raise ValueError("supplier_id cannot be empty")
    
    @property
    def is_approved(self) -> bool:
        return self.status in [PurchaseOrderStatus.APPROVED, PurchaseOrderStatus.ORDERED]
    
    @property
    def is_received(self) -> bool:
        return self.status == PurchaseOrderStatus.RECEIVED
    
    @property
    def line_count(self) -> int:
        return len(self.lines)
    
    @property
    def total_items(self) -> int:
        return sum(line.quantity for line in self.lines)
    
    @property
    def received_items(self) -> int:
        return sum(line.received_quantity for line in self.lines)
    
    @property
    def delivery_status(self) -> DeliveryStatus:
        if self.received_items == 0:
            return DeliveryStatus.PENDING
        if self.received_items >= self.total_items:
            return DeliveryStatus.COMPLETE
        return DeliveryStatus.PARTIAL
    
    def calculate_totals(self, tax_rate: Decimal = Decimal("0"), discount: Decimal = Decimal("0")) -> None:
        """Calculate order totals."""
        self.subtotal = sum(line.total_price for line in self.lines)
        self.tax_amount = self.subtotal * tax_rate
        self.discount_amount = discount
        self.total_amount = self.subtotal + self.tax_amount - self.discount_amount
    
    def receive_line(self, line_id: str, quantity: int, rejected: int = 0) -> None:
        """Process receiving of goods for a line item."""
        for line in self.lines:
            if line.id == line_id:
                line.received_quantity += quantity
                line.rejected_quantity += rejected
                break
        
        if self.delivery_status == DeliveryStatus.COMPLETE:
            self.status = PurchaseOrderStatus.RECEIVED
            self.actual_delivery = date.today()
        elif self.delivery_status == DeliveryStatus.PARTIAL:
            self.status = PurchaseOrderStatus.PARTIALLY_RECEIVED
    
    def approve(self, user_id: str, user_name: str) -> None:
        """Approve the purchase order."""
        self.status = PurchaseOrderStatus.APPROVED
        self.approved_by = user_id
        self.approved_name = user_name
        self.approved_at = datetime.utcnow()
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "order_number": self.order_number,
            "supplier_id": self.supplier_id,
            "supplier_name": self.supplier_name,
            "supplier_reference": self.supplier_reference,
            "status": self.status.value,
            "lines": [line.to_dict() for line in self.lines],
            "subtotal": str(self.subtotal),
            "tax_amount": str(self.tax_amount),
            "discount_amount": str(self.discount_amount),
            "total_amount": str(self.total_amount),
            "currency": self.currency,
            "expected_delivery": self.expected_delivery.isoformat() if self.expected_delivery else None,
            "actual_delivery": self.actual_delivery.isoformat() if self.actual_delivery else None,
            "payment_terms": self.payment_terms,
            "shipping_address": self.shipping_address,
            "billing_address": self.billing_address,
            "notes": self.notes,
            "terms_conditions": self.terms_conditions,
            "approved_by": self.approved_by,
            "approved_name": self.approved_name,
            "approved_at": self.approved_at.isoformat() if self.approved_at else None,
            "created_by": self.created_by,
            "created_name": self.created_name,
            "metadata": self.metadata,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
            "is_approved": self.is_approved,
            "is_received": self.is_received,
            "line_count": self.line_count,
            "total_items": self.total_items,
            "received_items": self.received_items,
            "delivery_status": self.delivery_status.value
        }


class PurchaseOrderBuilder:
    """Builder for creating PurchaseOrder instances."""
    
    def __init__(self):
        self._id: Optional[str] = None
        self._order_number: Optional[str] = None
        self._supplier_id: Optional[str] = None
        self._supplier_name: str = ""
        self._supplier_reference: str = ""
        self._status: PurchaseOrderStatus = PurchaseOrderStatus.DRAFT
        self._lines: List[PurchaseOrderLine] = []
        self._subtotal: Decimal = Decimal("0")
        self._tax_amount: Decimal = Decimal("0")
        self._discount_amount: Decimal = Decimal("0")
        self._total_amount: Decimal = Decimal("0")
        self._currency: str = "USD"
        self._expected_delivery: Optional[date] = None
        self._payment_terms: str = ""
        self._shipping_address: str = ""
        self._billing_address: str = ""
        self._notes: str = ""
        self._terms_conditions: str = ""
        self._created_by: str = ""
        self._created_name: str = ""
        self._metadata: Dict[str, Any] = {}
    
    def with_id(self, order_id: str) -> "PurchaseOrderBuilder":
        self._id = order_id
        return self
    
    def with_order_number(self, order_number: str) -> "PurchaseOrderBuilder":
        self._order_number = order_number
        return self
    
    def from_supplier(self, supplier_id: str, supplier_name: str, supplier_reference: str = "") -> "PurchaseOrderBuilder":
        self._supplier_id = supplier_id
        self._supplier_name = supplier_name
        self._supplier_reference = supplier_reference
        return self
    
    def with_status(self, status: PurchaseOrderStatus) -> "PurchaseOrderBuilder":
        self._status = status
        return self
    
    def with_lines(self, lines: List[PurchaseOrderLine]) -> "PurchaseOrderBuilder":
        self._lines = lines
        return self
    
    def with_totals(self, subtotal: Decimal, tax: Decimal, discount: Decimal, total: Decimal) -> "PurchaseOrderBuilder":
        self._subtotal = subtotal
        self._tax_amount = tax
        self._discount_amount = discount
        self._total_amount = total
        return self
    
    def with_currency(self, currency: str) -> "PurchaseOrderBuilder":
        self._currency = currency
        return self
    
    def with_delivery(self, expected: date) -> "PurchaseOrderBuilder":
        self._expected_delivery = expected
        return self
    
    def with_payment_terms(self, terms: str) -> "PurchaseOrderBuilder":
        self._payment_terms = terms
        return self
    
    def with_addresses(self, shipping: str, billing: str) -> "PurchaseOrderBuilder":
        self._shipping_address = shipping
        self._billing_address = billing
        return self
    
    def with_notes(self, notes: str, terms: str = "") -> "PurchaseOrderBuilder":
        self._notes = notes
        self._terms_conditions = terms
        return self
    
    def created_by(self, user_id: str, user_name: str) -> "PurchaseOrderBuilder":
        self._created_by = user_id
        self._created_name = user_name
        return self
    
    def with_metadata(self, metadata: Dict[str, Any]) -> "PurchaseOrderBuilder":
        self._metadata = metadata
        return self
    
    def build(self) -> PurchaseOrder:
        if not self._id:
            self._id = str(uuid4())
        if not self._order_number:
            from time import time
            self._order_number = f"PO-{int(time())}"
        if not self._supplier_id:
            raise ValueError("supplier_id is required")
        
        return PurchaseOrder(
            id=self._id,
            order_number=self._order_number,
            supplier_id=self._supplier_id,
            supplier_name=self._supplier_name,
            supplier_reference=self._supplier_reference,
            status=self._status,
            lines=self._lines,
            subtotal=self._subtotal,
            tax_amount=self._tax_amount,
            discount_amount=self._discount_amount,
            total_amount=self._total_amount,
            currency=self._currency,
            expected_delivery=self._expected_delivery,
            payment_terms=self._payment_terms,
            shipping_address=self._shipping_address,
            billing_address=self._billing_address,
            notes=self._notes,
            terms_conditions=self._terms_conditions,
            created_by=self._created_by,
            created_name=self._created_name,
            metadata=self._metadata
        )


def create_purchase_order(
    supplier_id: str,
    supplier_name: str,
    **kwargs
) -> PurchaseOrder:
    """Factory function to create a purchase order."""
    builder = PurchaseOrderBuilder()
    builder.from_supplier(supplier_id, supplier_name, kwargs.get("supplier_reference", ""))
    
    if order_number := kwargs.get("order_number"):
        builder.with_order_number(order_number)
    if status := kwargs.get("status"):
        builder.with_status(status)
    if lines := kwargs.get("lines"):
        builder.with_lines(lines)
    if currency := kwargs.get("currency"):
        builder.with_currency(currency)
    if expected_delivery := kwargs.get("expected_delivery"):
        builder.with_delivery(expected_delivery)
    if payment_terms := kwargs.get("payment_terms"):
        builder.with_payment_terms(payment_terms)
    if shipping_address := kwargs.get("shipping_address"):
        billing_address = kwargs.get("billing_address", shipping_address)
        builder.with_addresses(shipping_address, billing_address)
    if notes := kwargs.get("notes"):
        terms = kwargs.get("terms_conditions", "")
        builder.with_notes(notes, terms)
    if created_by := kwargs.get("created_by"):
        created_name = kwargs.get("created_name", "")
        builder.created_by(created_by, created_name)
    if metadata := kwargs.get("metadata"):
        builder.with_metadata(metadata)
    
    return builder.build()


def create_purchase_order_line(
    product_id: str,
    product_sku: str,
    product_name: str,
    quantity: int,
    unit_price: Decimal,
    **kwargs
) -> PurchaseOrderLine:
    """Factory function to create a purchase order line."""
    return PurchaseOrderLine(
        id=str(uuid4()),
        product_id=product_id,
        product_sku=product_sku,
        product_name=product_name,
        quantity=quantity,
        unit_price=unit_price,
        expected_date=kwargs.get("expected_date"),
        notes=kwargs.get("notes", "")
    )
