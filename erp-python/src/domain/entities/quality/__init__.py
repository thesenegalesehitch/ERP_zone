"""
Quality Control Entity for ERP System.

This module provides the QualityControl entity for managing quality control
following Clean Architecture principles.
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional, Dict, Any, List
from enum import Enum
from decimal import Decimal


class QCStatus(str, Enum):
    """Quality Control status enumeration."""
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    PASSED = "passed"
    FAILED = "failed"
    REWORK = "rework"
    CANCELLED = "cancelled"


class QCType(str, Enum):
    """Quality Control type enumeration."""
    INSPECTION = "inspection"
    TEST = "test"
    AUDIT = "audit"
    CERTIFICATION = "certification"
    SURVEY = "survey"


class Severity(str, Enum):
    """Severity enumeration."""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


@dataclass(frozen=True)
class QCInspectionItem:
    """
    Value Object representing a QC inspection item.
    Immutable and validated.
    """
    id: str
    parameter: str
    specification: str
    result: Optional[str] = None
    status: str = "pending"
    notes: Optional[str] = None
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "parameter": self.parameter,
            "specification": self.specification,
            "result": self.result,
            "status": self.status,
            "notes": self.notes
        }


@dataclass(frozen=True)
class QualityControl:
    """
    QualityControl entity representing a quality control inspection.
    
    This entity follows Clean Architecture principles and is immutable.
    
    Attributes:
        id: Unique identifier for the QC
        qc_number: Human-readable QC number
        qc_type: Type of QC
        status: Current status
        order_id: Associated order ID
        product_id: Product ID
        product_name: Product name
        batch_number: Batch number
        sample_size: Sample size inspected
        inspector_id: Inspector ID
        inspector_name: Inspector name
        items: List of inspection items
        notes: Additional notes
        metadata: Additional metadata
        created_at: Timestamp when created
        updated_at: Timestamp when last updated
    """
    id: str
    qc_number: str
    qc_type: QCType
    status: QCStatus
    order_id: Optional[str] = None
    product_id: Optional[str] = None
    product_name: Optional[str] = None
    batch_number: Optional[str] = None
    sample_size: Optional[int] = None
    inspector_id: Optional[str] = None
    inspector_name: Optional[str] = None
    items: List[QCInspectionItem] = field(default_factory=list)
    notes: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime = field(default_factory=datetime.utcnow)
    
    def __post_init__(self):
        """Validate QC after initialization."""
        if not self.qc_number:
            raise ValueError("qc_number cannot be empty")
    
    @property
    def is_passed(self) -> bool:
        """Check if QC passed."""
        return self.status == QCStatus.PASSED
    
    @property
    def is_failed(self) -> bool:
        """Check if QC failed."""
        return self.status == QCStatus.FAILED
    
    @property
    def is_completed(self) -> bool:
        """Check if QC is completed."""
        return self.status in [QCStatus.PASSED, QCStatus.FAILED, QCStatus.REWORK]
    
    @property
    def item_count(self) -> int:
        """Get number of inspection items."""
        return len(self.items)
    
    @property
    def passed_items(self) -> int:
        """Get number of passed items."""
        return sum(1 for item in self.items if item.status == "passed")
    
    @property
    def failed_items(self) -> int:
        """Get number of failed items."""
        return sum(1 for item in self.items if item.status == "failed")
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert QC to dictionary."""
        return {
            "id": self.id,
            "qc_number": self.qc_number,
            "qc_type": self.qc_type.value,
            "status": self.status.value,
            "order_id": self.order_id,
            "product_id": self.product_id,
            "product_name": self.product_name,
            "batch_number": self.batch_number,
            "sample_size": self.sample_size,
            "inspector_id": self.inspector_id,
            "inspector_name": self.inspector_name,
            "items": [i.to_dict() for i in self.items],
            "notes": self.notes,
            "metadata": self.metadata,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
            "is_passed": self.is_passed,
            "is_failed": self.is_failed,
            "is_completed": self.is_completed,
            "item_count": self.item_count,
            "passed_items": self.passed_items,
            "failed_items": self.failed_items
        }


@dataclass(frozen=True)
class NonConformance:
    """
    NonConformance entity representing a quality non-conformance.
    
    This entity follows Clean Architecture principles and is immutable.
    
    Attributes:
        id: Unique identifier
        nc_number: Human-readable NC number
        title: NC title
        description: NC description
        severity: Severity level
        status: Current status
        product_id: Product ID
        product_name: Product name
        order_id: Associated order ID
        reported_by: Reporter user ID
        reporter_name: Reporter name
        assigned_to: Assigned user ID
        assignee_name: Assignee name
        root_cause: Root cause description
        corrective_action: Corrective action
        preventive_action: Preventive action
        metadata: Additional metadata
        created_at: Timestamp when created
        updated_at: Timestamp when last updated
        closed_at: Timestamp when closed
    """
    id: str
    nc_number: str
    title: str
    description: str
    severity: Severity
    status: str
    product_id: Optional[str] = None
    product_name: Optional[str] = None
    order_id: Optional[str] = None
    reported_by: Optional[str] = None
    reporter_name: Optional[str] = None
    assigned_to: Optional[str] = None
    assignee_name: Optional[str] = None
    root_cause: Optional[str] = None
    corrective_action: Optional[str] = None
    preventive_action: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime = field(default_factory=datetime.utcnow)
    closed_at: Optional[datetime] = None
    
    def __post_init__(self):
        if not self.nc_number:
            raise ValueError("nc_number cannot be empty")
        if not self.title:
            raise ValueError("title cannot be empty")
    
    @property
    def is_open(self) -> bool:
        return self.status == "open"
    
    @property
    def is_closed(self) -> bool:
        return self.status == "closed"
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "nc_number": self.nc_number,
            "title": self.title,
            "description": self.description,
            "severity": self.severity.value,
            "status": self.status,
            "product_id": self.product_id,
            "product_name": self.product_name,
            "order_id": self.order_id,
            "reported_by": self.reported_by,
            "reporter_name": self.reporter_name,
            "assigned_to": self.assigned_to,
            "assignee_name": self.assignee_name,
            "root_cause": self.root_cause,
            "corrective_action": self.corrective_action,
            "preventive_action": self.preventive_action,
            "metadata": self.metadata,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
            "closed_at": self.closed_at.isoformat() if self.closed_at else None,
            "is_open": self.is_open,
            "is_closed": self.is_closed
        }


