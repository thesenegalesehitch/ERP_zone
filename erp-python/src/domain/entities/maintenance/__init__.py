"""
Maintenance Entity for ERP System.

This module provides entities for maintenance management
following Clean Architecture principles.
"""

from dataclasses import dataclass, field
from datetime import datetime, date
from typing import Optional, Dict, Any, List
from enum import Enum
from uuid import uuid4
from decimal import Decimal


class MaintenanceStatus(str, Enum):
    """Maintenance status enumeration."""
    SCHEDULED = "scheduled"
    IN_PROGRESS = "in_progress"
    ON_HOLD = "on_hold"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


class MaintenanceType(str, Enum):
    """Maintenance type enumeration."""
    PREVENTIVE = "preventive"
    CORRECTIVE = "corrective"
    PREDICTIVE = "predictive"
    EMERGENCY = "emergency"
    INSPECTION = "inspection"


class WorkOrderPriority(str, Enum):
    """Work order priority enumeration."""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    URGENT = "urgent"
    CRITICAL = "critical"


@dataclass(frozen=True)
class MaintenanceTask:
    """
    Value Object representing a maintenance task.
    Immutable and validated.
    """
    id: str
    description: str
    estimated_hours: Decimal
    actual_hours: Decimal = field(default=Decimal("0"))
    is_completed: bool = False
    notes: str = ""
    completed_at: Optional[datetime] = None
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "description": self.description,
            "estimated_hours": str(self.estimated_hours),
            "actual_hours": str(self.actual_hours),
            "is_completed": self.is_completed,
            "notes": self.notes,
            "completed_at": self.completed_at.isoformat() if self.completed_at else None
        }


@dataclass(frozen=True)
class MaintenancePart:
    """
    Value Object representing a maintenance part/material.
    Immutable and validated.
    """
    id: str
    part_id: str
    part_number: str
    part_name: str
    quantity: int
    unit_cost: Decimal
    total_cost: Decimal
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "part_id": self.part_id,
            "part_number": self.part_number,
            "part_name": self.part_name,
            "quantity": self.quantity,
            "unit_cost": str(self.unit_cost),
            "total_cost": str(self.total_cost)
        }


@dataclass(frozen=True)
class MaintenanceWorkOrder:
    """
    Maintenance Work Order entity for managing maintenance operations.
    
    This entity follows Clean Architecture principles and is immutable.
    
    Attributes:
        id: Unique identifier
        work_order_number: Human-readable work order number
        asset_id: Asset identifier
        asset_name: Asset name
        asset_code: Asset code
        maintenance_type: Type of maintenance
        status: Current status
        priority: Work order priority
        description: Detailed description
        cause: Root cause
        solution: Solution applied
        tasks: List of tasks
        parts: List of parts/materials
        labor_hours: Labor hours
        labor_cost: Labor cost
        parts_cost: Parts cost
        total_cost: Total cost
        scheduled_date: Scheduled maintenance date
        started_at: Actual start timestamp
        completed_at: Completion timestamp
        assigned_to: Technician user ID
        assigned_name: Technician name
        requested_by: Requester user ID
        requested_name: Requester name
        notes: Additional notes
        metadata: Additional metadata
        created_at: Creation timestamp
        updated_at: Last update timestamp
    """
    id: str
    work_order_number: str
    asset_id: str
    asset_name: str
    asset_code: str
    maintenance_type: MaintenanceType
    status: MaintenanceStatus
    priority: WorkOrderPriority
    description: str
    cause: str = ""
    solution: str = ""
    tasks: List[MaintenanceTask] = field(default_factory=list)
    parts: List[MaintenancePart] = field(default_factory=list)
    labor_hours: Decimal = field(default=Decimal("0"))
    labor_cost: Decimal = field(default=Decimal("0"))
    parts_cost: Decimal = field(default=Decimal("0"))
    total_cost: Decimal = field(default=Decimal("0"))
    scheduled_date: Optional[date] = None
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    assigned_to: Optional[str] = None
    assigned_name: str = ""
    requested_by: Optional[str] = None
    requested_name: str = ""
    notes: str = ""
    metadata: Dict[str, Any] = field(default_factory=dict)
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime = field(default_factory=datetime.utcnow)
    
    def __post_init__(self):
        if not self.work_order_number:
            raise ValueError("work_order_number cannot be empty")
        if not self.asset_id:
            raise ValueError("asset_id cannot be empty")
    
    @property
    def is_scheduled(self) -> bool:
        return self.status == MaintenanceStatus.SCHEDULED
    
    @property
    def is_in_progress(self) -> bool:
        return self.status == MaintenanceStatus.IN_PROGRESS
    
    @property
    def is_completed(self) -> bool:
        return self.status == MaintenanceStatus.COMPLETED
    
    @property
    def is_overdue(self) -> bool:
        if not self.scheduled_date:
            return False
        return date.today() > self.scheduled_date and not self.is_completed
    
    @property
    def task_count(self) -> int:
        return len(self.tasks)
    
    @property
    def completed_task_count(self) -> int:
        return sum(1 for t in self.tasks if t.is_completed)
    
    @property
    def completion_percentage(self) -> float:
        if not self.tasks:
            return 0.0
        return (self.completed_task_count / len(self.tasks)) * 100
    
    def calculate_costs(self, hourly_rate: Decimal = Decimal("50")) -> None:
        """Calculate work order costs."""
        self.labor_cost = self.labor_hours * hourly_rate
        self.parts_cost = sum(p.total_cost for p in self.parts)
        self.total_cost = self.labor_cost + self.parts_cost
    
    def assign(self, user_id: str, user_name: str) -> None:
        """Assign the work order to a technician."""
        self.assigned_to = user_id
        self.assigned_name = user_name
    
    def start(self) -> None:
        """Start the maintenance work."""
        self.status = MaintenanceStatus.IN_PROGRESS
        self.started_at = datetime.utcnow()
    
    def complete(self, solution: str) -> None:
        """Complete the maintenance work."""
        self.status = MaintenanceStatus.COMPLETED
        self.solution = solution
        self.completed_at = datetime.utcnow()
    
    def cancel(self, reason: str) -> None:
        """Cancel the work order."""
        self.status = MaintenanceStatus.CANCELLED
        self.notes += f"\n[CANCELLED: {reason}]"
    
    def hold(self, reason: str) -> None:
        """Put the work order on hold."""
        self.status = MaintenanceStatus.ON_HOLD
        self.notes += f"\n[ON HOLD: {reason}]"
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "work_order_number": self.work_order_number,
            "asset_id": self.asset_id,
            "asset_name": self.asset_name,
            "asset_code": self.asset_code,
            "maintenance_type": self.maintenance_type.value,
            "status": self.status.value,
            "priority": self.priority.value,
            "description": self.description,
            "cause": self.cause,
            "solution": self.solution,
            "tasks": [t.to_dict() for t in self.tasks],
            "parts": [p.to_dict() for p in self.parts],
            "labor_hours": str(self.labor_hours),
            "labor_cost": str(self.labor_cost),
            "parts_cost": str(self.parts_cost),
            "total_cost": str(self.total_cost),
            "scheduled_date": self.scheduled_date.isoformat() if self.scheduled_date else None,
            "started_at": self.started_at.isoformat() if self.started_at else None,
            "completed_at": self.completed_at.isoformat() if self.completed_at else None,
            "assigned_to": self.assigned_to,
            "assigned_name": self.assigned_name,
            "requested_by": self.requested_by,
            "requested_name": self.requested_name,
            "notes": self.notes,
            "metadata": self.metadata,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
            "is_scheduled": self.is_scheduled,
            "is_in_progress": self.is_in_progress,
            "is_completed": self.is_completed,
            "is_overdue": self.is_overdue,
            "task_count": self.task_count,
            "completed_task_count": self.completed_task_count,
            "completion_percentage": self.completion_percentage
        }


