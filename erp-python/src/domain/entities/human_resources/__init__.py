"""
Human Resources Entity for ERP System.

This module provides the Payroll entity for managing payroll
following Clean Architecture principles.
"""

from dataclasses import dataclass, field
from datetime import datetime, date
from typing import Optional, Dict, Any, List
from enum import Enum
from decimal import Decimal


class PayrollStatus(str, Enum):
    """Payroll status enumeration."""
    DRAFT = "draft"
    PROCESSING = "processing"
    APPROVED = "approved"
    PAID = "paid"
    CANCELLED = "cancelled"


class PayrollPeriod(str, Enum):
    """Payroll period enumeration."""
    WEEKLY = "weekly"
    BIWEEKLY = "biweekly"
    MONTHLY = "monthly"
    QUARTERLY = "quarterly"


@dataclass(frozen=True)
class PayrollItem:
    """
    Value Object representing a payroll item.
    Immutable and validated.
    """
    id: str
    employee_id: str
    employee_name: str
    basic_salary: Decimal
    allowances: Decimal = field(default=Decimal("0"))
    deductions: Decimal = field(default=Decimal("0"))
    bonuses: Decimal = field(default=Decimal("0"))
    overtime: Decimal = field(default=Decimal("0"))
    tax: Decimal = field(default=Decimal("0"))
    
    @property
    def gross_pay(self) -> Decimal:
        return self.basic_salary + self.allowances + self.bonuses + self.overtime
    
    @property
    def net_pay(self) -> Decimal:
        return self.gross_pay - self.deductions - self.tax
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "employee_id": self.employee_id,
            "employee_name": self.employee_name,
            "basic_salary": str(self.basic_salary),
            "allowances": str(self.allowances),
            "deductions": str(self.deductions),
            "bonuses": str(self.bonuses),
            "overtime": str(self.overtime),
            "tax": str(self.tax),
            "gross_pay": str(self.gross_pay),
            "net_pay": str(self.net_pay)
        }


@dataclass(frozen=True)
class Payroll:
    """
    Payroll entity representing a payroll run.
    
    This entity follows Clean Architecture principles and is immutable.
    
    Attributes:
        id: Unique identifier for the payroll
        payroll_number: Human-readable payroll number
        period_start: Period start date
        period_end: Period end date
        period_type: Payroll period type
        status: Current status
        items: List of payroll items
        total_gross: Total gross pay
        total_deductions: Total deductions
        total_tax: Total tax
        total_net: Total net pay
        approved_by: Approver user ID
        approved_name: Approver name
        paid_at: Payment timestamp
        metadata: Additional metadata
        created_at: Timestamp when created
        updated_at: Timestamp when last updated
    """
    id: str
    payroll_number: str
    period_start: date
    period_end: date
    period_type: PayrollPeriod
    status: PayrollStatus
    items: List[PayrollItem] = field(default_factory=list)
    total_gross: Decimal = field(default=Decimal("0"))
    total_deductions: Decimal = field(default=Decimal("0"))
    total_tax: Decimal = field(default=Decimal("0"))
    total_net: Decimal = field(default=Decimal("0"))
    approved_by: Optional[str] = None
    approved_name: Optional[str] = None
    paid_at: Optional[datetime] = None
    metadata: Dict[str, Any] = field(default_factory=dict)
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime = field(default_factory=datetime.utcnow)
    
    def __post_init__(self):
        if not self.payroll_number:
            raise ValueError("payroll_number cannot be empty")
        if self.period_end < self.period_start:
            raise ValueError("period_end must be after period_start")
    
    @property
    def is_paid(self) -> bool:
        return self.status == PayrollStatus.PAID
    
    @property
    def is_approved(self) -> bool:
        return self.status == PayrollStatus.APPROVED
    
    @property
    def employee_count(self) -> int:
        return len(self.items)
    
    @property
    def average_net(self) -> Decimal:
        if not self.items:
            return Decimal("0")
        return self.total_net / len(self.items)
    
    def calculate_totals(self) -> None:
        """Calculate payroll totals from items."""
        self.total_gross = sum(item.gross_pay for item in self.items)
        self.total_deductions = sum(item.deductions for item in self.items)
        self.total_tax = sum(item.tax for item in self.items)
        self.total_net = sum(item.net_pay for item in self.items)
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "payroll_number": self.payroll_number,
            "period_start": self.period_start.isoformat(),
            "period_end": self.period_end.isoformat(),
            "period_type": self.period_type.value,
            "status": self.status.value,
            "items": [i.to_dict() for i in self.items],
            "total_gross": str(self.total_gross),
            "total_deductions": str(self.total_deductions),
            "total_tax": str(self.total_tax),
            "total_net": str(self.total_net),
            "approved_by": self.approved_by,
            "approved_name": self.approved_name,
            "paid_at": self.paid_at.isoformat() if self.paid_at else None,
            "metadata": self.metadata,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
            "is_paid": self.is_paid,
            "is_approved": self.is_approved,
            "employee_count": self.employee_count,
            "average_net": str(self.average_net)
        }


