"""
Quote Entity for ERP System.

This module provides the Quote entity for managing sales quotes
following Clean Architecture principles.
"""

from dataclasses import dataclass, field
from datetime import datetime, date, timedelta
from typing import Optional, Dict, Any, List
from enum import Enum
from decimal import Decimal


class QuoteStatus(str, Enum):
    """Quote status enumeration."""
    DRAFT = "draft"
    SENT = "sent"
    VIEWED = "viewed"
    ACCEPTED = "accepted"
    REJECTED = "rejected"
    EXPIRED = "expired"
    CONVERTED = "converted"
    CANCELLED = "cancelled"


class QuotePriority(str, Enum):
    """Quote priority enumeration."""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    URGENT = "urgent"


@dataclass(frozen=True)
class QuoteLine:
    """
    Value Object representing a line item in a quote.
    Immutable and validated.
    """
    id: str
    product_id: str
    product_name: str
    description: str
    quantity: int
    unit_price: Decimal
    discount_percent: Decimal = field(default=Decimal("0"))
    tax_percent: Decimal = field(default=Decimal("0"))
    notes: Optional[str] = None
    
    def __post_init__(self):
        if self.quantity <= 0:
            raise ValueError("quantity must be positive")
        if self.unit_price < 0:
            raise ValueError("unit_price cannot be negative")
        if self.discount_percent < 0 or self.discount_percent > 100:
            raise ValueError("discount_percent must be between 0 and 100")
        if self.tax_percent < 0 or self.tax_percent > 100:
            raise ValueError("tax_percent must be between 0 and 100")
    
    @property
    def subtotal(self) -> Decimal:
        """Calculate subtotal before tax and discount."""
        return self.unit_price * self.quantity
    
    @property
    def discount_amount(self) -> Decimal:
        """Calculate discount amount."""
        return self.subtotal * (self.discount_percent / 100)
    
    @property
    def after_discount(self) -> Decimal:
        """Calculate amount after discount."""
        return self.subtotal - self.discount_amount
    
    @property
    def tax_amount(self) -> Decimal:
        """Calculate tax amount."""
        return self.after_discount * (self.tax_percent / 100)
    
    @property
    def total(self) -> Decimal:
        """Calculate total including tax."""
        return self.after_discount + self.tax_amount
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert quote line to dictionary."""
        return {
            "id": self.id,
            "product_id": self.product_id,
            "product_name": self.product_name,
            "description": self.description,
            "quantity": self.quantity,
            "unit_price": str(self.unit_price),
            "discount_percent": str(self.discount_percent),
            "tax_percent": str(self.tax_percent),
            "notes": self.notes,
            "subtotal": str(self.subtotal),
            "discount_amount": str(self.discount_amount),
            "after_discount": str(self.after_discount),
            "tax_amount": str(self.tax_amount),
            "total": str(self.total)
        }


@dataclass(frozen=True)
class Quote:
    """
    Quote entity representing a sales quote in the ERP system.
    
    This entity follows Clean Architecture principles and is immutable.
    
    Attributes:
        id: Unique identifier for the quote
        quote_number: Human-readable quote number
        customer_id: ID of the customer
        customer_name: Name of the customer
        contact_email: Contact email for the quote
        contact_phone: Contact phone for the quote
        valid_until: Date until quote is valid
        status: Current status of the quote
        priority: Priority level of the quote
        lines: List of quote line items
        subtotal: Subtotal before tax and discount
        discount_percent: Overall discount percentage
        discount_amount: Overall discount amount
        tax_percent: Overall tax percentage
        tax_amount: Tax amount
        total: Total amount after all adjustments
        currency: Currency code
        terms_and_conditions: Quote terms and conditions
        notes: Additional notes
        converted_to_order_id: ID if converted to order
        created_by: User who created the quote
        assigned_to: User assigned to follow up
        metadata: Additional metadata
        created_at: Timestamp when created
        updated_at: Timestamp when last updated
    """
    id: str
    quote_number: str
    customer_id: str
    customer_name: str
    contact_email: str
    contact_phone: Optional[str]
    valid_until: date
    status: QuoteStatus
    priority: QuotePriority
    lines: List[QuoteLine]
    discount_percent: Decimal = field(default=Decimal("0"))
    tax_percent: Decimal = field(default=Decimal("0"))
    terms_and_conditions: Optional[str] = None
    notes: Optional[str] = None
    converted_to_order_id: Optional[str] = None
    created_by: Optional[str] = None
    assigned_to: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime = field(default_factory=datetime.utcnow)
    
    def __post_init__(self):
        """Validate quote after initialization."""
        if not self.quote_number:
            raise ValueError("quote_number cannot be empty")
        if not self.customer_id:
            raise ValueError("customer_id cannot be empty")
        if not self.customer_name:
            raise ValueError("customer_name cannot be empty")
        if not self.lines:
            raise ValueError("quote must have at least one line")
        if self.valid_until < date.today():
            raise ValueError("valid_until cannot be in the past")
    
    @property
    def subtotal(self) -> Decimal:
        """Calculate subtotal from all lines."""
        return sum(line.subtotal for line in self.lines)
    
    @property
    def total_discount(self) -> Decimal:
        """Calculate total discount from all lines plus overall discount."""
        line_discounts = sum(line.discount_amount for line in self.lines)
        overall_discount = self.subtotal * (self.discount_percent / 100)
        return line_discounts + overall_discount
    
    @property
    def after_discount(self) -> Decimal:
        """Calculate amount after all discounts."""
        return self.subtotal - self.total_discount
    
    @property
    def total_tax(self) -> Decimal:
        """Calculate total tax from all lines plus overall tax."""
        line_taxes = sum(line.tax_amount for line in self.lines)
        overall_tax = self.after_discount * (self.tax_percent / 100)
        return line_taxes + overall_tax
    
    @property
    def total(self) -> Decimal:
        """Calculate final total."""
        return self.after_discount + self.total_tax
    
    @property
    def is_valid(self) -> bool:
        """Check if quote is still valid."""
        return self.valid_until >= date.today() and self.status not in [
            QuoteStatus.EXPIRED, QuoteStatus.CANCELLED, QuoteStatus.REJECTED
        ]
    
    @property
    def is_expired(self) -> bool:
        """Check if quote has expired."""
        return self.valid_until < date.today()
    
    @property
    def days_until_expiry(self) -> int:
        """Get days until quote expires."""
        delta = self.valid_until - date.today()
        return max(0, delta.days)
    
    @property
    def line_count(self) -> int:
        """Get number of lines in quote."""
        return len(self.lines)
    
    @property
    def item_count(self) -> int:
        """Get total quantity of items in quote."""
        return sum(line.quantity for line in self.lines)
    
    def can_convert_to_order(self) -> bool:
        """Check if quote can be converted to an order."""
        return (
            self.is_valid
            and self.status in [QuoteStatus.ACCEPTED, QuoteStatus.SENT]
            and not self.converted_to_order_id
        )
    
    def can_be_cancelled(self) -> bool:
        """Check if quote can be cancelled."""
        return self.status not in [
            QuoteStatus.CONVERTED, QuoteStatus.CANCELLED
        ]
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert quote to dictionary."""
        return {
            "id": self.id,
            "quote_number": self.quote_number,
            "customer_id": self.customer_id,
            "customer_name": self.customer_name,
            "contact_email": self.contact_email,
            "contact_phone": self.contact_phone,
            "valid_until": self.valid_until.isoformat(),
            "status": self.status.value,
            "priority": self.priority.value,
            "lines": [line.to_dict() for line in self.lines],
            "subtotal": str(self.subtotal),
            "discount_percent": str(self.discount_percent),
            "total_discount": str(self.total_discount),
            "tax_percent": str(self.tax_percent),
            "total_tax": str(self.total_tax),
            "total": str(self.total),
            "terms_and_conditions": self.terms_and_conditions,
            "notes": self.notes,
            "converted_to_order_id": self.converted_to_order_id,
            "created_by": self.created_by,
            "assigned_to": self.assigned_to,
            "metadata": self.metadata,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
            "is_valid": self.is_valid,
            "is_expired": self.is_expired,
            "days_until_expiry": self.days_until_expiry,
            "line_count": self.line_count,
            "item_count": self.item_count
        }