class MaintenanceWorkOrderBuilder:
    """Builder for creating MaintenanceWorkOrder instances."""
    
    def __init__(self):
        self._id: Optional[str] = None
        self._work_order_number: Optional[str] = None
        self._asset_id: Optional[str] = None
        self._asset_name: str = ""
        self._asset_code: str = ""
        self._maintenance_type: MaintenanceType = MaintenanceType.PREVENTIVE
        self._status: MaintenanceStatus = MaintenanceStatus.SCHEDULED
        self._priority: WorkOrderPriority = WorkOrderPriority.MEDIUM
        self._description: str = ""
        self._cause: str = ""
        self._solution: str = ""
        self._tasks: List[MaintenanceTask] = []
        self._parts: List[MaintenancePart] = []
        self._labor_hours: Decimal = Decimal("0")
        self._scheduled_date: Optional[date] = None
        self._assigned_to: Optional[str] = None
        self._assigned_name: str = ""
        self._requested_by: Optional[str] = None
        self._requested_name: str = ""
        self._notes: str = ""
        self._metadata: Dict[str, Any] = {}
    
    def with_id(self, order_id: str) -> "MaintenanceWorkOrderBuilder":
        self._id = order_id
        return self
    
    def with_work_order_number(self, work_order_number: str) -> "MaintenanceWorkOrderBuilder":
        self._work_order_number = work_order_number
        return self
    
    def for_asset(self, asset_id: str, asset_name: str, asset_code: str) -> "MaintenanceWorkOrderBuilder":
        self._asset_id = asset_id
        self._asset_name = asset_name
        self._asset_code = asset_code
        return self
    
    def with_maintenance_type(self, maint_type: MaintenanceType) -> "MaintenanceWorkOrderBuilder":
        self._maintenance_type = maint_type
        return self
    
    def with_status(self, status: MaintenanceStatus) -> "MaintenanceWorkOrderBuilder":
        self._status = status
        return self
    
    def with_priority(self, priority: WorkOrderPriority) -> "MaintenanceWorkOrderBuilder":
        self._priority = priority
        return self
    
    def with_description(self, description: str) -> "MaintenanceWorkOrderBuilder":
        self._description = description
        return self
    
    def with_cause_and_solution(self, cause: str, solution: str) -> "MaintenanceWorkOrderBuilder":
        self._cause = cause
        self._solution = solution
        return self
    
    def with_tasks(self, tasks: List[MaintenanceTask]) -> "MaintenanceWorkOrderBuilder":
        self._tasks = tasks
        return self
    
    def with_parts(self, parts: List[MaintenancePart]) -> "MaintenanceWorkOrderBuilder":
        self._parts = parts
        return self
    
    def with_labor_hours(self, hours: Decimal) -> "MaintenanceWorkOrderBuilder":
        self._labor_hours = hours
        return self
    
    def scheduled_for(self, scheduled_date: date) -> "MaintenanceWorkOrderBuilder":
        self._scheduled_date = scheduled_date
        return self
    
    def assigned_to(self, user_id: str, user_name: str) -> "MaintenanceWorkOrderBuilder":
        self._assigned_to = user_id
        self._assigned_name = user_name
        return self
    
    def requested_by(self, user_id: str, user_name: str) -> "MaintenanceWorkOrderBuilder":
        self._requested_by = user_id
        self._requested_name = user_name
        return self
    
    def with_notes(self, notes: str) -> "MaintenanceWorkOrderBuilder":
        self._notes = notes
        return self
    
    def with_metadata(self, metadata: Dict[str, Any]) -> "MaintenanceWorkOrderBuilder":
        self._metadata = metadata
        return self
    
    def build(self) -> MaintenanceWorkOrder:
        if not self._id:
            self._id = str(uuid4())
        if not self._work_order_number:
            from time import time
            self._work_order_number = f"WO-{int(time())}"
        if not self._asset_id:
            raise ValueError("asset_id is required")
        
        work_order = MaintenanceWorkOrder(
            id=self._id,
            work_order_number=self._work_order_number,
            asset_id=self._asset_id,
            asset_name=self._asset_name,
            asset_code=self._asset_code,
            maintenance_type=self._maintenance_type,
            status=self._status,
            priority=self._priority,
            description=self._description,
            cause=self._cause,
            solution=self._solution,
            tasks=self._tasks,
            parts=self._parts,
            labor_hours=self._labor_hours,
            scheduled_date=self._scheduled_date,
            assigned_to=self._assigned_to,
            assigned_name=self._assigned_name,
            requested_by=self._requested_by,
            requested_name=self._requested_name,
            notes=self._notes,
            metadata=self._metadata
        )
        
        work_order.calculate_costs()
        return work_order