class PayrollBuilder:
    """Builder for creating Payroll instances."""
    
    def __init__(self):
        self._id: Optional[str] = None
        self._payroll_number: Optional[str] = None
        self._period_start: Optional[date] = None
        self._period_end: Optional[date] = None
        self._period_type: PayrollPeriod = PayrollPeriod.MONTHLY
        self._status: PayrollStatus = PayrollStatus.DRAFT
        self._items: List[PayrollItem] = []
        self._total_gross: Decimal = Decimal("0")
        self._total_deductions: Decimal = Decimal("0")
        self._total_tax: Decimal = Decimal("0")
        self._total_net: Decimal = Decimal("0")
        self._approved_by: Optional[str] = None
        self._approved_name: Optional[str] = None
        self._metadata: Dict[str, Any] = {}
    
    def with_id(self, payroll_id: str) -> "PayrollBuilder":
        self._id = payroll_id
        return self
    
    def with_number(self, payroll_number: str) -> "PayrollBuilder":
        self._payroll_number = payroll_number
        return self
    
    def for_period(self, start: date, end: date) -> "PayrollBuilder":
        self._period_start = start
        self._period_end = end
        return self
    
    def with_period_type(self, period_type: PayrollPeriod) -> "PayrollBuilder":
        self._period_type = period_type
        return self
    
    def with_status(self, status: PayrollStatus) -> "PayrollBuilder":
        self._status = status
        return self
    
    def with_items(self, items: List[PayrollItem]) -> "PayrollBuilder":
        self._items = items
        return self
    
    def with_totals(self, gross: Decimal, deductions: Decimal, tax: Decimal, net: Decimal) -> "PayrollBuilder":
        self._total_gross = gross
        self._total_deductions = deductions
        self._total_tax = tax
        self._total_net = net
        return self
    
    def approved_by(self, user_id: str, user_name: str) -> "PayrollBuilder":
        self._approved_by = user_id
        self._approved_name = user_name
        return self
    
    def with_metadata(self, metadata: Dict[str, Any]) -> "PayrollBuilder":
        self._metadata = metadata
        return self
    
    def build(self) -> Payroll:
        from uuid import uuid4
        
        if not self._id:
            self._id = str(uuid4())
        if not self._payroll_number:
            from time import time
            self._payroll_number = f"PAY-{int(time())}"
        if not self._period_start:
            raise ValueError("period_start is required")
        if not self._period_end:
            raise ValueError("period_end is required")
        
        payroll = Payroll(
            id=self._id,
            payroll_number=self._payroll_number,
            period_start=self._period_start,
            period_end=self._period_end,
            period_type=self._period_type,
            status=self._status,
            items=self._items,
            total_gross=self._total_gross,
            total_deductions=self._total_deductions,
            total_tax=self._total_tax,
            total_net=self._total_net,
            approved_by=self._approved_by,
            approved_name=self._approved_name,
            metadata=self._metadata
        )
        
        if self._items and self._total_net == 0:
            payroll.calculate_totals()
        
        return payroll


# Factory functions
def create_payroll_item(
    employee_id: str,
    employee_name: str,
    basic_salary: Decimal,
    **kwargs
) -> PayrollItem:
    """Factory function to create a payroll item."""
    from uuid import uuid4
    
    return PayrollItem(
        id=str(uuid4()),
        employee_id=employee_id,
        employee_name=employee_name,
        basic_salary=basic_salary,
        allowances=kwargs.get("allowances", Decimal("0")),
        deductions=kwargs.get("deductions", Decimal("0")),
        bonuses=kwargs.get("bonuses", Decimal("0")),
        overtime=kwargs.get("overtime", Decimal("0")),
        tax=kwargs.get("tax", Decimal("0"))
    )


def create_payroll(
    period_start: date,
    period_end: date,
    **kwargs
) -> Payroll:
    """Factory function to create a payroll."""
    builder = PayrollBuilder()
    builder.for_period(period_start, period_end)
    
    if payroll_number := kwargs.get("payroll_number"):
        builder.with_number(payroll_number)
    if period_type := kwargs.get("period_type"):
        builder.with_period_type(period_type)
    if status := kwargs.get("status"):
        builder.with_status(status)
    if items := kwargs.get("items"):
        builder.with_items(items)
    if approved_by := kwargs.get("approved_by"):
        approved_name = kwargs.get("approved_name", "")
        builder.approved_by(approved_by, approved_name)
    if metadata := kwargs.get("metadata"):
        builder.with_metadata(metadata)
    
    return builder.build()
