"""
Invoice Entity - Domain Layer
Represents an invoice in the ERP system.

Author: Alexandre Albert Ndour
"""

from dataclasses import dataclass, field
from datetime import datetime, timezone, timedelta
from typing import Optional, List
from enum import Enum
import uuid


class InvoiceStatus(str, Enum):
    """Invoice status enumeration."""
    DRAFT = "draft"
    PENDING = "pending"
    SENT = "sent"
    VIEWED = "sent"
    PAID = "paid"
    PARTIAL = "partial"
    OVERDUE = "overdue"
    CANCELLED = "cancelled"
    VOID = "void"


class InvoiceType(str, Enum):
    """Invoice type enumeration."""
    STANDARD = "standard"
    PROFORMA = "proforma"
    RECURRING = "recurring"
    CREDIT_NOTE = "credit_note"
    DEBIT_NOTE = "debit_note"


class PaymentMethod(str, Enum):
    """Payment method enumeration."""
    CASH = "cash"
    BANK_TRANSFER = "bank_transfer"
    CREDIT_CARD = "credit_card"
    CHECK = "check"
    PAYPAL = "paypal"
    CRYPTO = "crypto"


@dataclass
class Invoice:
    """
    Invoice Entity.
    
    Represents an invoice for goods or services.
    """
    
    # Identity
    id: uuid.UUID = field(default_factory=uuid.uuid4)
    invoice_number: str = ""
    invoice_type: InvoiceType = InvoiceType.STANDARD
    
    # References
    customer_id: uuid.UUID = None  # type: ignore
    order_id: Optional[uuid.UUID] = None
    
    # Status
    status: InvoiceStatus = InvoiceStatus.DRAFT
    
    # Dates
    issue_date: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    due_date: datetime = None  # type: ignore
    sent_date: Optional[datetime] = None
    paid_date: Optional[datetime] = None
    cancelled_date: Optional[datetime] = None
    
    # Pricing
    subtotal: float = 0.0
    tax_amount: float = 0.0
    discount_amount: float = 0.0
    total: float = 0.0
    amount_paid: float = 0.0
    amount_due: float = 0.0
    
    # Currency
    currency: str = "EUR"
    
    # Notes
    customer_notes: Optional[str] = None
    internal_notes: Optional[str] = None
    terms: Optional[str] = None
    
    # Payment
    payment_method: Optional[PaymentMethod] = None
    payment_reference: Optional[str] = None
    
    # Address
    billing_address_id: Optional[uuid.UUID] = None
    
    # Recurring
    is_recurring: bool = False
    recurring_interval: Optional[str] = None  # monthly, yearly
    
    # Metadata
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    created_by: Optional[uuid.UUID] = None
    
    # Lines
    _lines: List["InvoiceLine"] = field(default_factory=list, repr=False)
    
    def __post_init__(self):
        """Validate after initialization."""
        if isinstance(self.customer_id, str):
            self.customer_id = uuid.UUID(self.customer_id)
        if self.due_date is None:
            self.due_date = datetime.now(timezone.utc) + timedelta(days=30)
    
    # ==================== Business Methods ====================
    
    def add_line(self, line: "InvoiceLine") -> None:
        """Add a line to the invoice."""
        self._lines.append(line)
        self._recalculate_totals()
    
    def remove_line(self, line_id: uuid.UUID) -> None:
        """Remove a line from the invoice."""
        self._lines = [l for l in self._lines if l.id != line_id]
        self._recalculate_totals()
    
    def _recalculate_totals(self) -> None:
        """Recalculate invoice totals."""
        self.subtotal = sum(line.total for line in self._lines)
        self.tax_amount = sum(line.tax_amount for line in self._lines)
        self.total = self.subtotal + self.tax_amount - self.discount_amount
        self.amount_due = self.total - self.amount_paid
    
    def send(self) -> None:
        """Send the invoice."""
        if self.status != InvoiceStatus.DRAFT:
            raise ValueError("Only draft invoices can be sent")
        self.status = InvoiceStatus.SENT
        self.sent_date = datetime.now(timezone.utc)
        self.updated_at = datetime.now(timezone.utc)
    
    def mark_as_paid(
        self,
        payment_method: PaymentMethod = None,
        reference: str = None
    ) -> None:
        """Mark invoice as paid."""
        self.status = InvoiceStatus.PAID
        self.paid_date = datetime.now(timezone.utc)
        self.amount_paid = self.total
        self.amount_due = 0
        if payment_method:
            self.payment_method = payment_method
        if reference:
            self.payment_reference = reference
        self.updated_at = datetime.now(timezone.utc)
    
    def record_payment(
        self,
        amount: float,
        payment_method: PaymentMethod = None,
        reference: str = None
    ) -> None:
        """Record a partial payment."""
        if amount <= 0:
            raise ValueError("Payment amount must be positive")
        if amount > self.amount_due:
            raise ValueError("Payment exceeds amount due")
        
        self.amount_paid += amount
        self.amount_due = self.total - self.amount_paid
        
        if self.amount_due == 0:
            self.status = InvoiceStatus.PAID
            self.paid_date = datetime.now(timezone.utc)
        else:
            self.status = InvoiceStatus.PARTIAL
        
        if payment_method:
            self.payment_method = payment_method
        if reference:
            self.payment_reference = reference
        
        self.updated_at = datetime.now(timezone.utc)
    
    def cancel(self, reason: str = None) -> None:
        """Cancel the invoice."""
        if self.status == InvoiceStatus.PAID:
            raise ValueError("Cannot cancel a paid invoice")
        self.status = InvoiceStatus.CANCELLED
        self.cancelled_date = datetime.now(timezone.utc)
        self.internal_notes = reason
        self.updated_at = datetime.now(timezone.utc)
    
    def apply_discount(self, amount: float) -> None:
        """Apply discount to invoice."""
        if amount < 0:
            raise ValueError("Discount cannot be negative")
        if amount > self.subtotal + self.tax_amount:
            raise ValueError("Discount cannot exceed invoice total")
        self.discount_amount = amount
        self._recalculate_totals()
    
    def is_overdue(self) -> bool:
        """Check if invoice is overdue."""
        if self.status in [InvoiceStatus.PAID, InvoiceStatus.CANCELLED]:
            return False
        return datetime.now(timezone.utc) > self.due_date
    
    def days_until_due(self) -> int:
        """Calculate days until due date."""
        delta = self.due_date - datetime.now(timezone.utc)
        return delta.days
    
    # ==================== Properties ====================
    
    @property
    def lines(self) -> List["InvoiceLine"]:
        """Get invoice lines."""
        return self._lines.copy()
    
    @property
    def line_count(self) -> int:
        """Get number of invoice lines."""
        return len(self._lines)
    
    @property
    def is_paid(self) -> bool:
        """Check if invoice is fully paid."""
        return self.status == InvoiceStatus.PAID
    
    @property
    def is_partially_paid(self) -> bool:
        """Check if invoice is partially paid."""
        return self.status == InvoiceStatus.PARTIAL
    
    @property
    def payment_percentage(self) -> float:
        """Get payment percentage."""
        if self.total == 0:
            return 0
        return (self.amount_paid / self.total) * 100
    
    # ==================== Factory Methods ====================
    
    @classmethod
    def create(
        cls,
        customer_id: uuid.UUID,
        invoice_type: InvoiceType = InvoiceType.STANDARD,
        order_id: uuid.UUID = None,
        due_days: int = 30,
        created_by: uuid.UUID = None
    ) -> "Invoice":
        """Factory method to create an invoice."""
        invoice_number = cls._generate_invoice_number(invoice_type)
        due_date = datetime.now(timezone.utc) + timedelta(days=due_days)
        
        return cls(
            invoice_number=invoice_number,
            invoice_type=invoice_type,
            customer_id=customer_id,
            order_id=order_id,
            due_date=due_date,
            created_by=created_by
        )
    
    @classmethod
    def _generate_invoice_number(cls, invoice_type: InvoiceType) -> str:
        """Generate invoice number."""
        from datetime import datetime
        now = datetime.now()
        prefix = "INV"
        if invoice_type == InvoiceType.PROFORMA:
            prefix = "PRO"
        elif invoice_type == InvoiceType.CREDIT_NOTE:
            prefix = "CN"
        elif invoice_type == InvoiceType.DEBIT_NOTE:
            prefix = "DN"
        
        return f"{prefix}-{now.strftime('%Y%m')}-{uuid.uuid4().hex[:6].upper()}"
    
    # ==================== Serialization ====================
    
    def to_dict(self) -> dict:
        """Convert to dictionary."""
        return {
            "id": str(self.id),
            "invoice_number": self.invoice_number,
            "invoice_type": self.invoice_type.value,
            "customer_id": str(self.customer_id),
            "order_id": str(self.order_id) if self.order_id else None,
            "status": self.status.value,
            "issue_date": self.issue_date.isoformat(),
            "due_date": self.due_date.isoformat(),
            "sent_date": self.sent_date.isoformat() if self.sent_date else None,
            "paid_date": self.paid_date.isoformat() if self.paid_date else None,
            "cancelled_date": self.cancelled_date.isoformat() if self.cancelled_date else None,
            "subtotal": self.subtotal,
            "tax_amount": self.tax_amount,
            "discount_amount": self.discount_amount,
            "total": self.total,
            "amount_paid": self.amount_paid,
            "amount_due": self.amount_due,
            "currency": self.currency,
            "is_overdue": self.is_overdue(),
            "days_until_due": self.days_until_due(),
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
        }