def create_maintenance_work_order(
    asset_id: str,
    asset_name: str,
    asset_code: str,
    **kwargs
) -> MaintenanceWorkOrder:
    """Factory function to create a maintenance work order."""
    builder = MaintenanceWorkOrderBuilder()
    builder.for_asset(asset_id, asset_name, asset_code)
    
    if work_order_number := kwargs.get("work_order_number"):
        builder.with_work_order_number(work_order_number)
    if maintenance_type := kwargs.get("maintenance_type"):
        builder.with_maintenance_type(maintenance_type)
    if status := kwargs.get("status"):
        builder.with_status(status)
    if priority := kwargs.get("priority"):
        builder.with_priority(priority)
    if description := kwargs.get("description"):
        builder.with_description(description)
    if cause := kwargs.get("cause"):
        solution = kwargs.get("solution", "")
        builder.with_cause_and_solution(cause, solution)
    if tasks := kwargs.get("tasks"):
        builder.with_tasks(tasks)
    if parts := kwargs.get("parts"):
        builder.with_parts(parts)
    if labor_hours := kwargs.get("labor_hours"):
        builder.with_labor_hours(labor_hours)
    if scheduled_date := kwargs.get("scheduled_date"):
        builder.scheduled_for(scheduled_date)
    if assigned_to := kwargs.get("assigned_to"):
        assigned_name = kwargs.get("assigned_name", "")
        builder.assigned_to(assigned_to, assigned_name)
    if requested_by := kwargs.get("requested_by"):
        requested_name = kwargs.get("requested_name", "")
        builder.requested_by(requested_by, requested_name)
    if notes := kwargs.get("notes"):
        builder.with_notes(notes)
    if metadata := kwargs.get("metadata"):
        builder.with_metadata(metadata)
    
    return builder.build()


def create_maintenance_task(
    description: str,
    estimated_hours: Decimal,
    **kwargs
) -> MaintenanceTask:
    """Factory function to create a maintenance task."""
    return MaintenanceTask(
        id=str(uuid4()),
        description=description,
        estimated_hours=estimated_hours,
        notes=kwargs.get("notes", "")
    )


def create_maintenance_part(
    part_id: str,
    part_number: str,
    part_name: str,
    quantity: int,
    unit_cost: Decimal
) -> MaintenancePart:
    """Factory function to create a maintenance part."""
    return MaintenancePart(
        id=str(uuid4()),
        part_id=part_id,
        part_number=part_number,
        part_name=part_name,
        quantity=quantity,
        unit_cost=unit_cost,
        total_cost=unit_cost * quantity
    )
