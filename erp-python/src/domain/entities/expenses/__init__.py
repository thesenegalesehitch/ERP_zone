"""
Expense Entity for ERP System.

This module provides the Expense entity for managing expenses
following Clean Architecture principles.
"""

from dataclasses import dataclass, field
from datetime import datetime, date
from typing import Optional, Dict, Any, List
from enum import Enum
from decimal import Decimal


class ExpenseStatus(str, Enum):
    """Expense status enumeration."""
    DRAFT = "draft"
    SUBMITTED = "submitted"
    APPROVED = "approved"
    REJECTED = "rejected"
    REIMBURSED = "reimbursed"
    CANCELLED = "cancelled"


class ExpenseCategory(str, Enum):
    """Expense category enumeration."""
    TRAVEL = "travel"
    MEALS = "meals"
    ACCOMMODATION = "accommodation"
    TRANSPORTATION = "transportation"
    OFFICE_SUPPLIES = "office_supplies"
    EQUIPMENT = "equipment"
    SOFTWARE = "software"
    COMMUNICATION = "communication"
    UTILITIES = "utilities"
    RENT = "rent"
    MARKETING = "marketing"
    TRAINING = "training"
    ENTERTAINMENT = "entertainment"
    PROFESSIONAL_SERVICES = "professional_services"
    INSURANCE = "insurance"
    TAXES = "taxes"
    OTHER = "other"


class PaymentMethod(str, Enum):
    """Payment method enumeration."""
    CASH = "cash"
    CREDIT_CARD = "credit_card"
    DEBIT_CARD = "debit_card"
    BANK_TRANSFER = "bank_transfer"
    CHECK = "check"
    CORPORATE_CARD = "corporate_card"
    ADVANCE = "advance"
    REIMBURSEMENT = "reimbursement"


