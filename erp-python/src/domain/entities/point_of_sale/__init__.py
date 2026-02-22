"""
Point of Sale Entity for ERP System.

This module provides entities for POS/Retail management
following Clean Architecture principles.
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional, Dict, Any, List
from enum import Enum
from uuid import uuid4
from decimal import Decimal


class POSOrderStatus(str, Enum):
    """POS order status enumeration."""
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    VOIDED = "voided"
    REFUNDED = "refunded"
    PARTIALLY_REFUNDED = "partially_refunded"


class PaymentMethod(str, Enum):
    """Payment method enumeration."""
    CASH = "cash"
    CREDIT_CARD = "credit_card"
    DEBIT_CARD = "debit_card"
    MOBILE_MONEY = "mobile_money"
    GIFT_CARD = "gift_card"
    LOYALTY_POINTS = "loyalty_points"
    BANK_TRANSFER = "bank_transfer"


class OrderType(str, Enum):
    """Order type enumeration."""
    DINE_IN = "dine_in"
    TAKEAWAY = "takeaway"
    DELIVERY = "delivery"
    ONLINE = "online"


@dataclass(frozen=True)
class POSLineItem:
    """
    Value Object representing a POS line item.
    Immutable and validated.
    """
    id: str
    product_id: str
    product_sku: str
    product_name: str
    quantity: int
    unit_price: Decimal
    discount_percentage: Decimal = field(default=Decimal("0"))
    tax_percentage: Decimal = field(default=Decimal("0"))
    line_total: Decimal = field(default=Decimal("0"))
    notes: str = ""
    
    def __post_init__(self):
        if self.quantity <= 0:
            raise ValueError("quantity must be positive")
        
        subtotal = self.unit_price * self.quantity
        discount = subtotal * (self.discount_percentage / Decimal("100"))
        after_discount = subtotal - discount
        tax = after_discount * (self.tax_percentage / Decimal("100"))
        self.line_total = after_discount + tax
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "product_id": self.product_id,
            "product_sku": self.product_sku,
            "product_name": self.product_name,
            "quantity": self.quantity,
            "unit_price": str(self.unit_price),
            "discount_percentage": str(self.discount_percentage),
            "tax_percentage": str(self.tax_percentage),
            "line_total": str(self.line_total),
            "notes": self.notes
        }


@dataclass(frozen=True)
class POSPayment:
    """
    Value Object representing a payment.
    Immutable and validated.
    """
    id: str
    payment_method: PaymentMethod
    amount: Decimal
    reference: str = ""
    card_last_four: str = ""
    card_brand: str = ""
    transaction_id: str = ""
    notes: str = ""
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "payment_method": self.payment_method.value,
            "amount": str(self.amount),
            "reference": self.reference,
            "card_last_four": self.card_last_four,
            "card_brand": self.card_brand,
            "transaction_id": self.transaction_id,
            "notes": self.notes
        }


@dataclass(frozen=True)
class POSOrder:
    """
    POS Order entity for retail/Point of Sale transactions.
    
    This entity follows Clean Architecture principles and is immutable.
    
    Attributes:
        id: Unique identifier
        order_number: Human-readable order number
        register_id: Register/terminal ID
        register_name: Register name
        order_type: Type of order
        status: Current order status
        customer_id: Customer identifier
        customer_name: Customer name
        items: Line items
        subtotal: Subtotal amount
        discount_amount: Total discount
        tax_amount: Total tax
        total_amount: Total amount
        payments: Payment list
        total_paid: Total amount paid
        change_due: Change due
        loyalty_points_earned: Points earned
        loyalty_points_redeemed: Points redeemed
        notes: Order notes
        created_by: Cashier user ID
        created_name: Cashier name
        metadata: Additional metadata
        created_at: Creation timestamp
        updated_at: Last update timestamp
    """
    id: str
    order_number: str
    register_id: str
    register_name: str
    order_type: OrderType
    status: POSOrderStatus
    customer_id: Optional[str] = None
    customer_name: str = ""
    items: List[POSLineItem] = field(default_factory=list)
    subtotal: Decimal = field(default=Decimal("0"))
    discount_amount: Decimal = field(default=Decimal("0"))
    tax_amount: Decimal = field(default=Decimal("0"))
    total_amount: Decimal = field(default=Decimal("0"))
    payments: List[POSPayment] = field(default_factory=list)
    total_paid: Decimal = field(default=Decimal("0"))
    change_due: Decimal = field(default=Decimal("0"))
    loyalty_points_earned: int = 0
    loyalty_points_redeemed: int = 0
    notes: str = ""
    created_by: str = ""
    created_name: str = ""
    metadata: Dict[str, Any] = field(default_factory=dict)
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime = field(default_factory=datetime.utcnow)
    
    def __post_init__(self):
        if not self.order_number:
            raise ValueError("order_number cannot be empty")
    
    @property
    def is_completed(self) -> bool:
        return self.status == POSOrderStatus.COMPLETED
    
    @property
    def is_pending(self) -> bool:
        return self.status == POSOrderStatus.PENDING
    
    @property
    def is_paid(self) -> bool:
        return self.total_paid >= self.total_amount
    
    @property
    def item_count(self) -> int:
        return sum(item.quantity for item in self.items)
    
    @property
    def unique_item_count(self) -> int:
        return len(self.items)
    
    def calculate_totals(self) -> None:
        """Calculate order totals."""
        self.subtotal = sum(item.line_total for item in self.items)
        
        item_discounts = sum(
            item.unit_price * item.quantity * (item.discount_percentage / Decimal("100"))
            for item in self.items
        )
        order_discount = self.discount_amount
        
        self.tax_amount = sum(
            (item.line_total - (item.unit_price * item.quantity * item.discount_percentage / Decimal("100"))) *
            (item.tax_percentage / Decimal("100"))
            for item in self.items
        )
        
        self.total_amount = self.subtotal - item_discounts - order_discount
        self.total_paid = sum(p.amount for p in self.payments)
        self.change_due = max(Decimal("0"), self.total_paid - self.total_amount)
    
    def add_item(self, item: POSLineItem) -> None:
        """Add an item to the order."""
        self.items.append(item)
        self.calculate_totals()
    
    def remove_item(self, item_id: str) -> None:
        """Remove an item from the order."""
        self.items = [item for item in self.items if item.id != item_id]
        self.calculate_totals()
    
    def add_payment(self, payment: POSPayment) -> None:
        """Add a payment to the order."""
        self.payments.append(payment)
        self.calculate_totals()
        
        if self.is_paid:
            self.status = POSOrderStatus.COMPLETED
    
    def void(self, reason: str) -> None:
        """Void the order."""
        self.status = POSOrderStatus.VOIDED
        self.notes += f"\n[VOIDED: {reason}]"
    
    def refund(self, amount: Decimal, reason: str) -> None:
        """Process a refund."""
        if amount >= self.total_amount:
            self.status = POSOrderStatus.REFUNDED
        else:
            self.status = POSOrderStatus.PARTIALLY_REFUNDED
        self.notes += f"\n[REFUND: {amount}] - {reason}"
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "order_number": self.order_number,
            "register_id": self.register_id,
            "register_name": self.register_name,
            "order_type": self.order_type.value,
            "status": self.status.value,
            "customer_id": self.customer_id,
            "customer_name": self.customer_name,
            "items": [item.to_dict() for item in self.items],
            "subtotal": str(self.subtotal),
            "discount_amount": str(self.discount_amount),
            "tax_amount": str(self.tax_amount),
            "total_amount": str(self.total_amount),
            "payments": [p.to_dict() for p in self.payments],
            "total_paid": str(self.total_paid),
            "change_due": str(self.change_due),
            "loyalty_points_earned": self.loyalty_points_earned,
            "loyalty_points_redeemed": self.loyalty_points_redeemed,
            "notes": self.notes,
            "created_by": self.created_by,
            "created_name": self.created_name,
            "metadata": self.metadata,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
            "is_completed": self.is_completed,
            "is_pending": self.is_pending,
            "is_paid": self.is_paid,
            "item_count": self.item_count,
            "unique_item_count": self.unique_item_count
        }


class POSOrderBuilder:
    """Builder for creating POSOrder instances."""
    
    def __init__(self):
        self._id: Optional[str] = None
        self._order_number: Optional[str] = None
        self._register_id: Optional[str] = None
        self._register_name: str = ""
        self._order_type: OrderType = OrderType.DINE_IN
        self._status: POSOrderStatus = POSOrderStatus.PENDING
        self._customer_id: Optional[str] = None
        self._customer_name: str = ""
        self._items: List[POSLineItem] = []
        self._discount_amount: Decimal = Decimal("0")
        self._payments: List[POSPayment] = []
        self._loyalty_points_earned: int = 0
        self._loyalty_points_redeemed: int = 0
        self._notes: str = ""
        self._created_by: str = ""
        self._created_name: str = ""
        self._metadata: Dict[str, Any] = {}
    
    def with_id(self, order_id: str) -> "POSOrderBuilder":
        self._id = order_id
        return self
    
    def with_order_number(self, order_number: str) -> "POSOrderBuilder":
        self._order_number = order_number
        return self
    
    def at_register(self, register_id: str, register_name: str) -> "POSOrderBuilder":
        self._register_id = register_id
        self._register_name = register_name
        return self
    
    def with_order_type(self, order_type: OrderType) -> "POSOrderBuilder":
        self._order_type = order_type
        return self
    
    def with_status(self, status: POSOrderStatus) -> "POSOrderBuilder":
        self._status = status
        return self
    
    def for_customer(self, customer_id: str, customer_name: str) -> "POSOrderBuilder":
        self._customer_id = customer_id
        self._customer_name = customer_name
        return self
    
    def with_items(self, items: List[POSLineItem]) -> "POSOrderBuilder":
        self._items = items
        return self
    
    def with_discount(self, amount: Decimal) -> "POSOrderBuilder":
        self._discount_amount = amount
        return self
    
    def with_payments(self, payments: List[POSPayment]) -> "POSOrderBuilder":
        self._payments = payments
        return self
    
    def with_loyalty(self, earned: int, redeemed: int) -> "POSOrderBuilder":
        self._loyalty_points_earned = earned
        self._loyalty_points_redeemed = redeemed
        return self
    
    def with_notes(self, notes: str) -> "POSOrderBuilder":
        self._notes = notes
        return self
    
    def created_by(self, user_id: str, user_name: str) -> "POSOrderBuilder":
        self._created_by = user_id
        self._created_name = user_name
        return self
    
    def with_metadata(self, metadata: Dict[str, Any]) -> "POSOrderBuilder":
        self._metadata = metadata
        return self
    
    def build(self) -> POSOrder:
        if not self._id:
            self._id = str(uuid4())
        if not self._order_number:
            from time import time
            self._order_number = f"POS-{int(time())}"
        if not self._register_id:
            raise ValueError("register_id is required")
        
        order = POSOrder(
            id=self._id,
            order_number=self._order_number,
            register_id=self._register_id,
            register_name=self._register_name,
            order_type=self._order_type,
            status=self._status,
            customer_id=self._customer_id,
            customer_name=self._customer_name,
            items=self._items,
            discount_amount=self._discount_amount,
            payments=self._payments,
            loyalty_points_earned=self._loyalty_points_earned,
            loyalty_points_redeemed=self._loyalty_points_redeemed,
            notes=self._notes,
            created_by=self._created_by,
            created_name=self._created_name,
            metadata=self._metadata
        )
        
        order.calculate_totals()
        return order


def create_pos_order(
    register_id: str,
    register_name: str,
    **kwargs
) -> POSOrder:
    """Factory function to create a POS order."""
    builder = POSOrderBuilder()
    builder.at_register(register_id, register_name)
    
    if order_number := kwargs.get("order_number"):
        builder.with_order_number(order_number)
    if order_type := kwargs.get("order_type"):
        builder.with_order_type(order_type)
    if status := kwargs.get("status"):
        builder.with_status(status)
    if customer_id := kwargs.get("customer_id"):
        customer_name = kwargs.get("customer_name", "")
        builder.for_customer(customer_id, customer_name)
    if items := kwargs.get("items"):
        builder.with_items(items)
    if discount_amount := kwargs.get("discount_amount"):
        builder.with_discount(discount_amount)
    if payments := kwargs.get("payments"):
        builder.with_payments(payments)
    if earned := kwargs.get("loyalty_points_earned"):
        redeemed = kwargs.get("loyalty_points_redeemed", 0)
        builder.with_loyalty(earned, redeemed)
    if notes := kwargs.get("notes"):
        builder.with_notes(notes)
    if created_by := kwargs.get("created_by"):
        created_name = kwargs.get("created_name", "")
        builder.created_by(created_by, created_name)
    if metadata := kwargs.get("metadata"):
        builder.with_metadata(metadata)
    
    return builder.build()


def create_pos_line_item(
    product_id: str,
    product_sku: str,
    product_name: str,
    quantity: int,
    unit_price: Decimal,
    **kwargs
) -> POSLineItem:
    """Factory function to create a POS line item."""
    return POSLineItem(
        id=str(uuid4()),
        product_id=product_id,
        product_sku=product_sku,
        product_name=product_name,
        quantity=quantity,
        unit_price=unit_price,
        discount_percentage=kwargs.get("discount_percentage", Decimal("0")),
        tax_percentage=kwargs.get("tax_percentage", Decimal("0")),
        notes=kwargs.get("notes", "")
    )


def create_pos_payment(
    payment_method: PaymentMethod,
    amount: Decimal,
    **kwargs
) -> POSPayment:
    """Factory function to create a POS payment."""
    return POSPayment(
        id=str(uuid4()),
        payment_method=payment_method,
        amount=amount,
        reference=kwargs.get("reference", ""),
        card_last_four=kwargs.get("card_last_four", ""),
        card_brand=kwargs.get("card_brand", ""),
        transaction_id=kwargs.get("transaction_id", ""),
        notes=kwargs.get("notes", "")
    )
