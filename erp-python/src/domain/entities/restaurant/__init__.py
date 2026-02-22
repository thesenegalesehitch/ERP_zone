"""
Restaurant Entity for ERP System.

This module provides entities for restaurant/food service management
following Clean Architecture principles.
"""

from dataclasses import dataclass, field
from datetime import datetime, date, time
from typing import Optional, Dict, Any, List
from enum import Enum
from uuid import uuid4
from decimal import Decimal


class TableStatus(str, Enum):
    """Table status enumeration."""
    AVAILABLE = "available"
    OCCUPIED = "occupied"
    RESERVED = "reserved"
    CLEANING = "cleaning"
    OUT_OF_SERVICE = "out_of_service"


class OrderStatus(str, Enum):
    """Order status enumeration."""
    PENDING = "pending"
    CONFIRMED = "confirmed"
    PREPARING = "preparing"
    READY = "ready"
    SERVED = "served"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


class ReservationStatus(str, Enum):
    """Reservation status enumeration."""
    PENDING = "pending"
    CONFIRMED = "confirmed"
    SEATED = "seated"
    COMPLETED = "completed"
    NO_SHOW = "no_show"
    CANCELLED = "cancelled"


@dataclass(frozen=True)
class MenuItem:
    """
    Value Object representing a menu item.
    Immutable and validated.
    """
    id: str
    name: str
    description: str
    price: Decimal
    category: str
    preparation_time_minutes: int
    is_available: bool = True
    allergens: List[str] = field(default_factory=list)
    dietary_info: List[str] = field(default_factory=list)
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "price": str(self.price),
            "category": self.category,
            "preparation_time_minutes": self.preparation_time_minutes,
            "is_available": self.is_available,
            "allergens": self.allergens,
            "dietary_info": self.dietary_info
        }


@dataclass(frozen=True)
class TableReservation:
    """
    Value Object representing a table reservation.
    Immutable and validated.
    """
    id: str
    customer_name: str
    customer_phone: str
    customer_email: str
    party_size: int
    reservation_date: date
    reservation_time: time
    table_id: str
    table_number: int
    status: ReservationStatus
    notes: str = ""
    created_at: datetime = field(default_factory=datetime.utcnow)
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "customer_name": self.customer_name,
            "customer_phone": self.customer_phone,
            "customer_email": self.customer_email,
            "party_size": self.party_size,
            "reservation_date": self.reservation_date.isoformat(),
            "reservation_time": self.reservation_time.isoformat(),
            "table_id": self.table_id,
            "table_number": self.table_number,
            "status": self.status.value,
            "notes": self.notes,
            "created_at": self.created_at.isoformat()
        }


