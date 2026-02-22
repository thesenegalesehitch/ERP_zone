"""
Payment Entity - Domain Layer
Represents payments in the ERP system.

Author: Alexandre Albert Ndour
"""

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Optional
from enum import Enum
import uuid


class PaymentStatus(str, Enum):
    """Payment status enumeration."""
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"
    REFUNDED = "refunded"
    CANCELLED = "cancelled"


class PaymentMethod(str, Enum):
    """Payment method enumeration."""
    CASH = "cash"
    BANK_TRANSFER = "bank_transfer"
    CREDIT_CARD = "credit_card"
    DEBIT_CARD = "debit_card"
    CHECK = "check"
    PAYPAL = "paypal"
    STRIPE = "stripe"
    CRYPTO = "crypto"


@dataclass
class Payment:
    """
    Payment Entity.
    
    Represents a payment transaction.
    """
    
    # Identity
    id: uuid.UUID = field(default_factory=uuid.uuid4)
    payment_number: str = ""
    
    # References
    invoice_id: Optional[uuid.UUID] = None
    order_id: Optional[uuid.UUID] = None
    customer_id: uuid.UUID = None  # type: ignore
    
    # Amount
    amount: float = 0.0
    currency: str = "EUR"
    
    # Method
    payment_method: PaymentMethod = PaymentMethod.BANK_TRANSFER
    
    # Status
    status: PaymentStatus = PaymentStatus.PENDING
    
    # Gateway
    gateway: Optional[str] = None
    gateway_reference: Optional[str] = None
    gateway_response: Optional[dict] = None
    
    # Reference
    reference: Optional[str] = None  # Check number, transaction ID
    
    # Dates
    payment_date: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    processed_date: Optional[datetime] = None
    failed_date: Optional[datetime] = None
    
    # Notes
    notes: Optional[str] = None
    
    # Refund
    is_refunded: bool = False
    refund_amount: float = 0.0
    refund_date: Optional[datetime] = None
    refund_reason: Optional[str] = None
    
    # Metadata
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    created_by: Optional[uuid.UUID] = None
    
    def __post_init__(self):
        if isinstance(self.customer_id, str):
            self.customer_id = uuid.UUID(self.customer_id)
    
    # ==================== Business Methods ====================
    
    def process(self) -> None:
        """Process the payment."""
        if self.status != PaymentStatus.PENDING:
            raise ValueError("Only pending payments can be processed")
        self.status = PaymentStatus.PROCESSING
        self.processed_date = datetime.now(timezone.utc)
        self.updated_at = datetime.now(timezone.utc)
    
    def complete(self, gateway_reference: str = None) -> None:
        """Complete the payment."""
        if self.status not in [PaymentStatus.PENDING, PaymentStatus.PROCESSING]:
            raise ValueError("Payment cannot be completed")
        self.status = PaymentStatus.COMPLETED
        if gateway_reference:
            self.gateway_reference = gateway_reference
        self.updated_at = datetime.now(timezone.utc)
    
    def fail(self, reason: str = None) -> None:
        """Fail the payment."""
        self.status = PaymentStatus.FAILED
        self.failed_date = datetime.now(timezone.utc)
        if reason:
            self.notes = reason
        self.updated_at = datetime.now(timezone.utc)
    
    def refund(self, amount: float = None, reason: str = None) -> None:
        """Refund the payment."""
        if self.status != PaymentStatus.COMPLETED:
            raise ValueError("Only completed payments can be refunded")
        
        refund_amount = amount if amount is not None else self.amount
        if refund_amount > self.amount - self.refund_amount:
            raise ValueError("Refund amount exceeds remaining")
        
        self.refund_amount += refund_amount
        self.is_refunded = self.refund_amount >= self.amount
        
        if self.is_refunded:
            self.status = PaymentStatus.REFUNDED
        
        self.refund_date = datetime.now(timezone.utc)
        if reason:
            self.refund_reason = reason
        self.updated_at = datetime.now(timezone.utc)
    
    def cancel(self) -> None:
        """Cancel the payment."""
        if self.status in [PaymentStatus.COMPLETED, PaymentStatus.REFUNDED]:
            raise ValueError("Cannot cancel completed or refunded payments")
        self.status = PaymentStatus.CANCELLED
        self.updated_at = datetime.now(timezone.utc)
    
    # ==================== Properties ====================
    
    @property
    def remaining_amount(self) -> float:
        """Get remaining refundable amount."""
        return self.amount - self.refund_amount
    
    @property
    def is_full_refund(self) -> bool:
        """Check if fully refunded."""
        return self.is_refunded
    
    @property
    def is_refundable(self) -> bool:
        """Check if payment can be refunded."""
        return self.status == PaymentStatus.COMPLETED and not self.is_refunded
    
    # ==================== Factory Methods ====================
    
    @classmethod
    def create(
        cls,
        customer_id: uuid.UUID,
        amount: float,
        payment_method: PaymentMethod = PaymentMethod.BANK_TRANSFER,
        invoice_id: uuid.UUID = None,
        order_id: uuid.UUID = None,
        reference: str = None,
        created_by: uuid.UUID = None
    ) -> "Payment":
        """Factory method to create a payment."""
        payment_number = cls._generate_payment_number()
        
        return cls(
            payment_number=payment_number,
            customer_id=customer_id,
            amount=amount,
            payment_method=payment_method,
            invoice_id=invoice_id,
            order_id=order_id,
            reference=reference,
            created_by=created_by
        )
    
    @classmethod
    def _generate_payment_number(cls) -> str:
        """Generate payment number."""
        from datetime import datetime
        now = datetime.now()
        return f"PAY-{now.strftime('%Y%m%d')}-{uuid.uuid4().hex[:8].upper()}"
    
    # ==================== Serialization ====================
    
    def to_dict(self) -> dict:
        """Convert to dictionary."""
        return {
            "id": str(self.id),
            "payment_number": self.payment_number,
            "invoice_id": str(self.invoice_id) if self.invoice_id else None,
            "order_id": str(self.order_id) if self.order_id else None,
            "customer_id": str(self.customer_id),
            "amount": self.amount,
            "currency": self.currency,
            "payment_method": self.payment_method.value,
            "status": self.status.value,
            "gateway": self.gateway,
            "gateway_reference": self.gateway_reference,
            "reference": self.reference,
            "payment_date": self.payment_date.isoformat(),
            "processed_date": self.processed_date.isoformat() if self.processed_date else None,
            "is_refunded": self.is_refunded,
            "refund_amount": self.refund_amount,
            "is_refundable": self.is_refundable,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
        }
