"""
Application Layer - Invoice DTOs
Data Transfer Objects for Invoice operations.

Author: Alexandre Albert Ndour
"""

from dataclasses import dataclass
from datetime import datetime
from typing import Optional, List
import uuid


@dataclass
class CreateInvoiceDTO:
    """DTO for creating a new invoice."""
    customer_id: uuid.UUID
    invoice_type: str = "standard"
    order_id: Optional[uuid.UUID] = None
    due_days: int = 30
    customer_notes: Optional[str] = None
    terms: Optional[str] = None


@dataclass
class CreateInvoiceLineDTO:
    """DTO for adding a line to an invoice."""
    product_id: Optional[uuid.UUID] = None
    description: str
    quantity: float = 1.0
    unit_price: float = 0.0
    tax_rate: float = 0.0
    discount_percent: float = 0.0
    discount_amount: float = 0.0


@dataclass
class RecordPaymentDTO:
    """DTO for recording a payment."""
    amount: float
    payment_method: Optional[str] = None
    reference: Optional[str] = None


@dataclass
class InvoiceResponseDTO:
    """DTO for invoice response."""
    id: uuid.UUID
    invoice_number: str
    invoice_type: str
    customer_id: uuid.UUID
    order_id: Optional[uuid.UUID]
    status: str
    issue_date: datetime
    due_date: datetime
    sent_date: Optional[datetime]
    paid_date: Optional[datetime]
    subtotal: float
    tax_amount: float
    discount_amount: float
    total: float
    amount_paid: float
    amount_due: float
    currency: str
    is_overdue: bool
    days_until_due: int
    created_at: datetime
    updated_at: datetime


@dataclass
class InvoiceLineResponseDTO:
    """DTO for invoice line response."""
    id: uuid.UUID
    product_id: Optional[uuid.UUID]
    description: str
    quantity: float
    unit_price: float
    tax_rate: float
    discount_percent: float
    discount_amount: float
    subtotal: float
    tax_amount: float
    total: float


@dataclass
class InvoiceFilterDTO:
    """Filter parameters for invoice list."""
    customer_id: Optional[uuid.UUID] = None
    status: Optional[str] = None
    invoice_type: Optional[str] = None
    date_from: Optional[datetime] = None
    date_to: Optional[datetime] = None
    overdue_only: bool = False
    unpaid_only: bool = False


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