@dataclass(frozen=True)
class RestaurantOrder:
    """
    Restaurant Order entity for managing restaurant orders.
    
    This entity follows Clean Architecture principles and is immutable.
    
    Attributes:
        id: Unique identifier
        order_number: Human-readable order number
        table_id: Table identifier
        table_number: Table number
        customer_name: Customer name
        status: Current order status
        order_type: Type of order (dine-in, takeout, delivery)
        items: List of ordered items
        subtotal: Subtotal amount
        tax_amount: Tax amount
        discount_amount: Discount amount
        total_amount: Total amount
        guest_count: Number of guests
        server_id: Server user ID
        server_name: Server name
        notes: Order notes
        metadata: Additional metadata
        created_at: Creation timestamp
        updated_at: Last update timestamp
    """
    id: str
    order_number: str
    table_id: Optional[str] = None
    table_number: Optional[int] = None
    customer_name: str = ""
    status: OrderStatus = OrderStatus.PENDING
    order_type: str = "dine_in"
    items: List[Dict[str, Any]] = field(default_factory=list)
    subtotal: Decimal = field(default=Decimal("0"))
    tax_amount: Decimal = field(default=Decimal("0"))
    discount_amount: Decimal = field(default=Decimal("0"))
    total_amount: Decimal = field(default=Decimal("0"))
    guest_count: int = 1
    server_id: Optional[str] = None
    server_name: str = ""
    notes: str = ""
    metadata: Dict[str, Any] = field(default_factory=dict)
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime = field(default_factory=datetime.utcnow)
    
    def __post_init__(self):
        if not self.order_number:
            raise ValueError("order_number cannot be empty")
    
    @property
    def is_active(self) -> bool:
        return self.status in [OrderStatus.PENDING, OrderStatus.CONFIRMED, OrderStatus.PREPARING, OrderStatus.READY]
    
    @property
    def is_completed(self) -> bool:
        return self.status in [OrderStatus.SERVED, OrderStatus.COMPLETED]
    
    @property
    def item_count(self) -> int:
        return sum(item.get("quantity", 1) for item in self.items)
    
    @property
    def unique_item_count(self) -> int:
        return len(self.items)
    
    @property
    def average_prep_time(self) -> int:
        if not self.items:
            return 0
        return sum(item.get("preparation_time", 0) for item in self.items) // len(self.items)
    
    def add_item(self, item: Dict[str, Any]) -> None:
        """Add an item to the order."""
        self.items.append(item)
        self.calculate_totals()
    
    def remove_item(self, item_id: str) -> None:
        """Remove an item from the order."""
        self.items = [item for item in self.items if item.get("id") != item_id]
        self.calculate_totals()
    
    def calculate_totals(self) -> None:
        """Calculate order totals."""
        self.subtotal = sum(
            Decimal(str(item.get("price", 0))) * item.get("quantity", 1)
            for item in self.items
        )
        tax_rate = Decimal("0.1")
        self.tax_amount = self.subtotal * tax_rate
        self.total_amount = self.subtotal + self.tax_amount - self.discount_amount
    
    def confirm(self) -> None:
        """Confirm the order."""
        self.status = OrderStatus.CONFIRMED
    
    def start_preparation(self) -> None:
        """Start preparing the order."""
        self.status = OrderStatus.PREPARING
    
    def mark_ready(self) -> None:
        """Mark order as ready."""
        self.status = OrderStatus.READY
    
    def serve(self) -> None:
        """Serve the order."""
        self.status = OrderStatus.SERVED
    
    def complete(self) -> None:
        """Complete the order."""
        self.status = OrderStatus.COMPLETED
    
    def cancel(self, reason: str) -> None:
        """Cancel the order."""
        self.status = OrderStatus.CANCELLED
        self.notes += f"\n[CANCELLED: {reason}]"
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "order_number": self.order_number,
            "table_id": self.table_id,
            "table_number": self.table_number,
            "customer_name": self.customer_name,
            "status": self.status.value,
            "order_type": self.order_type,
            "items": self.items,
            "subtotal": str(self.subtotal),
            "tax_amount": str(self.tax_amount),
            "discount_amount": str(self.discount_amount),
            "total_amount": str(self.total_amount),
            "guest_count": self.guest_count,
            "server_id": self.server_id,
            "server_name": self.server_name,
            "notes": self.notes,
            "metadata": self.metadata,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
            "is_active": self.is_active,
            "is_completed": self.is_completed,
            "item_count": self.item_count,
            "unique_item_count": self.unique_item_count,
            "average_prep_time": self.average_prep_time
        }


