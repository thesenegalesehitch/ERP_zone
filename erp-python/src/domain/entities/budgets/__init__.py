"""
Budget Entity for ERP System.

This module provides the Budget entity for managing budgets
following Clean Architecture principles.
"""

from dataclasses import dataclass, field
from datetime import datetime, date
from typing import Optional, Dict, Any, List
from enum import Enum
from decimal import Decimal


class BudgetStatus(str, Enum):
    """Budget status enumeration."""
    DRAFT = "draft"
    PENDING = "pending"
    APPROVED = "approved"
    ACTIVE = "active"
    CLOSED = "closed"
    CANCELLED = "cancelled"


class BudgetType(str, Enum):
    """Budget type enumeration."""
    OPERATIONAL = "operational"
    CAPITAL = "capital"
    PROJECT = "project"
    DEPARTMENT = "department"
    COMPANY = "company"


@dataclass(frozen=True)
class BudgetAllocation:
    """
    Value Object representing a budget allocation.
    Immutable and validated.
    """
    id: str
    category: str
    allocated: Decimal
    spent: Decimal = field(default=Decimal("0"))
    
    def __post_init__(self):
        if self.allocated <= 0:
            raise ValueError("allocated must be positive")
        if self.spent < 0:
            raise ValueError("spent cannot be negative")
    
    @property
    def remaining(self) -> Decimal:
        return self.allocated - self.spent
    
    @property
    def utilization_percent(self) -> Decimal:
        if self.allocated == 0:
            return Decimal("0")
        return (self.spent / self.allocated) * 100
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "category": self.category,
            "allocated": str(self.allocated),
            "spent": str(self.spent),
            "remaining": str(self.remaining),
            "utilization_percent": str(self.utilization_percent)
        }