class QuoteBuilder:
    """Builder for creating Quote instances."""
    
    def __init__(self):
        self._id: Optional[str] = None
        self._quote_number: Optional[str] = None
        self._customer_id: Optional[str] = None
        self._customer_name: Optional[str] = None
        self._contact_email: str = ""
        self._contact_phone: Optional[str] = None
        self._valid_until: Optional[date] = None
        self._status: QuoteStatus = QuoteStatus.DRAFT
        self._priority: QuotePriority = QuotePriority.MEDIUM
        self._lines: List[QuoteLine] = []
        self._discount_percent: Decimal = Decimal("0")
        self._tax_percent: Decimal = Decimal("0")
        self._terms_and_conditions: Optional[str] = None
        self._notes: Optional[str] = None
        self._created_by: Optional[str] = None
        self._assigned_to: Optional[str] = None
        self._metadata: Dict[str, Any] = {}
    
    def with_id(self, quote_id: str) -> "QuoteBuilder":
        self._id = quote_id
        return self
    
    def with_quote_number(self, number: str) -> "QuoteBuilder":
        self._quote_number = number
        return self
    
    def for_customer(self, customer_id: str, customer_name: str) -> "QuoteBuilder":
        self._customer_id = customer_id
        self._customer_name = customer_name
        return self
    
    def with_contact(self, email: str, phone: Optional[str] = None) -> "QuoteBuilder":
        self._contact_email = email
        self._contact_phone = phone
        return self
    
    def valid_until(self, valid_until: date) -> "QuoteBuilder":
        self._valid_until = valid_until
        return self
    
    def with_status(self, status: QuoteStatus) -> "QuoteBuilder":
        self._status = status
        return self
    
    def with_priority(self, priority: QuotePriority) -> "QuoteBuilder":
        self._priority = priority
        return self
    
    def with_lines(self, lines: List[QuoteLine]) -> "QuoteBuilder":
        self._lines = lines
        return self
    
    def add_line(self, line: QuoteLine) -> "QuoteBuilder":
        self._lines.append(line)
        return self
    
    def with_discount(self, discount_percent: Decimal) -> "QuoteBuilder":
        self._discount_percent = discount_percent
        return self
    
    def with_tax(self, tax_percent: Decimal) -> "QuoteBuilder":
        self._tax_percent = tax_percent
        return self
    
    def with_terms(self, terms: str) -> "QuoteBuilder":
        self._terms_and_conditions = terms
        return self
    
    def with_notes(self, notes: str) -> "QuoteBuilder":
        self._notes = notes
        return self
    
    def created_by(self, user_id: str) -> "QuoteBuilder":
        self._created_by = user_id
        return self
    
    def assigned_to(self, user_id: str) -> "QuoteBuilder":
        self._assigned_to = user_id
        return self
    
    def with_metadata(self, metadata: Dict[str, Any]) -> "QuoteBuilder":
        self._metadata = metadata
        return self
    
    def build(self) -> Quote:
        from uuid import uuid4
        
        if not self._id:
            self._id = str(uuid4())
        if not self._quote_number:
            from time import time
            self._quote_number = f"QTE-{int(time())}"
        if not self._customer_id:
            raise ValueError("customer_id is required")
        if not self._customer_name:
            raise ValueError("customer_name is required")
        if not self._lines:
            raise ValueError("quote must have at least one line")
        if not self._valid_until:
            self._valid_until = date.today() + timedelta(days=30)
        
        return Quote(
            id=self._id,
            quote_number=self._quote_number,
            customer_id=self._customer_id,
            customer_name=self._customer_name,
            contact_email=self._contact_email,
            contact_phone=self._contact_phone,
            valid_until=self._valid_until,
            status=self._status,
            priority=self._priority,
            lines=self._lines,
            discount_percent=self._discount_percent,
            tax_percent=self._tax_percent,
            terms_and_conditions=self._terms_and_conditions,
            notes=self._notes,
            created_by=self._created_by,
            assigned_to=self._assigned_to,
            metadata=self._metadata
        )