class RestaurantOrderBuilder:
    """Builder for creating RestaurantOrder instances."""
    
    def __init__(self):
        self._id: Optional[str] = None
        self._order_number: Optional[str] = None
        self._table_id: Optional[str] = None
        self._table_number: Optional[int] = None
        self._customer_name: str = ""
        self._status: OrderStatus = OrderStatus.PENDING
        self._order_type: str = "dine_in"
        self._items: List[Dict[str, Any]] = []
        self._discount_amount: Decimal = Decimal("0")
        self._guest_count: int = 1
        self._server_id: Optional[str] = None
        self._server_name: str = ""
        self._notes: str = ""
        self._metadata: Dict[str, Any] = {}
    
    def with_id(self, order_id: str) -> "RestaurantOrderBuilder":
        self._id = order_id
        return self
    
    def with_order_number(self, order_number: str) -> "RestaurantOrderBuilder":
        self._order_number = order_number
        return self
    
    def at_table(self, table_id: str, table_number: int) -> "RestaurantOrderBuilder":
        self._table_id = table_id
        self._table_number = table_number
        return self
    
    def for_customer(self, customer_name: str) -> "RestaurantOrderBuilder":
        self._customer_name = customer_name
        return self
    
    def with_status(self, status: OrderStatus) -> "RestaurantOrderBuilder":
        self._status = status
        return self
    
    def with_order_type(self, order_type: str) -> "RestaurantOrderBuilder":
        self._order_type = order_type
        return self
    
    def with_items(self, items: List[Dict[str, Any]]) -> "RestaurantOrderBuilder":
        self._items = items
        return self
    
    def with_discount(self, amount: Decimal) -> "RestaurantOrderBuilder":
        self._discount_amount = amount
        return self
    
    def with_guests(self, count: int) -> "RestaurantOrderBuilder":
        self._guest_count = count
        return self
    
    def served_by(self, server_id: str, server_name: str) -> "RestaurantOrderBuilder":
        self._server_id = server_id
        self._server_name = server_name
        return self
    
    def with_notes(self, notes: str) -> "RestaurantOrderBuilder":
        self._notes = notes
        return self
    
    def with_metadata(self, metadata: Dict[str, Any]) -> "RestaurantOrderBuilder":
        self._metadata = metadata
        return self
    
    def build(self) -> RestaurantOrder:
        if not self._id:
            self._id = str(uuid4())
        if not self._order_number:
            from time import time
            self._order_number = f"ORD-{int(time())}"
        
        order = RestaurantOrder(
            id=self._id,
            order_number=self._order_number,
            table_id=self._table_id,
            table_number=self._table_number,
            customer_name=self._customer_name,
            status=self._status,
            order_type=self._order_type,
            items=self._items,
            discount_amount=self._discount_amount,
            guest_count=self._guest_count,
            server_id=self._server_id,
            server_name=self._server_name,
            notes=self._notes,
            metadata=self._metadata
        )
        
        order.calculate_totals()
        return order


def create_restaurant_order(**kwargs) -> RestaurantOrder:
    """Factory function to create a restaurant order."""
    builder = RestaurantOrderBuilder()
    
    if order_number := kwargs.get("order_number"):
        builder.with_order_number(order_number)
    if table_id := kwargs.get("table_id"):
        table_number = kwargs.get("table_number", 1)
        builder.at_table(table_id, table_number)
    if customer_name := kwargs.get("customer_name"):
        builder.for_customer(customer_name)
    if status := kwargs.get("status"):
        builder.with_status(status)
    if order_type := kwargs.get("order_type"):
        builder.with_order_type(order_type)
    if items := kwargs.get("items"):
        builder.with_items(items)
    if discount_amount := kwargs.get("discount_amount"):
        builder.with_discount(discount_amount)
    if guest_count := kwargs.get("guest_count"):
        builder.with_guests(guest_count)
    if server_id := kwargs.get("server_id"):
        server_name = kwargs.get("server_name", "")
        builder.served_by(server_id, server_name)
    if notes := kwargs.get("notes"):
        builder.with_notes(notes)
    if metadata := kwargs.get("metadata"):
        builder.with_metadata(metadata)
    
    return builder.build()


def create_menu_item(
    name: str,
    description: str,
    price: Decimal,
    category: str,
    preparation_time_minutes: int,
    **kwargs
) -> MenuItem:
    """Factory function to create a menu item."""
    return MenuItem(
        id=str(uuid4()),
        name=name,
        description=description,
        price=price,
        category=category,
        preparation_time_minutes=preparation_time_minutes,
        is_available=kwargs.get("is_available", True),
        allergens=kwargs.get("allergens", []),
        dietary_info=kwargs.get("dietary_info", [])
    )


def create_table_reservation(
    customer_name: str,
    customer_phone: str,
    party_size: int,
    reservation_date: date,
    reservation_time: time,
    table_id: str,
    table_number: int,
    **kwargs
) -> TableReservation:
    """Factory function to create a table reservation."""
    return TableReservation(
        id=str(uuid4()),
        customer_name=customer_name,
        customer_phone=customer_phone,
        customer_email=kwargs.get("customer_email", ""),
        party_size=party_size,
        reservation_date=reservation_date,
        reservation_time=reservation_time,
        table_id=table_id,
        table_number=table_number,
        status=kwargs.get("status", ReservationStatus.PENDING),
        notes=kwargs.get("notes", "")
    )