@dataclass(frozen=True)
class ExpenseReceipt:
    """
    Value Object representing an expense receipt.
    Immutable and validated.
    """
    id: str
    filename: str
    file_url: str
    file_type: str
    file_size: int
    uploaded_at: datetime = field(default_factory=datetime.utcnow)
    
    def __post_init__(self):
        if not self.filename:
            raise ValueError("filename cannot be empty")
        if not self.file_url:
            raise ValueError("file_url cannot be empty")
        if self.file_size <= 0:
            raise ValueError("file_size must be positive")
    
    @property
    def is_image(self) -> bool:
        """Check if receipt is an image."""
        return self.file_type.startswith("image/")
    
    @property
    def is_pdf(self) -> bool:
        """Check if receipt is a PDF."""
        return self.file_type == "application/pdf"
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert receipt to dictionary."""
        return {
            "id": self.id,
            "filename": self.filename,
            "file_url": self.file_url,
            "file_type": self.file_type,
            "file_size": self.file_size,
            "uploaded_at": self.uploaded_at.isoformat(),
            "is_image": self.is_image,
            "is_pdf": self.is_pdf
        }


@dataclass(frozen=True)
class Expense:
    """
    Expense entity representing a business expense in the ERP system.
    
    This entity follows Clean Architecture principles and is immutable.
    
    Attributes:
        id: Unique identifier for the expense
        expense_number: Human-readable expense number
        employee_id: ID of the employee who incurred the expense
        employee_name: Name of the employee
        department: Department name
        category: Expense category
        status: Current status of the expense
        amount: Expense amount
        currency: Currency code
        expense_date: Date when expense was incurred
        description: Description of the expense
        vendor: Vendor name
        receipt: Receipt attachment
        payment_method: Method of payment
        project_id: Associated project ID (optional)
        billable: Whether expense is billable to client
        client_id: Client ID if billable
        approved_by: ID of approver
        approved_at: Timestamp of approval
        rejected_by: ID of rejecter
        rejected_at: Timestamp of rejection
        reimbursed_at: Timestamp of reimbursement
        notes: Additional notes
        metadata: Additional metadata
        created_at: Timestamp when created
        updated_at: Timestamp when last updated
    """
    id: str
    expense_number: str
    employee_id: str
    employee_name: str
    department: str
    category: ExpenseCategory
    status: ExpenseStatus
    amount: Decimal
    currency: str
    expense_date: date
    description: str
    vendor: Optional[str] = None
    receipt: Optional[ExpenseReceipt] = None
    payment_method: PaymentMethod = PaymentMethod.CASH
    project_id: Optional[str] = None
    billable: bool = False
    client_id: Optional[str] = None
    approved_by: Optional[str] = None
    approved_at: Optional[datetime] = None
    rejected_by: Optional[str] = None
    rejected_at: Optional[datetime] = None
    reimbursed_at: Optional[datetime] = None
    notes: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime = field(default_factory=datetime.utcnow)
    
    def __post_init__(self):
        """Validate expense after initialization."""
        if not self.expense_number:
            raise ValueError("expense_number cannot be empty")
        if not self.employee_id:
            raise ValueError("employee_id cannot be empty")
        if not self.employee_name:
            raise ValueError("employee_name cannot be empty")
        if not self.department:
            raise ValueError("department cannot be empty")
        if self.amount <= 0:
            raise ValueError("amount must be positive")
        if not self.description:
            raise ValueError("description cannot be empty")
        if self.billable and not self.client_id:
            raise ValueError("client_id required when billable is True")
    
    @property
    def is_pending(self) -> bool:
        """Check if expense is pending approval."""
        return self.status == ExpenseStatus.SUBMITTED
    
    @property
    def is_approved(self) -> bool:
        """Check if expense is approved."""
        return self.status == ExpenseStatus.APPROVED
    
    @property
    def is_rejected(self) -> bool:
        """Check if expense is rejected."""
        return self.status == ExpenseStatus.REJECTED
    
    @property
    def is_reimbursed(self) -> bool:
        """Check if expense is reimbursed."""
        return self.status == ExpenseStatus.REIMBURSED
    
    @property
    def has_receipt(self) -> bool:
        """Check if expense has a receipt."""
        return self.receipt is not None
    
    @property
    def days_since_expense(self) -> int:
        """Get days since expense was incurred."""
        delta = date.today() - self.expense_date
        return delta.days
    
    def can_submit(self) -> bool:
        """Check if expense can be submitted."""
        return self.status == ExpenseStatus.DRAFT
    
    def can_approve(self) -> bool:
        """Check if expense can be approved."""
        return self.status == ExpenseStatus.SUBMITTED
    
    def can_reject(self) -> bool:
        """Check if expense can be rejected."""
        return self.status == ExpenseStatus.SUBMITTED
    
    def can_reimburse(self) -> bool:
        """Check if expense can be reimbursed."""
        return self.status == ExpenseStatus.APPROVED
    
    def can_cancel(self) -> bool:
        """Check if expense can be cancelled."""
        return self.status in [
            ExpenseStatus.DRAFT, ExpenseStatus.SUBMITTED
        ]
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert expense to dictionary."""
        return {
            "id": self.id,
            "expense_number": self.expense_number,
            "employee_id": self.employee_id,
            "employee_name": self.employee_name,
            "department": self.department,
            "category": self.category.value,
            "status": self.status.value,
            "amount": str(self.amount),
            "currency": self.currency,
            "expense_date": self.expense_date.isoformat(),
            "description": self.description,
            "vendor": self.vendor,
            "receipt": self.receipt.to_dict() if self.receipt else None,
            "payment_method": self.payment_method.value,
            "project_id": self.project_id,
            "billable": self.billable,
            "client_id": self.client_id,
            "approved_by": self.approved_by,
            "approved_at": self.approved_at.isoformat() if self.approved_at else None,
            "rejected_by": self.rejected_by,
            "rejected_at": self.rejected_at.isoformat() if self.rejected_at else None,
            "reimbursed_at": self.reimbursed_at.isoformat() if self.reimbursed_at else None,
            "notes": self.notes,
            "metadata": self.metadata,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
            "is_pending": self.is_pending,
            "is_approved": self.is_approved,
            "is_rejected": self.is_rejected,
            "is_reimbursed": self.is_reimbursed,
            "has_receipt": self.has_receipt,
            "days_since_expense": self.days_since_expense
        }