# Factory functions
def create_quote_line(
    product_id: str,
    product_name: str,
    quantity: int,
    unit_price: Decimal,
    **kwargs
) -> QuoteLine:
    """Factory function to create a quote line."""
    from uuid import uuid4
    
    return QuoteLine(
        id=str(uuid4()),
        product_id=product_id,
        product_name=product_name,
        description=kwargs.get("description", ""),
        quantity=quantity,
        unit_price=unit_price,
        discount_percent=kwargs.get("discount_percent", Decimal("0")),
        tax_percent=kwargs.get("tax_percent", Decimal("0")),
        notes=kwargs.get("notes")
    )


def create_quote(
    customer_id: str,
    customer_name: str,
    lines: List[QuoteLine],
    contact_email: str,
    **kwargs
) -> Quote:
    """Factory function to create a quote."""
    builder = QuoteBuilder()
    builder.for_customer(customer_id, customer_name)
    builder.with_contact(contact_email, kwargs.get("contact_phone"))
    builder.with_lines(lines)
    
    if quote_number := kwargs.get("quote_number"):
        builder.with_quote_number(quote_number)
    if valid_until := kwargs.get("valid_until"):
        builder.valid_until(valid_until)
    if status := kwargs.get("status"):
        builder.with_status(status)
    if priority := kwargs.get("priority"):
        builder.with_priority(priority)
    if discount := kwargs.get("discount_percent"):
        builder.with_discount(discount)
    if tax := kwargs.get("tax_percent"):
        builder.with_tax(tax)
    if terms := kwargs.get("terms_and_conditions"):
        builder.with_terms(terms)
    if notes := kwargs.get("notes"):
        builder.with_notes(notes)
    if created_by := kwargs.get("created_by"):
        builder.created_by(created_by)
    if assigned_to := kwargs.get("assigned_to"):
        builder.assigned_to(assigned_to)
    if metadata := kwargs.get("metadata"):
        builder.with_metadata(metadata)
    
    return builder.build()