class QualityControlBuilder:
    """Builder for creating QualityControl instances."""
    
    def __init__(self):
        self._id: Optional[str] = None
        self._qc_number: Optional[str] = None
        self._qc_type: QCType = QCType.INSPECTION
        self._status: QCStatus = QCStatus.PENDING
        self._order_id: Optional[str] = None
        self._product_id: Optional[str] = None
        self._product_name: Optional[str] = None
        self._batch_number: Optional[str] = None
        self._sample_size: Optional[int] = None
        self._inspector_id: Optional[str] = None
        self._inspector_name: Optional[str] = None
        self._items: List[QCInspectionItem] = []
        self._notes: Optional[str] = None
        self._metadata: Dict[str, Any] = {}
    
    def with_id(self, qc_id: str) -> "QualityControlBuilder":
        self._id = qc_id
        return self
    
    def with_number(self, qc_number: str) -> "QualityControlBuilder":
        self._qc_number = qc_number
        return self
    
    def with_type(self, qc_type: QCType) -> "QualityControlBuilder":
        self._qc_type = qc_type
        return self
    
    def with_status(self, status: QCStatus) -> "QualityControlBuilder":
        self._status = status
        return self
    
    def for_order(self, order_id: str) -> "QualityControlBuilder":
        self._order_id = order_id
        return self
    
    def for_product(self, product_id: str, product_name: str) -> "QualityControlBuilder":
        self._product_id = product_id
        self._product_name = product_name
        return self
    
    def with_batch(self, batch_number: str) -> "QualityControlBuilder":
        self._batch_number = batch_number
        return self
    
    def with_sample_size(self, size: int) -> "QualityControlBuilder":
        self._sample_size = size
        return self
    
    def inspected_by(self, inspector_id: str, inspector_name: str) -> "QualityControlBuilder":
        self._inspector_id = inspector_id
        self._inspector_name = inspector_name
        return self
    
    def with_items(self, items: List[QCInspectionItem]) -> "QualityControlBuilder":
        self._items = items
        return self
    
    def with_notes(self, notes: str) -> "QualityControlBuilder":
        self._notes = notes
        return self
    
    def with_metadata(self, metadata: Dict[str, Any]) -> "QualityControlBuilder":
        self._metadata = metadata
        return self
    
    def build(self) -> QualityControl:
        from uuid import uuid4
        
        if not self._id:
            self._id = str(uuid4())
        if not self._qc_number:
            from time import time
            self._qc_number = f"QC-{int(time())}"
        
        return QualityControl(
            id=self._id,
            qc_number=self._qc_number,
            qc_type=self._qc_type,
            status=self._status,
            order_id=self._order_id,
            product_id=self._product_id,
            product_name=self._product_name,
            batch_number=self._batch_number,
            sample_size=self._sample_size,
            inspector_id=self._inspector_id,
            inspector_name=self._inspector_name,
            items=self._items,
            notes=self._notes,
            metadata=self._metadata
        )


# Factory functions
def create_qc_item(
    parameter: str,
    specification: str,
    **kwargs
) -> QCInspectionItem:
    """Factory function to create a QC inspection item."""
    from uuid import uuid4
    
    return QCInspectionItem(
        id=str(uuid4()),
        parameter=parameter,
        specification=specification,
        result=kwargs.get("result"),
        status=kwargs.get("status", "pending"),
        notes=kwargs.get("notes")
    )


def create_quality_control(
    **kwargs
) -> QualityControl:
    """Factory function to create a quality control."""
    builder = QualityControlBuilder()
    
    if qc_type := kwargs.get("qc_type"):
        builder.with_type(qc_type)
    if order_id := kwargs.get("order_id"):
        builder.for_order(order_id)
    if product_id := kwargs.get("product_id"):
        product_name = kwargs.get("product_name", "")
        builder.for_product(product_id, product_name)
    if batch_number := kwargs.get("batch_number"):
        builder.with_batch(batch_number)
    if sample_size := kwargs.get("sample_size"):
        builder.with_sample_size(sample_size)
    if inspector_id := kwargs.get("inspector_id"):
        inspector_name = kwargs.get("inspector_name", "")
        builder.inspected_by(inspector_id, inspector_name)
    if items := kwargs.get("items"):
        builder.with_items(items)
    if notes := kwargs.get("notes"):
        builder.with_notes(notes)
    if metadata := kwargs.get("metadata"):
        builder.with_metadata(metadata)
    
    return builder.build()