class ExpenseBuilder:
    """Builder for creating Expense instances."""
    
    def __init__(self):
        self._id: Optional[str] = None
        self._expense_number: Optional[str] = None
        self._employee_id: Optional[str] = None
        self._employee_name: Optional[str] = None
        self._department: Optional[str] = None
        self._category: Optional[ExpenseCategory] = None
        self._status: ExpenseStatus = ExpenseStatus.DRAFT
        self._amount: Optional[Decimal] = None
        self._currency: str = "USD"
        self._expense_date: Optional[date] = None
        self._description: Optional[str] = None
        self._vendor: Optional[str] = None
        self._receipt: Optional[ExpenseReceipt] = None
        self._payment_method: PaymentMethod = PaymentMethod.CASH
        self._project_id: Optional[str] = None
        self._billable: bool = False
        self._client_id: Optional[str] = None
        self._notes: Optional[str] = None
        self._metadata: Dict[str, Any] = {}
    
    def with_id(self, expense_id: str) -> "ExpenseBuilder":
        self._id = expense_id
        return self
    
    def with_expense_number(self, number: str) -> "ExpenseBuilder":
        self._expense_number = number
        return self
    
    def by_employee(self, employee_id: str, employee_name: str) -> "ExpenseBuilder":
        self._employee_id = employee_id
        self._employee_name = employee_name
        return self
    
    def in_department(self, department: str) -> "ExpenseBuilder":
        self._department = department
        return self
    
    def with_category(self, category: ExpenseCategory) -> "ExpenseBuilder":
        self._category = category
        return self
    
    def with_status(self, status: ExpenseStatus) -> "ExpenseBuilder":
        self._status = status
        return self
    
    def with_amount(self, amount: Decimal, currency: str = "USD") -> "ExpenseBuilder":
        self._amount = amount
        self._currency = currency
        return self
    
    def on_date(self, expense_date: date) -> "ExpenseBuilder":
        self._expense_date = expense_date
        return self
    
    def with_description(self, description: str) -> "ExpenseBuilder":
        self._description = description
        return self
    
    def from_vendor(self, vendor: str) -> "ExpenseBuilder":
        self._vendor = vendor
        return self
    
    def with_receipt(self, receipt: ExpenseReceipt) -> "ExpenseBuilder":
        self._receipt = receipt
        return self
    
    def with_payment_method(self, method: PaymentMethod) -> "ExpenseBuilder":
        self._payment_method = method
        return self
    
    def for_project(self, project_id: str) -> "ExpenseBuilder":
        self._project_id = project_id
        return self
    
    def billable_to(self, client_id: str) -> "ExpenseBuilder":
        self._billable = True
        self._client_id = client_id
        return self
    
    def with_notes(self, notes: str) -> "ExpenseBuilder":
        self._notes = notes
        return self
    
    def with_metadata(self, metadata: Dict[str, Any]) -> "ExpenseBuilder":
        self._metadata = metadata
        return self
    
    def build(self) -> Expense:
        from uuid import uuid4
        
        if not self._id:
            self._id = str(uuid4())
        if not self._expense_number:
            from time import time
            self._expense_number = f"EXP-{int(time())}"
        if not self._employee_id:
            raise ValueError("employee_id is required")
        if not self._employee_name:
            raise ValueError("employee_name is required")
        if not self._department:
            raise ValueError("department is required")
        if not self._category:
            raise ValueError("category is required")
        if not self._amount:
            raise ValueError("amount is required")
        if not self._description:
            raise ValueError("description is required")
        if not self._expense_date:
            self._expense_date = date.today()
        
        return Expense(
            id=self._id,
            expense_number=self._expense_number,
            employee_id=self._employee_id,
            employee_name=self._employee_name,
            department=self._department,
            category=self._category,
            status=self._status,
            amount=self._amount,
            currency=self._currency,
            expense_date=self._expense_date,
            description=self._description,
            vendor=self._vendor,
            receipt=self._receipt,
            payment_method=self._payment_method,
            project_id=self._project_id,
            billable=self._billable,
            client_id=self._client_id,
            notes=self._notes,
            metadata=self._metadata
        )


# Factory functions
def create_receipt(
    filename: str,
    file_url: str,
    file_type: str,
    file_size: int
) -> ExpenseReceipt:
    """Factory function to create an expense receipt."""
    from uuid import uuid4
    
    return ExpenseReceipt(
        id=str(uuid4()),
        filename=filename,
        file_url=file_url,
        file_type=file_type,
        file_size=file_size
    )


def create_expense(
    employee_id: str,
    employee_name: str,
    department: str,
    category: ExpenseCategory,
    amount: Decimal,
    description: str,
    currency: str = "USD",
    **kwargs
) -> Expense:
    """Factory function to create an expense."""
    builder = ExpenseBuilder()
    builder.by_employee(employee_id, employee_name)
    builder.in_department(department)
    builder.with_category(category)
    builder.with_amount(amount, currency)
    builder.with_description(description)
    
    if expense_number := kwargs.get("expense_number"):
        builder.with_expense_number(expense_number)
    if expense_date := kwargs.get("expense_date"):
        builder.on_date(expense_date)
    if status := kwargs.get("status"):
        builder.with_status(status)
    if vendor := kwargs.get("vendor"):
        builder.from_vendor(vendor)
    if receipt := kwargs.get("receipt"):
        builder.with_receipt(receipt)
    if payment_method := kwargs.get("payment_method"):
        builder.with_payment_method(payment_method)
    if project_id := kwargs.get("project_id"):
        builder.for_project(project_id)
    if client_id := kwargs.get("client_id"):
        builder.billable_to(client_id)
    if notes := kwargs.get("notes"):
        builder.with_notes(notes)
    if metadata := kwargs.get("metadata"):
        builder.with_metadata(metadata)
    
    return builder.build()