@dataclass(frozen=True)
class Budget:
    """
    Budget entity representing a budget.
    
    This entity follows Clean Architecture principles and is immutable.
    
    Attributes:
        id: Unique identifier for the budget
        name: Budget name
        description: Budget description
        budget_type: Type of budget
        status: Current status
        fiscal_year: Fiscal year
        start_date: Budget start date
        end_date: Budget end date
        total_amount: Total budget amount
        currency: Currency code
        department_id: Department ID (optional)
        department_name: Department name
        project_id: Project ID (optional)
        project_name: Project name
        allocations: List of budget allocations
        owner_id: Budget owner ID
        owner_name: Budget owner name
        metadata: Additional metadata
        created_at: Timestamp when created
        updated_at: Timestamp when last updated
    """
    id: str
    name: str
    description: str
    budget_type: BudgetType
    status: BudgetStatus
    fiscal_year: int
    start_date: date
    end_date: date
    total_amount: Decimal
    currency: str = "USD"
    department_id: Optional[str] = None
    department_name: Optional[str] = None
    project_id: Optional[str] = None
    project_name: Optional[str] = None
    allocations: List[BudgetAllocation] = field(default_factory=list)
    owner_id: Optional[str] = None
    owner_name: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime = field(default_factory=datetime.utcnow)
    
    def __post_init__(self):
        """Validate budget after initialization."""
        if not self.name:
            raise ValueError("name cannot be empty")
        if self.end_date < self.start_date:
            raise ValueError("end_date must be after start_date")
        if self.total_amount <= 0:
            raise ValueError("total_amount must be positive")
    
    @property
    def is_active(self) -> bool:
        """Check if budget is active."""
        today = date.today()
        return self.status == BudgetStatus.ACTIVE and self.start_date <= today <= self.end_date
    
    @property
    def total_allocated(self) -> Decimal:
        """Get total allocated amount."""
        return sum(a.allocated for a in self.allocations)
    
    @property
    def total_spent(self) -> Decimal:
        """Get total spent amount."""
        return sum(a.spent for a in self.allocations)
    
    @property
    def total_remaining(self) -> Decimal:
        """Get total remaining amount."""
        return self.total_amount - self.total_spent
    
    @property
    def utilization_percent(self) -> Decimal:
        """Get budget utilization percentage."""
        if self.total_amount == 0:
            return Decimal("0")
        return (self.total_spent / self.total_amount) * 100
    
    @property
    def days_remaining(self) -> int:
        """Get days remaining in budget period."""
        today = date.today()
        if today > self.end_date:
            return 0
        return (self.end_date - today).days
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert budget to dictionary."""
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "budget_type": self.budget_type.value,
            "status": self.status.value,
            "fiscal_year": self.fiscal_year,
            "start_date": self.start_date.isoformat(),
            "end_date": self.end_date.isoformat(),
            "total_amount": str(self.total_amount),
            "currency": self.currency,
            "department_id": self.department_id,
            "department_name": self.department_name,
            "project_id": self.project_id,
            "project_name": self.project_name,
            "allocations": [a.to_dict() for a in self.allocations],
            "owner_id": self.owner_id,
            "owner_name": self.owner_name,
            "metadata": self.metadata,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
            "is_active": self.is_active,
            "total_allocated": str(self.total_allocated),
            "total_spent": str(self.total_spent),
            "total_remaining": str(self.total_remaining),
            "utilization_percent": str(self.utilization_percent),
            "days_remaining": self.days_remaining
        }


class BudgetBuilder:
    """Builder for creating Budget instances."""
    
    def __init__(self):
        self._id: Optional[str] = None
        self._name: Optional[str] = None
        self._description: str = ""
        self._budget_type: BudgetType = BudgetType.OPERATIONAL
        self._status: BudgetStatus = BudgetStatus.DRAFT
        self._fiscal_year: Optional[int] = None
        self._start_date: Optional[date] = None
        self._end_date: Optional[date] = None
        self._total_amount: Optional[Decimal] = None
        self._currency: str = "USD"
        self._department_id: Optional[str] = None
        self._department_name: Optional[str] = None
        self._project_id: Optional[str] = None
        self._project_name: Optional[str] = None
        self._allocations: List[BudgetAllocation] = []
        self._owner_id: Optional[str] = None
        self._owner_name: Optional[str] = None
        self._metadata: Dict[str, Any] = {}
    
    def with_id(self, budget_id: str) -> "BudgetBuilder":
        self._id = budget_id
        return self
    
    def with_name(self, name: str) -> "BudgetBuilder":
        self._name = name
        return self
    
    def with_description(self, description: str) -> "BudgetBuilder":
        self._description = description
        return self
    
    def with_type(self, budget_type: BudgetType) -> "BudgetBuilder":
        self._budget_type = budget_type
        return self
    
    def with_status(self, status: BudgetStatus) -> "BudgetBuilder":
        self._status = status
        return self
    
    def for_fiscal_year(self, year: int) -> "BudgetBuilder":
        self._fiscal_year = year
        return self
    
    def valid_from(self, start_date: date, end_date: date) -> "BudgetBuilder":
        self._start_date = start_date
        self._end_date = end_date
        return self
    
    def with_amount(self, amount: Decimal) -> "BudgetBuilder":
        self._total_amount = amount
        return self
    
    def with_currency(self, currency: str) -> "BudgetBuilder":
        self._currency = currency
        return self
    
    def for_department(self, department_id: str, department_name: str) -> "BudgetBuilder":
        self._department_id = department_id
        self._department_name = department_name
        return self
    
    def for_project(self, project_id: str, project_name: str) -> "BudgetBuilder":
        self._project_id = project_id
        self._project_name = project_name
        return self
    
    def with_allocations(self, allocations: List[BudgetAllocation]) -> "BudgetBuilder":
        self._allocations = allocations
        return self
    
    def owned_by(self, owner_id: str, owner_name: str) -> "BudgetBuilder":
        self._owner_id = owner_id
        self._owner_name = owner_name
        return self
    
    def with_metadata(self, metadata: Dict[str, Any]) -> "BudgetBuilder":
        self._metadata = metadata
        return self
    
    def build(self) -> Budget:
        from uuid import uuid4
        
        if not self._id:
            self._id = str(uuid4())
        if not self._name:
            raise ValueError("name is required")
        if not self._fiscal_year:
            raise ValueError("fiscal_year is required")
        if not self._start_date:
            raise ValueError("start_date is required")
        if not self._end_date:
            raise ValueError("end_date is required")
        if not self._total_amount:
            raise ValueError("total_amount is required")
        
        return Budget(
            id=self._id,
            name=self._name,
            description=self._description,
            budget_type=self._budget_type,
            status=self._status,
            fiscal_year=self._fiscal_year,
            start_date=self._start_date,
            end_date=self._end_date,
            total_amount=self._total_amount,
            currency=self._currency,
            department_id=self._department_id,
            department_name=self._department_name,
            project_id=self._project_id,
            project_name=self._project_name,
            allocations=self._allocations,
            owner_id=self._owner_id,
            owner_name=self._owner_name,
            metadata=self._metadata
        )


# Factory functions
def create_budget_allocation(
    category: str,
    allocated: Decimal,
    **kwargs
) -> BudgetAllocation:
    """Factory function to create a budget allocation."""
    from uuid import uuid4
    
    return BudgetAllocation(
        id=str(uuid4()),
        category=category,
        allocated=allocated,
        spent=kwargs.get("spent", Decimal("0"))
    )


def create_budget(
    name: str,
    fiscal_year: int,
    start_date: date,
    end_date: date,
    total_amount: Decimal,
    **kwargs
) -> Budget:
    """Factory function to create a budget."""
    builder = BudgetBuilder()
    builder.with_name(name)
    builder.for_fiscal_year(fiscal_year)
    builder.valid_from(start_date, end_date)
    builder.with_amount(total_amount)
    
    if description := kwargs.get("description"):
        builder.with_description(description)
    if budget_type := kwargs.get("budget_type"):
        builder.with_type(budget_type)
    if status := kwargs.get("status"):
        builder.with_status(status)
    if currency := kwargs.get("currency"):
        builder.with_currency(currency)
    if department_id := kwargs.get("department_id"):
        department_name = kwargs.get("department_name", "")
        builder.for_department(department_id, department_name)
    if project_id := kwargs.get("project_id"):
        project_name = kwargs.get("project_name", "")
        builder.for_project(project_id, project_name)
    if allocations := kwargs.get("allocations"):
        builder.with_allocations(allocations)
    if owner_id := kwargs.get("owner_id"):
        owner_name = kwargs.get("owner_name", "")
        builder.owned_by(owner_id, owner_name)
    if metadata := kwargs.get("metadata"):
        builder.with_metadata(metadata)
    
    return builder.build()