@dataclass
class InvoiceLine:
    """
    InvoiceLine Entity.
    
    Represents a single line item in an invoice.
    """
    
    # Identity
    id: uuid.UUID = field(default_factory=uuid.uuid4)
    invoice_id: uuid.UUID = None  # type: ignore
    
    # References
    product_id: Optional[uuid.UUID] = None
    order_line_id: Optional[uuid.UUID] = None
    
    # Line details
    description: str = ""
    
    # Quantity and pricing
    quantity: float = 1.0
    unit_price: float = 0.0
    tax_rate: float = 0.0
    
    # Discount
    discount_percent: float = 0.0
    discount_amount: float = 0.0
    
    # Metadata
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    
    def __post_init__(self):
        """Validate after initialization."""
        if self.quantity <= 0:
            raise ValueError("Quantity must be positive")
        if self.unit_price < 0:
            raise ValueError("Unit price cannot be negative")
    
    # ==================== Properties ====================
    
    @property
    def subtotal(self) -> float:
        """Calculate line subtotal."""
        return self.quantity * self.unit_price
    
    @property
    def discount_total(self) -> float:
        """Calculate total discount."""
        amount_discount = self.discount_amount
        percent_discount = self.subtotal * (self.discount_percent / 100)
        return amount_discount + percent_discount
    
    @property
    def taxable_amount(self) -> float:
        """Calculate taxable amount."""
        return self.subtotal - self.discount_total
    
    @property
    def tax_amount(self) -> float:
        """Calculate tax amount."""
        return self.taxable_amount * (self.tax_rate / 100)
    
    @property
    def total(self) -> float:
        """Calculate line total."""
        return self.taxable_amount + self.tax_amount
    
    # ==================== Factory Methods ====================
    
    @classmethod
    def create(
        cls,
        invoice_id: uuid.UUID,
        description: str,
        quantity: float,
        unit_price: float,
        tax_rate: float = 0.0,
        product_id: uuid.UUID = None
    ) -> "InvoiceLine":
        """Factory method to create an invoice line."""
        return cls(
            invoice_id=invoice_id,
            description=description,
            quantity=quantity,
            unit_price=unit_price,
            tax_rate=tax_rate,
            product_id=product_id
        )
    
    # ==================== Serialization ====================
    
    def to_dict(self) -> dict:
        """Convert to dictionary."""
        return {
            "id": str(self.id),
            "invoice_id": str(self.invoice_id),
            "product_id": str(self.product_id) if self.product_id else None,
            "description": self.description,
            "quantity": self.quantity,
            "unit_price": self.unit_price,
            "tax_rate": self.tax_rate,
            "discount_percent": self.discount_percent,
            "discount_amount": self.discount_amount,
            "subtotal": self.subtotal,
            "tax_amount": self.tax_amount,
            "total": self.total,
            "created_at": self.created_at.isoformat(),
        }
