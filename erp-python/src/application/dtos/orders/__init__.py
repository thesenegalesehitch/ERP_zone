"""
Application Layer - Order DTOs
Data Transfer Objects for Order operations.

Author: Alexandre Albert Ndour
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional, List
import uuid


@dataclass
class CreateOrderDTO:
    """DTO for creating a new order."""
    customer_id: uuid.UUID
    shipping_address_id: Optional[uuid.UUID] = None
    billing_address_id: Optional[uuid.UUID] = None
    customer_notes: Optional[str] = None


@dataclass
class CreateOrderLineDTO:
    """DTO for adding a line to an order."""
    product_id: uuid.UUID
    variant_id: Optional[uuid.UUID] = None
    quantity: int = 1
    unit_price: float = 0.0
    tax_rate: float = 0.0


@dataclass
class UpdateOrderStatusDTO:
    """DTO for updating order status."""
    status: str
    notes: Optional[str] = None


@dataclass
class OrderResponseDTO:
    """DTO for order response."""
    id: uuid.UUID
    order_number: str
    customer_id: uuid.UUID
    status: str
    payment_status: str
    shipping_status: str
    subtotal: float
    tax_amount: float
    shipping_amount: float
    discount_amount: float
    total: float
    currency: str
    order_date: datetime
    confirmed_date: Optional[datetime]
    shipped_date: Optional[datetime]
    delivered_date: Optional[datetime]
    cancelled_date: Optional[datetime]
    customer_notes: Optional[str]
    internal_notes: Optional[str]
    line_count: int
    item_count: int
    created_at: datetime
    updated_at: datetime


@dataclass
class OrderLineResponseDTO:
    """DTO for order line response."""
    id: uuid.UUID
    product_id: uuid.UUID
    variant_id: Optional[uuid.UUID]
    name: str
    sku: str
    quantity: int
    unit_price: float
    tax_rate: float
    discount_amount: float
    subtotal: float
    tax_amount: float
    total: float
    is_cancelled: bool


@dataclass
class OrderFilterDTO:
    """Filter parameters for order list."""
    customer_id: Optional[uuid.UUID] = None
    status: Optional[str] = None
    payment_status: Optional[str] = None
    shipping_status: Optional[str] = None
    date_from: Optional[datetime] = None
    date_to: Optional[datetime] = None
    search: Optional[str] = None


@dataclass
class PaginationParams:
    """Pagination parameters."""
    page: int = 1
    limit: int = 20
    sort_by: str = "created_at"
    sort_order: str = "desc"
    
    @property
    def offset(self) -> int:
        return (self.page - 1) * self.limit
